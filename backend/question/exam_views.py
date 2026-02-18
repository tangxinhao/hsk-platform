"""
考试相关视图
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import logging

from .models import QuestionSet, Question
from .exam_models import ExamAttempt, ExamReport, ExamRanking
from .services.exam_service import ExamService
from .serializers import QuestionSetSerializer, QuestionSerializer

# 获取日志记录器
logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([AllowAny])
def question_set_list(request):
    """获取套卷列表"""
    try:
        level = request.GET.get('level')
        
        queryset = QuestionSet.objects.all()
        
        if level:
            try:
                queryset = queryset.filter(level=int(level))
            except ValueError:
                logger.warning(f"无效的level参数: {level}")
                pass
        
        queryset = queryset.order_by('-created_at')
        
        serializer = QuestionSetSerializer(queryset, many=True)
        logger.info(f"成功获取{len(serializer.data)}个套卷")
        return Response(serializer.data)
        
    except Exception as e:
        logger.error(f"获取套卷列表失败: {str(e)}", exc_info=True)
        return Response(
            {'error': '获取套卷列表失败，请稍后重试'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def question_set_detail(request, pk):
    """获取套卷详情"""
    question_set = get_object_or_404(QuestionSet, pk=pk)
    
    # 获取该套卷的所有题目
    questions = Question.objects.filter(question_set=question_set).order_by('id')
    
    return Response({
        'question_set': QuestionSetSerializer(question_set).data,
        'questions': QuestionSerializer(questions, many=True).data,
        'total_questions': questions.count()
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def question_set_structured(request, pk):
    """获取结构化的套卷详情（按section和part组织）"""
    from .models import Material
    from collections import defaultdict
    
    question_set = get_object_or_404(QuestionSet, pk=pk)
    
    # 获取所有题目
    questions = Question.objects.filter(question_set=question_set).order_by(
        'section_type', 'part_number', 'question_number', 'id'
    )
    
    # 获取所有材料
    materials = Material.objects.filter(
        level=question_set.level,
        is_active=True
    ).order_by('section_type', 'part_number', 'order')
    
    # 构建section和part的结构
    sections_dict = defaultdict(lambda: {
        'parts': defaultdict(lambda: {
            'questions': [],
            'material': None
        })
    })
    
    # 处理题目
    for question in questions:
        # 如果没有section_type，根据题目类型自动分配
        if question.section_type:
            section_type = question.section_type
        else:
            # 根据题目类型自动分类
            if question.type in ['listening', 'judge'] and question.audio_url:
                section_type = 'listening'
            elif question.type in ['fill', 'essay', 'writing']:
                section_type = 'writing'
            else:
                section_type = 'reading'
        
        part_number = question.part_number or 1
        
        # 构建题目数据
        question_data = QuestionSerializer(question).data
        
        sections_dict[section_type]['parts'][part_number]['questions'].append(question_data)
    
    # 处理材料
    for material in materials:
        section_type = material.section_type
        part_number = material.part_number
        
        if section_type in sections_dict and part_number in sections_dict[section_type]['parts']:
            sections_dict[section_type]['parts'][part_number]['material'] = {
                'id': material.id,
                'title': material.title,
                'content': material.content,
                'audio_url': material.audio_url,
                'audio_duration': material.audio_duration,
                'play_times': material.play_times,
                'question_range_start': material.question_range_start,
                'question_range_end': material.question_range_end
            }
    
    # 转换为列表结构
    sections = []
    section_names = {
        'listening': '听力',
        'reading': '阅读',
        'writing': '书写'
    }
    section_icons = {
        'listening': 'Headset',
        'reading': 'Reading',
        'writing': 'Edit'
    }
    
    for section_type in ['listening', 'reading', 'writing']:
        if section_type in sections_dict:
            parts = []
            section_audio_url = None
            section_audio_duration = 0
            
            # 对于听力部分，优先使用QuestionSet的统一音频，否则查找Material中的音频
            if section_type == 'listening':
                # 构造当前请求的完整主机地址，例如 http://118.190.106.159
                full_host = f"{request.scheme}://{request.get_host()}"

                def build_full_url(url: str) -> str:
                    """
                    将相对路径转换为完整URL:
                    - /media/xxx -> http://host/media/xxx
                    - media/xxx  -> http://host/media/xxx
                    - 已经是 http(s) 开头则原样返回
                    """
                    if not url:
                        return url
                    if url.startswith('http'):
                        return url
                    path = url if url.startswith('/') else f'/{url}'
                    return f'{full_host}{path}'

                # 优先使用套卷配置的统一听力音频
                if question_set.listening_audio_url:
                    audio_url = question_set.listening_audio_url
                    section_audio_url = build_full_url(audio_url)
                    section_audio_duration = question_set.listening_audio_duration or 0
                else:
                    # 否则查找Material中duration最长的音频
                    listening_materials = Material.objects.filter(
                        level=question_set.level,
                        section_type='listening',
                        is_active=True
                    ).order_by('-audio_duration')
                    
                    if listening_materials.exists():
                        longest_material = listening_materials.first()
                        audio_url = longest_material.audio_url
                        section_audio_url = build_full_url(audio_url)
                        section_audio_duration = longest_material.audio_duration
            
            for part_num, part_data in sorted(sections_dict[section_type]['parts'].items()):
                part_info = {
                    'id': f'{section_type}_part{part_num}',
                    'part_number': part_num,
                    'title': f'第{part_num}部分',
                    'description': get_part_description(section_type, part_num, question_set.level),
                    'questions': part_data['questions'],
                    'material': part_data['material']
                }
                
                # 如果有材料，使用材料的标题
                if part_data['material']:
                    part_info['title'] = part_data['material']['title']
                    part_info['passage'] = part_data['material']['content']
                
                parts.append(part_info)
            
            section_info = {
                'id': section_type,
                'name': section_names.get(section_type, section_type),
                'type': section_type,
                'icon': section_icons.get(section_type, 'Document'),
                'parts': parts
            }
            
            # 如果是听力Section且有音频，添加到Section级别
            if section_type == 'listening' and section_audio_url:
                section_info['audio_url'] = section_audio_url
                section_info['audio_duration'] = section_audio_duration
            
            sections.append(section_info)
    
    return Response({
        'exam_id': question_set.id,
        'title': question_set.title,
        'level': question_set.level,
        'time_limit': question_set.time_limit,
        'total_questions': questions.count(),
        'sections': sections
    })


def get_part_description(section_type, part_number, level):
    """获取Part的描述文本"""
    descriptions = {
        'listening': {
            1: '听录音，选择正确答案',
            2: '听录音，判断对错',
            3: '听对话，回答问题',
            4: '听短文，回答问题'
        },
        'reading': {
            1: '选择正确的词语',
            2: '选择正确的句子',
            3: '阅读短文，回答问题',
            4: '阅读长文，回答问题'
        },
        'writing': {
            1: '组词成句',
            2: '看图写话',
            3: '写短文'
        }
    }
    
    return descriptions.get(section_type, {}).get(part_number, '完成题目')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_exam(request):
    """开始考试"""
    question_set_id = request.data.get('question_set_id')
    
    if not question_set_id:
        return Response(
            {'error': '请提供套卷ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    question_set = get_object_or_404(QuestionSet, pk=question_set_id)
    
    try:
        exam_attempt = ExamService.start_exam(request.user, question_set)
        
        return Response({
            'exam_id': exam_attempt.id,
            'question_set_id': question_set.id,
            'question_set_title': question_set.title,
            'time_limit': question_set.time_limit,
            'start_time': exam_attempt.start_time.isoformat(),
            'status': exam_attempt.status
        })
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request, exam_id):
    """提交答案"""
    exam_attempt = get_object_or_404(ExamAttempt, pk=exam_id, user=request.user)
    
    question_id = request.data.get('question_id')
    user_answer = request.data.get('answer')
    
    if not question_id:
        return Response(
            {'error': '请提供题目ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        exam_attempt.submit_answer(question_id, user_answer)
        
        return Response({
            'message': '答案已提交',
            'exam_id': exam_attempt.id,
            'answered_count': len(exam_attempt.answers)
        })
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_exam(request, exam_id):
    """完成考试"""
    exam_attempt = get_object_or_404(ExamAttempt, pk=exam_id, user=request.user)
    
    try:
        exam_attempt = ExamService.submit_exam(exam_attempt)
        
        return Response({
            'message': '考试已完成',
            'exam_id': exam_attempt.id,
            'score': float(exam_attempt.score),
            'status': exam_attempt.status
        })
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def abandon_exam(request, exam_id):
    """放弃考试"""
    exam_attempt = get_object_or_404(ExamAttempt, pk=exam_id, user=request.user)
    
    exam_attempt.abandon()
    
    return Response({
        'message': '考试已放弃',
        'exam_id': exam_attempt.id
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_history(request):
    """获取考试历史"""
    limit = request.GET.get('limit', 10)
    
    history = ExamService.get_user_exam_history(request.user, limit=limit)
    
    data = [{
        'exam_id': attempt.id,
        'question_set_title': attempt.question_set.title,
        'level': attempt.question_set.level,
        'score': float(attempt.score) if attempt.score else 0,
        'status': attempt.status,
        'start_time': attempt.start_time.isoformat(),
        'end_time': attempt.end_time.isoformat() if attempt.end_time else None,
        'duration': attempt.get_duration_minutes()
    } for attempt in history]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_report(request, exam_id):
    """获取考试报告"""
    exam_attempt = get_object_or_404(ExamAttempt, pk=exam_id, user=request.user)
    
    try:
        report = ExamReport.objects.get(exam_attempt=exam_attempt)
        
        return Response({
            'exam_id': exam_attempt.id,
            'question_set_title': exam_attempt.question_set.title,
            'score': float(exam_attempt.score),
            'total_questions': report.total_questions,
            'correct_count': report.correct_count,
            'accuracy_rate': float(report.accuracy_rate),
            'time_spent': report.time_spent,
            'category_performance': report.category_performance,
            'weak_points': report.weak_points,
            'suggestions': report.suggestions
        })
    except ExamReport.DoesNotExist:
        return Response(
            {'error': '报告未生成'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_ranking(request, exam_id):
    """获取考试排行榜"""
    exam_attempt = get_object_or_404(ExamAttempt, pk=exam_id)
    question_set = exam_attempt.question_set
    
    rankings = ExamService.get_leaderboard(question_set, limit=50)
    
    data = [{
        'rank': ranking.rank,
        'username': ranking.user.username,
        'score': float(ranking.score),
        'time_spent': ranking.time_spent // 60,  # 转为分钟
        'is_current_user': ranking.user == request.user
    } for ranking in rankings]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_statistics(request):
    """获取用户考试统计"""
    stats = ExamService.get_exam_statistics(request.user)
    return Response(stats)
