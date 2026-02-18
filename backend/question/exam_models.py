"""
考试相关模型
包含考试记录、考试报告等功能
"""

from django.db import models
from django.utils import timezone
from user.models import User
from .models import QuestionSet, Question, QuestionCategory
import json
import datetime


class ExamAttempt(models.Model):
    """考试记录模型"""
    STATUS_CHOICES = (
        ('in_progress', '进行中'),
        ('completed', '已完成'),
        ('abandoned', '已放弃'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, verbose_name='套卷')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='得分')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name='状态')
    answers = models.JSONField(default=dict, verbose_name='答案JSON')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '考试记录'
        verbose_name_plural = '考试记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.question_set.title} - {self.get_status_display()}"
    
    def get_duration(self):
        """获取考试时长（秒）"""
        if self.end_time:
            return int((self.end_time - self.start_time).total_seconds())
        return 0
    
    def get_duration_minutes(self):
        """获取考试时长（分钟）"""
        return self.get_duration() // 60
    
    def submit_answer(self, question_id, user_answer):
        """
        提交单题答案
        
        Args:
            question_id: 题目ID
            user_answer: 用户答案
            
        Raises:
            ValueError: 考试状态不正确或题目不属于该套卷
        """
        if self.status != 'in_progress':
            raise ValueError("考试已结束，无法提交答案")
        
        # 验证题目是否属于该套卷
        from .models import Question
        if not Question.objects.filter(
            id=question_id,
            question_set=self.question_set
        ).exists():
            raise ValueError("题目不属于该套卷")
        
        if not isinstance(self.answers, dict):
            self.answers = {}
        
        # 限制答案长度，防止恶意提交
        if isinstance(user_answer, str) and len(user_answer) > 10000:
            user_answer = user_answer[:10000]
        
        self.answers[str(question_id)] = {
            'answer': user_answer,
            'submitted_at': timezone.now().isoformat()
        }
        self.save(update_fields=['answers', 'updated_at'])
    
    def complete_exam(self):
        """
        完成考试
        
        该方法会：
        1. 标记考试为已完成
        2. 计算分数
        3. 生成考试报告
        4. 更新用户统计
        """
        if self.status != 'in_progress':
            return
        
        from django.db import transaction
        
        with transaction.atomic():
            self.end_time = timezone.now()
            self.status = 'completed'
            
            # 计算分数
            self.calculate_score()
            self.save(update_fields=['end_time', 'status', 'score', 'updated_at'])
            
            # 生成报告
            from .services.exam_service import ExamService
            ExamService.generate_report(self)
            
            # 更新用户统计（使用F表达式避免竞态条件）
            from django.db.models import F
            type(self.user).objects.filter(id=self.user.id).update(
                total_practice_count=F('total_practice_count') + len(self.answers)
            )
            self.user.refresh_from_db()
    
    def calculate_score(self):
        """计算分数"""
        if not self.answers:
            self.score = 0
            return
        
        questions = Question.objects.filter(
            question_set=self.question_set
        )
        
        correct_count = 0
        total_count = questions.count()
        
        for question in questions:
            user_answer = self.answers.get(str(question.id), {}).get('answer')
            if user_answer and self._check_answer(question, user_answer):
                correct_count += 1
        
        if total_count > 0:
            self.score = round(correct_count / total_count * 100, 2)
        else:
            self.score = 0
    
    def _check_answer(self, question, user_answer):
        """
        检查答案是否正确
        
        Args:
            question: 题目对象
            user_answer: 用户答案
            
        Returns:
            bool: 是否正确
        """
        if not user_answer:
            return False
        
        # 转换为字符串并标准化
        try:
            correct_answer = str(question.answer).strip().lower()
            user_answer_str = str(user_answer).strip().lower()
            
            # 基本的字符串比较
            if correct_answer == user_answer_str:
                return True
            
            # 移除标点符号后比较（可选）
            import re
            correct_cleaned = re.sub(r'[^\w\s]', '', correct_answer)
            user_cleaned = re.sub(r'[^\w\s]', '', user_answer_str)
            
            return correct_cleaned == user_cleaned
        except Exception:
            return False
    
    def abandon(self):
        """放弃考试"""
        self.status = 'abandoned'
        self.end_time = timezone.now()
        self.save()


class ExamReport(models.Model):
    """考试报告模型"""
    exam_attempt = models.OneToOneField(
        ExamAttempt,
        on_delete=models.CASCADE,
        verbose_name='考试记录'
    )
    total_questions = models.IntegerField(verbose_name='总题目数')
    correct_count = models.IntegerField(verbose_name='正确数量')
    accuracy_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='正确率')
    time_spent = models.IntegerField(verbose_name='用时(秒)')
    category_performance = models.JSONField(default=dict, verbose_name='分类表现')
    weak_points = models.JSONField(default=list, verbose_name='薄弱知识点')
    suggestions = models.TextField(blank=True, verbose_name='学习建议')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '考试报告'
        verbose_name_plural = '考试报告'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report - {self.exam_attempt.user.username} - {self.exam_attempt.question_set.title}"
    
    def generate_suggestions(self):
        """生成学习建议"""
        suggestions = []
        
        # 基于正确率的建议
        if self.accuracy_rate < 60:
            suggestions.append("建议系统学习HSK{}级的基础知识，加强练习。".format(
                self.exam_attempt.question_set.level
            ))
        elif self.accuracy_rate < 80:
            suggestions.append("已掌握大部分内容，建议针对薄弱环节进行专项练习。")
        else:
            suggestions.append("掌握情况良好！可以尝试更高级别的练习。")
        
        # 基于分类表现的建议
        if self.category_performance:
            weak_categories = [
                cat for cat, perf in self.category_performance.items()
                if perf.get('accuracy', 0) < 60
            ]
            if weak_categories:
                suggestions.append("建议加强以下题型的练习：{}".format(
                    "、".join(weak_categories)
                ))
        
        # 基于用时的建议
        time_limit = self.exam_attempt.question_set.time_limit * 60
        if self.time_spent > time_limit:
            suggestions.append("考试用时超过限制，建议加强做题速度训练。")
        
        self.suggestions = "\n".join(suggestions)
        self.save()


# PaperImport 和 AudioFile 模型已被删除
# 原因：
# 1. PaperImport - 只用于导入过程，可以用独立脚本处理，不需要数据库表
# 2. AudioFile - 音频信息已经整合到 Question 模型中（audio_url, audio_file, audio_duration）
# 
# 如需导入试卷，请使用 create_hsk_real_test_data.py 脚本


class ExamRanking(models.Model):
    """考试排行榜"""
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, verbose_name='套卷')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='分数')
    time_spent = models.IntegerField(verbose_name='用时(秒)')
    rank = models.IntegerField(verbose_name='排名')
    exam_attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        verbose_name='考试记录'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '考试排行榜'
        verbose_name_plural = '考试排行榜'
        unique_together = ['question_set', 'user']
        ordering = ['rank']
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}"
    
    @classmethod
    def update_rankings(cls, question_set):
        """更新排行榜"""
        # 获取该套卷的所有完成记录，按分数降序、用时升序排序
        attempts = ExamAttempt.objects.filter(
            question_set=question_set,
            status='completed'
        ).select_related('user').order_by('-score', 'end_time')
        
        # 更新或创建排行榜记录
        for index, attempt in enumerate(attempts, start=1):
            cls.objects.update_or_create(
                question_set=question_set,
                user=attempt.user,
                defaults={
                    'score': attempt.score,
                    'time_spent': attempt.get_duration(),
                    'rank': index,
                    'exam_attempt': attempt
                }
            )
