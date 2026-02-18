"""
学习进度API视图
提供用户学习统计和进度数据
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q, Min
from django.utils import timezone
from datetime import timedelta, datetime
from .models import User
from question.models import AnswerRecord, QuestionSet
from question.exam_models import ExamAttempt


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_progress_overview(request):
    """
    获取学习进度概览
    返回：总练习数、正确率、学习天数、总积分
    """
    user = request.user

    # 基础统计：答题记录
    answers = AnswerRecord.objects.filter(user=user)
    total_practices = answers.count()
    correct_count = answers.filter(is_correct=True).count()
    wrong_count = total_practices - correct_count
    correct_rate = round(correct_count / total_practices * 100, 1) if total_practices else 0

    # 从考试尝试获取得分累计（如无字段，则为0）
    total_score = getattr(user, 'total_score', 0) or 0

    # 计算学习天数（从第一次答题或考试开始）
    first_answer = answers.aggregate(first_time=Min('created_at'))['first_time']
    
    from question.exam_models import ExamAttempt
    first_exam = ExamAttempt.objects.filter(user=user).aggregate(first_time=Min('start_time'))['first_time']

    first_time = None
    if first_answer and first_exam:
        first_time = min(first_answer, first_exam)
    elif first_answer:
        first_time = first_answer
    elif first_exam:
        first_time = first_exam

    if first_time:
        study_days = (timezone.now().date() - first_time.date()).days + 1
    else:
        study_days = 0

    return Response({
        'total_practices': total_practices,
        'correct_rate': correct_rate,
        'study_days': study_days,
        'total_score': total_score,
        'wrong_count': wrong_count
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_level_progress(request):
    """
    获取各HSK等级的学习进度
    """
    user = request.user
    level_data = []
    
    from question.models import Question
    
    for level in range(1, 7):
        # 获取该等级的练习记录（通过question__level匹配）
        level_answers = AnswerRecord.objects.filter(
            user=user,
            question__level=level
        )
        
        total_practiced = level_answers.count()
        correct_count = level_answers.filter(is_correct=True).count()
        
        # 计算正确率
        accuracy = round(correct_count / total_practiced * 100, 1) if total_practiced > 0 else 0
        
        # 获取该等级的总题目数
        total_questions = Question.objects.filter(level=level).count()
        
        # 计算进度百分比（基于实际题目数）
        if total_questions > 0:
            # 获取该等级已练习的不同题目数（去重）
            unique_practiced = AnswerRecord.objects.filter(
                user=user,
                question__level=level
            ).values('question').distinct().count()
            
            progress = min(100, round(unique_practiced / total_questions * 100, 1))
        else:
            progress = 0
        
        level_data.append({
            'level': level,
            'progress': progress,
            'practiced': total_practiced,
            'accuracy': accuracy
        })
    
    return Response(level_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_activities(request):
    """
    获取当前登录用户的最近学习活动记录
    """
    user = request.user
    if not user or not user.is_authenticated:
        return Response([])
    activities = []
    
    # 获取最近的考试记录
    recent_exams = ExamAttempt.objects.filter(
        user=user,
        status='completed'
    ).select_related('question_set').order_by('-end_time')[:5]
    
    for exam in recent_exams:
        # 计算时间差
        time_diff = timezone.now() - exam.end_time
        if time_diff.days == 0:
            if time_diff.seconds < 3600:
                time_str = f"{time_diff.seconds // 60}分钟前"
            else:
                time_str = f"{time_diff.seconds // 3600}小时前"
        elif time_diff.days == 1:
            time_str = "昨天 " + exam.end_time.strftime('%H:%M')
        else:
            time_str = exam.end_time.strftime('%m月%d日 %H:%M')
        
        activities.append({
            'type': 'exam',
            'title': f"完成{exam.question_set.title}",
            'description': f"HSK{exam.question_set.level}模拟考试",
            'time': time_str,
            'score': exam.score
        })
    
    # 不再使用StudyStatistics表，只返回考试记录
    return Response(activities)


@api_view(['GET'])
def get_study_goals(request):
    """
    获取学习目标和进度
    """
    # 临时使用第一个用户（演示用）
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user = User.objects.first()
    if not user:
        return Response({
            'has_goal': False,
            'daily_goal': 10,
            'daily_progress': 0,
            'weekly_goal': 70,
            'weekly_progress': 0,
            'monthly_goal': 300,
            'monthly_progress': 0
        })
    
    # 默认目标（暂时不依赖StudyGoal表）
    daily_goal = 10
    weekly_goal = 70
    monthly_goal = 300
    
    # 获取今日进度（从AnswerRecord统计）
    today = timezone.now().date()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    daily_progress = AnswerRecord.objects.filter(
        user=user,
        created_at__range=(today_start, today_end)
    ).count()
    
    # 获取本周进度
    week_start = today - timedelta(days=today.weekday())
    week_start_dt = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
    
    weekly_progress = AnswerRecord.objects.filter(
        user=user,
        created_at__gte=week_start_dt
    ).count()
    
    # 获取本月进度
    month_start = today.replace(day=1)
    month_start_dt = timezone.make_aware(datetime.combine(month_start, datetime.min.time()))
    
    monthly_progress = AnswerRecord.objects.filter(
        user=user,
        created_at__gte=month_start_dt
    ).count()
    
    return Response({
        'has_goal': False,  # 暂时设为False
        'daily_goal': daily_goal,
        'daily_progress': daily_progress,
        'weekly_goal': weekly_goal,
        'weekly_progress': weekly_progress,
        'monthly_goal': monthly_goal,
        'monthly_progress': monthly_progress
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weak_points(request):
    """
    获取薄弱知识点分析
    """
    user = request.user
    
    # 分析各题型的正确率
    from question.models import Question
    
    weak_points = []
    
    # 按题型分组统计
    question_types = Question.objects.filter(
        answerrecord__user=user
    ).values('question_type').distinct()
    
    for qt in question_types:
        q_type = qt['question_type']
        type_answers = AnswerRecord.objects.filter(
            user=user,
            question__question_type=q_type
        )
        
        total = type_answers.count()
        correct = type_answers.filter(is_correct=True).count()
        accuracy = round(correct / total * 100, 1) if total > 0 else 0
        
        if accuracy < 70:  # 正确率低于70%视为薄弱点
            type_name_map = {
                'listening': '听力',
                'reading': '阅读',
                'writing': '写作',
                'grammar': '语法',
                'vocabulary': '词汇'
            }
            
            weak_points.append({
                'type': q_type,
                'type_name': type_name_map.get(q_type, q_type),
                'accuracy': accuracy,
                'total_practiced': total,
                'suggestion': f'建议多练习{type_name_map.get(q_type, q_type)}相关内容'
            })
    
    return Response(weak_points)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_study_trend(request):
    """
    获取学习趋势数据
    """
    user = request.user
    days = int(request.GET.get('days', 7))  # 默认7天
    
    # 计算日期范围
    from django.utils import timezone as tz
    end_datetime = tz.now()
    end_date = end_datetime.date()
    start_date = end_date - timedelta(days=days - 1)
    
    # 生成日期列表
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    
    # 查询每天的答题数量
    trend_data = []
    max_count = 1  # 用于计算百分比
    
    for date in date_list:
        next_date = date + timedelta(days=1)
        # 使用timezone-aware datetime
        start_datetime = tz.make_aware(datetime.combine(date, datetime.min.time()))
        end_datetime = tz.make_aware(datetime.combine(next_date, datetime.min.time()))
        
        count = AnswerRecord.objects.filter(
            user=user,
            created_at__gte=start_datetime,
            created_at__lt=end_datetime
        ).count()
        
        # 格式化日期，30天时只显示月/日，不显示年
        date_str = date.strftime('%m/%d').lstrip('0').replace('/0', '/')
        
        trend_data.append({
            'date': date_str,
            'count': count
        })
        max_count = max(max_count, count)
    
    # 计算百分比（用于显示柱状图高度）
    for item in trend_data:
        item['percentage'] = round(item['count'] / max_count * 100) if max_count > 0 else 0
    
    return Response(trend_data)
