"""
考试服务类
处理考试相关的业务逻辑
"""

import datetime
from collections import defaultdict
from django.db.models import Count, Avg, Q
from django.utils import timezone
from ..models import Question, QuestionCategory
from ..exam_models import ExamAttempt, ExamReport, ExamRanking


class ExamService:
    """考试服务类"""
    
    @staticmethod
    def start_exam(user, question_set):
        """
        开始考试
        
        Args:
            user: 用户对象
            question_set: 套卷对象
        
        Returns:
            ExamAttempt: 考试记录对象
            
        Raises:
            ValueError: 套卷无效或题目数量为0
        """
        # 验证套卷是否有效
        if not question_set:
            raise ValueError("套卷不存在")
        
        # 验证套卷是否有题目
        question_count = Question.objects.filter(question_set=question_set).count()
        if question_count == 0:
            raise ValueError("该套卷没有题目")
        
        # 检查是否有未完成的考试
        existing = ExamAttempt.objects.filter(
            user=user,
            question_set=question_set,
            status='in_progress'
        ).first()
        
        if existing:
            # 检查考试是否超时（超过时间限制的2倍自动放弃）
            if existing.start_time:
                time_elapsed = (timezone.now() - existing.start_time).total_seconds() / 60
                time_limit = question_set.time_limit * 2
                if time_elapsed > time_limit:
                    existing.abandon()
                else:
                    return existing
        
        # 创建新的考试记录
        exam_attempt = ExamAttempt.objects.create(
            user=user,
            question_set=question_set,
            status='in_progress'
        )
        
        return exam_attempt
    
    @staticmethod
    def submit_exam(exam_attempt):
        """
        提交考试
        
        Args:
            exam_attempt: 考试记录对象
        """
        if exam_attempt.status != 'in_progress':
            raise ValueError("考试已结束")
        
        exam_attempt.complete_exam()
        
        # 更新排行榜
        ExamRanking.update_rankings(exam_attempt.question_set)
        
        return exam_attempt
    
    @staticmethod
    def generate_report(exam_attempt):
        """
        生成考试报告
        
        Args:
            exam_attempt: 考试记录对象
        
        Returns:
            ExamReport: 考试报告对象
        """
        # 如果已存在报告，先删除
        ExamReport.objects.filter(exam_attempt=exam_attempt).delete()
        
        # 获取所有题目
        questions = Question.objects.filter(
            question_set=exam_attempt.question_set
        ).select_related('category')
        
        total_questions = questions.count()
        correct_count = 0
        
        # 分类表现统计
        category_stats = defaultdict(lambda: {'total': 0, 'correct': 0})
        
        # 薄弱知识点
        weak_questions = []
        
        for question in questions:
            user_answer = exam_attempt.answers.get(str(question.id), {}).get('answer')
            is_correct = ExamService._check_answer(question, user_answer)
            
            if is_correct:
                correct_count += 1
            else:
                weak_questions.append({
                    'question_id': question.id,
                    'content': question.content[:50],
                    'category': question.category.get_name_display() if question.category else '未分类',
                    'difficulty': question.difficulty
                })
            
            # 更新分类统计
            category_name = question.category.get_name_display() if question.category else '未分类'
            category_stats[category_name]['total'] += 1
            if is_correct:
                category_stats[category_name]['correct'] += 1
        
        # 计算正确率
        accuracy_rate = round(correct_count / total_questions * 100, 2) if total_questions > 0 else 0
        
        # 处理分类表现数据
        category_performance = {}
        for category, stats in category_stats.items():
            category_performance[category] = {
                'total': stats['total'],
                'correct': stats['correct'],
                'accuracy': round(stats['correct'] / stats['total'] * 100, 2) if stats['total'] > 0 else 0
            }
        
        # 创建报告
        report = ExamReport.objects.create(
            exam_attempt=exam_attempt,
            total_questions=total_questions,
            correct_count=correct_count,
            accuracy_rate=accuracy_rate,
            time_spent=exam_attempt.get_duration(),
            category_performance=category_performance,
            weak_points=weak_questions[:10]  # 只保留前10个薄弱点
        )
        
        # 生成学习建议
        report.generate_suggestions()
        
        return report
    
    @staticmethod
    def _check_answer(question, user_answer):
        """
        检查答案是否正确
        
        Args:
            question: 题目对象
            user_answer: 用户答案
        
        Returns:
            bool: 是否正确
        """
        if not user_answer or not question or not question.answer:
            return False
        
        try:
            # 标准化答案
            correct_answer = str(question.answer).strip().lower()
            user_answer_str = str(user_answer).strip().lower()
            
            # 直接比较
            if correct_answer == user_answer_str:
                return True
            
            # 移除多余空格后比较
            correct_normalized = ' '.join(correct_answer.split())
            user_normalized = ' '.join(user_answer_str.split())
            
            return correct_normalized == user_normalized
        except Exception:
            return False
    
    @staticmethod
    def get_user_exam_history(user, question_set=None, limit=10):
        """
        获取用户考试历史
        
        Args:
            user: 用户对象
            question_set: 可选的套卷对象
            limit: 返回数量限制
        
        Returns:
            QuerySet: 考试记录列表
        """
        # 验证limit参数
        try:
            limit = int(limit)
            if limit < 1:
                limit = 10
            elif limit > 100:  # 限制最大返回数量
                limit = 100
        except (ValueError, TypeError):
            limit = 10
        
        queryset = ExamAttempt.objects.filter(user=user)
        
        if question_set:
            queryset = queryset.filter(question_set=question_set)
        
        return queryset.select_related('question_set').order_by('-created_at')[:limit]
    
    @staticmethod
    def get_exam_statistics(user):
        """
        获取用户考试统计
        
        Args:
            user: 用户对象
        
        Returns:
            dict: 统计数据
        """
        attempts = ExamAttempt.objects.filter(
            user=user,
            status='completed'
        )
        
        total_exams = attempts.count()
        
        if total_exams == 0:
            return {
                'total_exams': 0,
                'average_score': 0,
                'highest_score': 0,
                'total_time': 0,
                'by_level': {}
            }
        
        # 基础统计
        stats = attempts.aggregate(
            avg_score=Avg('score'),
            total_time=Count('id')
        )
        
        # 按等级统计
        by_level = {}
        for level in range(1, 7):
            level_attempts = attempts.filter(question_set__level=level)
            if level_attempts.exists():
                by_level[f'HSK{level}'] = {
                    'count': level_attempts.count(),
                    'avg_score': round(level_attempts.aggregate(
                        avg=Avg('score')
                    )['avg'] or 0, 2)
                }
        
        return {
            'total_exams': total_exams,
            'average_score': round(stats['avg_score'] or 0, 2),
            'highest_score': round(attempts.order_by('-score').first().score, 2),
            'total_time': sum(a.get_duration() for a in attempts) // 60,  # 分钟
            'by_level': by_level
        }
    
    @staticmethod
    def get_question_set_statistics(question_set):
        """
        获取套卷统计数据
        
        Args:
            question_set: 套卷对象
        
        Returns:
            dict: 统计数据
        """
        attempts = ExamAttempt.objects.filter(
            question_set=question_set,
            status='completed'
        )
        
        total_attempts = attempts.count()
        
        if total_attempts == 0:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'pass_rate': 0,
                'average_time': 0
            }
        
        # 统计
        stats = attempts.aggregate(
            avg_score=Avg('score')
        )
        
        # 及格率（假设60分及格）
        passed = attempts.filter(score__gte=60).count()
        pass_rate = round(passed / total_attempts * 100, 2)
        
        # 平均用时
        total_time = sum(a.get_duration() for a in attempts)
        avg_time = total_time // total_attempts if total_attempts > 0 else 0
        
        return {
            'total_attempts': total_attempts,
            'average_score': round(stats['avg_score'] or 0, 2),
            'pass_rate': pass_rate,
            'average_time': avg_time // 60,  # 分钟
            'highest_score': round(attempts.order_by('-score').first().score, 2)
        }
    
    @staticmethod
    def get_leaderboard(question_set, limit=10):
        """
        获取排行榜
        
        Args:
            question_set: 套卷对象
            limit: 返回数量
        
        Returns:
            QuerySet: 排行榜列表
        """
        return ExamRanking.objects.filter(
            question_set=question_set
        ).select_related('user', 'exam_attempt').order_by('rank')[:limit]
    
    @staticmethod
    def analyze_weak_points(user, hsk_level=None):
        """
        分析用户薄弱点
        
        Args:
            user: 用户对象
            hsk_level: 可选的HSK等级过滤
        
        Returns:
            list: 薄弱点列表
        """
        # 获取用户的考试报告
        reports_query = ExamReport.objects.filter(
            exam_attempt__user=user
        )
        
        if hsk_level:
            reports_query = reports_query.filter(
                exam_attempt__question_set__level=hsk_level
            )
        
        reports = reports_query.order_by('-created_at')[:5]  # 最近5次
        
        # 统计薄弱知识点
        weak_points_counter = defaultdict(int)
        
        for report in reports:
            if report.weak_points:
                for point in report.weak_points:
                    category = point.get('category', '未分类')
                    weak_points_counter[category] += 1
        
        # 排序
        weak_points = [
            {'category': cat, 'count': count}
            for cat, count in weak_points_counter.items()
        ]
        weak_points.sort(key=lambda x: x['count'], reverse=True)
        
        return weak_points[:5]  # 返回前5个
