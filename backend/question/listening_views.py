"""
听力题组批量管理API
提供听力题组的创建、查询、更新功能
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.db.models import Q
from django.core.files.base import ContentFile
import base64
import uuid
import json
from datetime import datetime

from django.conf import settings
import os

from .models import Material, Question
from .serializers import MaterialSerializer, QuestionSerializer


def _build_audio_url(request, audio_url: str):
    """
    构造可访问的完整音频URL，如果文件缺失则尝试使用默认音频占位
    """
    if not audio_url:
        return None

    def _check_exists(path: str):
        if not path:
            return False
        return os.path.exists(path)

    # 相对路径 => MEDIA_ROOT + media/...
    if not audio_url.startswith('http'):
        rel_path = audio_url.lstrip('/')
        file_path = os.path.join(settings.BASE_DIR, rel_path)
        if not _check_exists(file_path) and rel_path.startswith('media/'):
            file_path = os.path.join(settings.MEDIA_ROOT, rel_path[len('media/'):])
        # fallback
        if not _check_exists(file_path):
            fallback = os.path.join(settings.MEDIA_ROOT, 'audio', 'H11556.mp3')
            if _check_exists(fallback):
                return request.build_absolute_uri('/media/audio/H11556.mp3')
        return request.build_absolute_uri('/' + rel_path)

    # http开头：尝试解析本地文件是否存在
    full_url = audio_url
    if '/media/' in audio_url:
        rel_path = audio_url.split('/media/', 1)[-1]
        file_path = os.path.join(settings.MEDIA_ROOT, rel_path)
        if not _check_exists(file_path):
            fallback = os.path.join(settings.MEDIA_ROOT, 'audio', 'H11556.mp3')
            if _check_exists(fallback):
                return request.build_absolute_uri('/media/audio/H11556.mp3')

    return full_url


@api_view(['POST'])
@permission_classes([AllowAny])
def create_listening_group(request):
    """
    批量创建听力题组
    一段音频对应多道题目
    """
    try:
        material_data = request.data.get('material', {})
        questions_data = request.data.get('questions', [])
        
        if not material_data or not questions_data:
            return Response({
                'error': '缺少必要参数：material 和 questions'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 生成唯一的材料组标识
        material_group = f"HSK{material_data.get('level', 1)}_L_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        with transaction.atomic():
            # 1. 创建Material记录
            material = Material.objects.create(
                title=material_data.get('title', '未命名材料'),
                level=material_data.get('level', 1),
                section_type='listening',
                part_number=material_data.get('part_number', 1),
                content=material_data.get('content', ''),
                audio_duration=material_data.get('duration', 0),
                material_group=material_group,
                play_times=material_data.get('play_times', 2),
                question_range_start=1,
                question_range_end=len(questions_data),
                order=material_data.get('order', 0)
            )
            
            # 处理音频文件上传
            if 'audio_file' in material_data:
                audio_data = material_data['audio_file']
                if audio_data.startswith('data:audio'):
                    # Base64格式
                    format, audio_str = audio_data.split(';base64,')
                    ext = format.split('/')[-1]
                    audio_file = ContentFile(
                        base64.b64decode(audio_str),
                        name=f'{material_group}.{ext}'
                    )
                    material.audio_url = f'/media/audio/{material_group}.{ext}'
                    # 这里需要实际保存文件，暂时只设置URL
            elif 'audio_url' in material_data:
                material.audio_url = material_data['audio_url']
            
            material.save()
            
            # 2. 批量创建Question记录
            created_questions = []
            for idx, q_data in enumerate(questions_data, 1):
                # 处理选项数据
                options = q_data.get('options', [])
                option_type = q_data.get('option_type', 'text')
                
                # 构建标准化的options JSON
                formatted_options = {
                    'option_type': option_type,
                    'options': []
                }
                
                for opt in options:
                    option_item = {
                        'label': opt.get('label', ''),
                        'value': opt.get('value', opt.get('label', ''))
                    }
                    
                    if option_type == 'text':
                        option_item['text'] = opt.get('text', '')
                    elif option_type == 'image':
                        option_item['image'] = opt.get('image', '')
                        option_item['text'] = opt.get('text', '')  # 图片说明文字
                    elif option_type == 'mixed':
                        option_item['text'] = opt.get('text', '')
                        option_item['image'] = opt.get('image', '')
                    
                    formatted_options['options'].append(option_item)
                
                question = Question.objects.create(
                    content=q_data.get('content', f'第{idx}题'),
                    type=q_data.get('type', 'single'),
                    level=material_data.get('level', 1),
                    difficulty=q_data.get('difficulty', 2),
                    section_type='listening',  # 使用section_type字段
                    part_number=material_data.get('part_number', 1),
                    answer=q_data.get('answer', ''),
                    explanation=q_data.get('explanation', ''),
                    options=json.dumps(formatted_options, ensure_ascii=False),  # 转换为JSON字符串
                    material_group=material_group,  # 关联Material
                    audio_group=material_group,      # 同时设置audio_group
                    audio_url=material.audio_url,
                    question_number=idx
                )
                created_questions.append(question)
            
            # 3. 返回创建结果
            return Response({
                'success': True,
                'message': f'成功创建听力题组，包含 {len(created_questions)} 道题目',
                'data': {
                    'material_group': material_group,
                    'material': MaterialSerializer(material).data,
                    'questions': QuestionSerializer(created_questions, many=True).data
                }
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            'error': f'创建失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def get_listening_group(request, material_group):
    """
    查询或更新听力题组
    GET: 返回材料信息和所有关联的题目
    PUT: 更新题组信息
    """
    if request.method == 'GET':
        try:
            # 查询Material
            try:
                material = Material.objects.get(material_group=material_group)
            except Material.DoesNotExist:
                return Response({
                    'error': '未找到该听力材料'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 查询所有关联的Question（同时检查material_group和audio_group）
            questions = Question.objects.filter(
                Q(material_group=material_group) | Q(audio_group=material_group)
            ).order_by('question_number', 'id')
            
            material_data = MaterialSerializer(material).data
            material_data['audio_url'] = _build_audio_url(request, material_data.get('audio_url'))

            return Response({
                'material': material_data,
                'questions': QuestionSerializer(questions, many=True).data,
                'total_questions': questions.count()
            })
            
        except Exception as e:
            return Response({
                'error': f'查询失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    elif request.method == 'PUT':
        # 调用更新函数
        return update_listening_group(request, material_group)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_listening_groups(request):
    """
    列出所有听力题组
    支持按等级、日期筛选
    """
    try:
        level = request.query_params.get('level')
        
        # 查询所有听力材料
        materials = Material.objects.filter(section_type='listening')
        
        if level:
            materials = materials.filter(level=int(level))
        
        materials = materials.order_by('-created_at')
        
        # 组装数据
        result = []
        for material in materials:
            question_count = Question.objects.filter(
                Q(material_group=material.material_group) | Q(audio_group=material.material_group)
            ).count()
            
            result.append({
                'material_group': material.material_group,
                'title': material.title,
                'level': material.level,
                'question_count': question_count,
                'audio_duration': material.audio_duration,
                'play_times': material.play_times,
                'created_at': material.created_at.isoformat() if material.created_at else None,
                'audio_url': _build_audio_url(request, material.audio_url)
            })
        
        return Response({
            'count': len(result),
            'results': result
        })
        
    except Exception as e:
        return Response({
            'error': f'查询失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_listening_group(request, material_group):
    """
    更新听力题组
    """
    try:
        material_data = request.data.get('material', {})
        questions_data = request.data.get('questions', [])
        
        with transaction.atomic():
            # 更新Material
            try:
                material = Material.objects.get(material_group=material_group)
            except Material.DoesNotExist:
                return Response({
                    'error': '未找到该听力材料'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 更新材料信息
            if material_data:
                material.title = material_data.get('title', material.title)
                material.level = material_data.get('level', material.level)
                material.play_times = material_data.get('play_times', material.play_times)
                material.audio_duration = material_data.get('audio_duration', material.audio_duration)
                
                # 保留原音频URL或更新为新URL
                if 'audio_url' in material_data and material_data['audio_url']:
                    material.audio_url = material_data['audio_url']
                
                material.save()
            
            # 更新Questions
            if questions_data:
                # 删除现有题目（使用material_group或audio_group）
                Question.objects.filter(
                    Q(material_group=material_group) | Q(audio_group=material_group)
                ).delete()
                
                # 创建新题目
                for idx, q_data in enumerate(questions_data, 1):
                    # 正确处理选项数据
                    options_data = q_data.get('options', {})
                    if isinstance(options_data, dict):
                        formatted_options = json.dumps({
                            'option_type': options_data.get('option_type', 'text'),
                            'options': options_data.get('options', [])
                        }, ensure_ascii=False)
                    else:
                        formatted_options = json.dumps(options_data, ensure_ascii=False)
                    
                    Question.objects.create(
                        content=q_data.get('content', f'第{idx}题'),
                        type=q_data.get('type', 'single'),
                        level=material.level,
                        difficulty=q_data.get('difficulty', 2),
                        section_type='listening',
                        answer=q_data.get('answer', ''),
                        explanation=q_data.get('explanation', ''),
                        options=formatted_options,
                        material_group=material_group,
                        audio_group=material_group,
                        audio_url=material.audio_url,
                        question_number=idx
                    )
            
            return Response({
                'success': True,
                'message': '更新成功'
            })
            
    except Exception as e:
        return Response({
            'error': f'更新失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_listening_group(request, material_group):
    """
    删除听力题组
    """
    try:
        with transaction.atomic():
            # 删除Material
            Material.objects.filter(material_group=material_group).delete()
            
            # 删除所有关联的Questions
            Question.objects.filter(audio_group=material_group).delete()
            
            return Response({
                'success': True,
                'message': '删除成功'
            })
            
    except Exception as e:
        return Response({
            'error': f'删除失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
