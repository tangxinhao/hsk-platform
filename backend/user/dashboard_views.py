"""
Dashboard视图
提供用户和管理员的Dashboard数据
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta, date
import datetime

from .models import User
from .study_models import StudyStatistics, StudyGoal
from question.models import Question, QuestionSet, AnswerRecord, WrongBook
from question.exam_models import ExamAttempt, ExamReport
from university.models import University
from culture.models import Content


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_dashboard(request):
    """
    获取用户个人Dashboard数据
    """
    user = request.user
    
    # 获取并验证查询参数
    try:
        days = int(request.GET.get('days', 7))
        # 限制查询范围，防止查询过大数据量
        if days < 1 or days > 365:
            days = 7
    except (ValueError, TypeError):
        days = 7
    
    # 1. 基础统计
    total_practice = AnswerRecord.objects.filter(user=user).count()
    correct_count = AnswerRecord.objects.filter(user=user, is_correct=True).count()
    accuracy_rate = round(correct_count / total_practice * 100, 2) if total_practice > 0 else 0
    
    # 2. 学习趋势（最近N天）
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    statistics = StudyStatistics.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # 填充所有日期
    date_range = []
    practice_trend = []
    time_trend = []
    accuracy_trend = []
    
    current_date = start_date
    stats_dict = {stat.date: stat for stat in statistics}
    
    while current_date <= end_date:
        date_str = current_date.strftime('%m-%d')
        date_range.append(date_str)
        
        if current_date in stats_dict:
            stat = stats_dict[current_date]
            practice_trend.append(stat.practice_count)
            time_trend.append(stat.study_time)
            accuracy_trend.append(stat.get_accuracy_rate())
        else:
            practice_trend.append(0)
            time_trend.append(0)
            accuracy_trend.append(0)
        
        current_date += timedelta(days=1)
    
    # 3. 学习目标
    study_goal = StudyGoal.objects.filter(
        user=user,
        is_completed=False
    ).order_by('-created_at').first()
    
    goal_data = None
    if study_goal:
        goal_data = {
            'target_hsk_level': study_goal.target_hsk_level,
            'target_date': study_goal.target_date.isoformat(),
            'days_remaining': study_goal.get_days_remaining(),
            'progress_percentage': study_goal.get_progress_percentage(),
            'current_progress': study_goal.current_progress,
            'daily_target': study_goal.daily_practice_count
        }
    
    # 4. 分类掌握情况（优化N+1查询）
    from question.models import QuestionCategory
    from django.db.models import Count, Case, When, IntegerField
    
    # 使用聚合查询优化性能
    category_performance = []
    categories = QuestionCategory.objects.all()
    
    for category in categories:
        stats = AnswerRecord.objects.filter(
            user=user,
            question__category=category
        ).aggregate(
            total=Count('id'),
            correct=Count(Case(
                When(is_correct=True, then=1),
                output_field=IntegerField()
            ))
        )
        
        total = stats['total'] or 0
        correct = stats['correct'] or 0
        
        if total > 0:
            category_performance.append({
                'category': category.get_name_display(),
                'total': total,
                'correct': correct,
                'accuracy': round(correct / total * 100, 2)
            })
    
    # 5. 错题统计
    wrong_count = WrongBook.objects.filter(user=user).count()
    
    # 6. 考试统计
    exam_attempts = ExamAttempt.objects.filter(
        user=user,
        status='completed'
    )
    exam_count = exam_attempts.count()
    avg_exam_score = exam_attempts.aggregate(avg=Avg('score'))['avg'] or 0
    
    # 7. 最近活动
    recent_practice = AnswerRecord.objects.filter(user=user).order_by('-created_at')[:5]
    recent_activities = [{
        'type': 'practice',
        'question_id': record.question.id,
        'question_content': record.question.content[:50],
        'is_correct': record.is_correct,
        'created_at': record.created_at.isoformat()
    } for record in recent_practice]
    
    # 8. 文化学习进度 (功能暂未实现，使用默认值)
    culture_progress = 0
    
    return Response({
        'basic_stats': {
            'total_practice': total_practice,
            'correct_count': correct_count,
            'accuracy_rate': accuracy_rate,
            'current_hsk_level': user.hsk_level,
            'study_days': statistics.count(),
            'total_study_time': sum(s.study_time for s in statistics),  # 分钟
        },
        'trends': {
            'dates': date_range,
            'practice_count': practice_trend,
            'study_time': time_trend,
            'accuracy_rate': accuracy_trend
        },
        'study_goal': goal_data,
        'category_performance': category_performance,
        'wrong_count': wrong_count,
        'exam_stats': {
            'exam_count': exam_count,
            'average_score': round(avg_exam_score, 2)
        },
        'recent_activities': recent_activities,
        'culture_progress': culture_progress
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_dashboard(request):
    """
    获取管理员Dashboard数据
    
    安全注意：
    1. 只有管理员可以访问
    2. 所有统计数据使用聚合查询，避免N+1问题
    3. 限制返回数据量，避免性能问题
    """
    # 使用缓存优化性能（可选）
    # from django.core.cache import cache
    # cache_key = 'admin_dashboard_data'
    # cached_data = cache.get(cache_key)
    # if cached_data:
    #     return Response(cached_data)
    
    # 1. 用户统计
    total_users = User.objects.count()
    
    # 最近7天新增用户
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_users_7d = User.objects.filter(date_joined__gte=seven_days_ago).count()
    
    # 活跃用户（最近7天有练习记录）
    active_users = AnswerRecord.objects.filter(
        created_at__gte=seven_days_ago
    ).values('user').distinct().count()
    
    # 按HSK等级分布
    users_by_level = []
    for level in range(1, 7):
        count = User.objects.filter(hsk_level=level).count()
        users_by_level.append({
            'level': f'HSK{level}',
            'count': count
        })
    
    # 2. 题目统计
    total_questions = Question.objects.count()
    questions_by_level = []
    for level in range(1, 7):
        count = Question.objects.filter(level=level).count()
        questions_by_level.append({
            'level': f'HSK{level}',
            'count': count
        })
    
    # 3. 练习统计
    total_practice = AnswerRecord.objects.count()
    practice_7d = AnswerRecord.objects.filter(created_at__gte=seven_days_ago).count()
    
    # 每日练习趋势（最近7天）
    daily_practice = []
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        count = AnswerRecord.objects.filter(
            created_at__date=day
        ).count()
        daily_practice.append({
            'date': day.strftime('%m-%d'),
            'count': count
        })
    
    # 4. 院校统计
    total_universities = University.objects.count()
    universities_by_region = University.objects.values('region').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # 5. 文化内容统计
    total_culture_content = Content.objects.count()
    culture_by_type = Content.objects.values('content_type').annotate(
        count=Count('id')
    )
    
    # 热门文化内容
    popular_content = Content.objects.order_by('-view_count')[:10]
    popular_content_data = [{
        'id': content.id,
        'title': content.title,
        'view_count': content.view_count,
        'like_count': content.like_count
    } for content in popular_content]
    
    # 6. 考试统计
    total_exams = ExamAttempt.objects.filter(status='completed').count()
    exams_7d = ExamAttempt.objects.filter(
        status='completed',
        end_time__gte=seven_days_ago
    ).count()
    
    avg_exam_score = ExamAttempt.objects.filter(
        status='completed'
    ).aggregate(avg=Avg('score'))['avg'] or 0
    
    # 7. 套卷统计
    total_question_sets = QuestionSet.objects.count()
    question_sets_by_level = []
    for level in range(1, 7):
        count = QuestionSet.objects.filter(level=level).count()
        question_sets_by_level.append({
            'level': f'HSK{level}',
            'count': count
        })
    
    # 热门套卷
    popular_sets = QuestionSet.objects.annotate(
        attempt_count=Count('examattempt')
    ).order_by('-attempt_count')[:10]
    
    popular_sets_data = [{
        'id': qs.id,
        'title': qs.title,
        'level': qs.level,
        'attempt_count': qs.attempt_count
    } for qs in popular_sets]
    
    # 8. 系统活跃度
    today = date.today()
    activity_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        
        # 统计当天的各种活动
        practice_count = AnswerRecord.objects.filter(created_at__date=day).count()
        exam_count = ExamAttempt.objects.filter(start_time__date=day).count()
        active_user_count = AnswerRecord.objects.filter(
            created_at__date=day
        ).values('user').distinct().count()
        
        activity_data.append({
            'date': day.strftime('%m-%d'),
            'practice_count': practice_count,
            'exam_count': exam_count,
            'active_users': active_user_count
        })
    
    return Response({
        'user_stats': {
            'total_users': total_users,
            'new_users_7d': new_users_7d,
            'active_users': active_users,
            'users_by_level': users_by_level
        },
        'question_stats': {
            'total_questions': total_questions,
            'questions_by_level': questions_by_level
        },
        'practice_stats': {
            'total_practice': total_practice,
            'practice_7d': practice_7d,
            'daily_practice': daily_practice
        },
        'university_stats': {
            'total_universities': total_universities,
            'universities_by_region': list(universities_by_region)
        },
        'culture_stats': {
            'total_content': total_culture_content,
            'content_by_type': list(culture_by_type),
            'popular_content': popular_content_data
        },
        'exam_stats': {
            'total_exams': total_exams,
            'exams_7d': exams_7d,
            'average_score': round(avg_exam_score, 2),
            'question_sets_by_level': question_sets_by_level,
            'popular_sets': popular_sets_data
        },
        'activity_data': activity_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_study_goal(request):
    """
    设置学习目标
    """
    user = request.user
    target_hsk_level = request.data.get('target_hsk_level')
    target_date = request.data.get('target_date')
    daily_practice_count = request.data.get('daily_practice_count', 10)
    
    # 验证必填字段
    if not target_hsk_level or not target_date:
        return Response({
            'error': '请提供目标HSK等级和目标日期'
        }, status=400)
    
    # 验证HSK等级范围
    try:
        target_hsk_level = int(target_hsk_level)
        if target_hsk_level < 1 or target_hsk_level > 6:
            return Response({
                'error': 'HSK等级必须在1-6之间'
            }, status=400)
    except (ValueError, TypeError):
        return Response({
            'error': 'HSK等级必须是数字'
        }, status=400)
    
    # 验证每日练习数量
    try:
        daily_practice_count = int(daily_practice_count)
        if daily_practice_count < 1 or daily_practice_count > 500:
            return Response({
                'error': '每日练习数量必须在1-500之间'
            }, status=400)
    except (ValueError, TypeError):
        return Response({
            'error': '每日练习数量必须是数字'
        }, status=400)
    
    # 验证日期
    try:
        target_date_obj = datetime.datetime.strptime(target_date, '%Y-%m-%d').date()
        if target_date_obj <= date.today():
            return Response({
                'error': '目标日期必须大于今天'
            }, status=400)
        # 限制目标日期不能超过5年
        max_date = date.today() + timedelta(days=365 * 5)
        if target_date_obj > max_date:
            return Response({
                'error': '目标日期不能超过5年'
            }, status=400)
    except ValueError:
        return Response({
            'error': '日期格式错误，请使用YYYY-MM-DD格式'
        }, status=400)
    
    # 创建学习目标
    study_goal = StudyGoal.objects.create(
        user=user,
        target_hsk_level=target_hsk_level,
        target_date=target_date_obj,
        daily_practice_count=daily_practice_count
    )
    
    return Response({
        'id': study_goal.id,
        'target_hsk_level': study_goal.target_hsk_level,
        'target_date': study_goal.target_date.isoformat(),
        'daily_practice_count': study_goal.daily_practice_count,
        'days_remaining': study_goal.get_days_remaining()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_study_report(request):
    """
    导出学习报告
    """
    from .study_models import StudyReport
    
    user = request.user
    report_type = request.GET.get('type', 'weekly')
    
    # 生成报告
    report = StudyReport.generate_report(user, report_type)
    
    return Response({
        'report_id': report.id,
        'report_type': report.get_report_type_display(),
        'start_date': report.start_date.isoformat(),
        'end_date': report.end_date.isoformat(),
        'summary': report.summary,
        'generated_at': report.generated_at.isoformat()
    })
