"""
用户学习相关模型
包含学习目标、学习统计等功能
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import datetime

# 使用settings.AUTH_USER_MODEL来避免循环导入
User = settings.AUTH_USER_MODEL


class StudyGoal(models.Model):
    """学习目标模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    target_hsk_level = models.IntegerField(
        verbose_name='目标HSK等级',
        validators=[
            MinValueValidator(1, message='HSK等级最小为1'),
            MaxValueValidator(6, message='HSK等级最大为6')
        ]
    )
    target_date = models.DateField(verbose_name='目标日期')
    daily_practice_count = models.IntegerField(
        default=10,
        verbose_name='每日练习目标',
        validators=[
            MinValueValidator(1, message='每日练习目标最小为1'),
            MaxValueValidator(500, message='每日练习目标最大为500')
        ]
    )
    current_progress = models.IntegerField(
        default=0,
        verbose_name='当前进度',
        validators=[
            MinValueValidator(0, message='进度不能为负数'),
            MaxValueValidator(100, message='进度不能大于100')
        ]
    )
    is_completed = models.BooleanField(default=False, verbose_name='是否完成')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '学习目标'
        verbose_name_plural = '学习目标'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - HSK{self.target_hsk_level} - {self.target_date}"
    
    def get_days_remaining(self):
        """获取剩余天数"""
        today = datetime.date.today()
        delta = self.target_date - today
        return max(0, delta.days)
    
    def get_progress_percentage(self):
        """获取进度百分比"""
        if self.daily_practice_count <= 0:
            return 0
        
        days_total = (self.target_date - self.created_at.date()).days
        days_passed = (datetime.date.today() - self.created_at.date()).days
        
        if days_total <= 0:
            return 100
        
        expected_progress = days_passed * self.daily_practice_count
        if expected_progress <= 0:
            return 0
        
        return min(100, round(self.current_progress / expected_progress * 100, 2))
    
    def update_progress(self, count=1):
        """更新进度"""
        self.current_progress += count
        
        # 检查是否完成
        total_required = (self.target_date - self.created_at.date()).days * self.daily_practice_count
        if self.current_progress >= total_required:
            self.is_completed = True
        
        self.save()


class StudyStatistics(models.Model):
    """学习统计模型（按日期聚合）"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    date = models.DateField(verbose_name='统计日期')
    practice_count = models.IntegerField(default=0, verbose_name='练习次数')
    correct_count = models.IntegerField(default=0, verbose_name='正确次数')
    study_time = models.IntegerField(default=0, verbose_name='学习时长(分钟)')
    points_earned = models.IntegerField(default=0, verbose_name='获得积分')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '学习统计'
        verbose_name_plural = '学习统计'
        unique_together = ['user', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    def get_accuracy_rate(self):
        """获取正确率"""
        if self.practice_count == 0:
            return 0
        # 防止除零错误和确保数据有效性
        try:
            rate = (self.correct_count / self.practice_count) * 100
            return round(min(100, max(0, rate)), 2)
        except (ZeroDivisionError, TypeError):
            return 0
    
    @classmethod
    def record_practice(cls, user, is_correct=False, study_time=0, points=0):
        """
        记录一次练习
        
        Args:
            user: 用户对象
            is_correct: 是否正确
            study_time: 学习时长（分钟）
            points: 获得积分
        """
        # 数据验证
        study_time = max(0, int(study_time or 0))
        points = max(0, int(points or 0))
        
        # 防止异常数据
        if study_time > 1440:  # 一天最多1440分钟
            study_time = 1440
        if points > 10000:  # 单次积分上限
            points = 10000
        
        today = datetime.date.today()
        
        # 使用事务确保数据一致性
        from django.db import transaction
        
        with transaction.atomic():
            stats, created = cls.objects.select_for_update().get_or_create(
                user=user,
                date=today,
                defaults={
                    'practice_count': 0,
                    'correct_count': 0,
                    'study_time': 0,
                    'points_earned': 0
                }
            )
            
            stats.practice_count += 1
            if is_correct:
                stats.correct_count += 1
            stats.study_time += study_time
            stats.points_earned += points
            stats.save()
        
        return stats
    
    @classmethod
    def get_user_trend(cls, user, days=7):
        """获取用户最近N天的学习趋势"""
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days-1)
        
        statistics = cls.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')
        
        # 填充缺失的日期
        result = []
        current_date = start_date
        stats_dict = {stat.date: stat for stat in statistics}
        
        while current_date <= end_date:
            if current_date in stats_dict:
                result.append(stats_dict[current_date])
            else:
                # 创建空记录
                result.append({
                    'date': current_date,
                    'practice_count': 0,
                    'correct_count': 0,
                    'study_time': 0,
                    'points_earned': 0
                })
            current_date += datetime.timedelta(days=1)
        
        return result


class StudySession(models.Model):
    """学习会话记录"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    duration = models.IntegerField(default=0, verbose_name='持续时间(秒)')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('practice', '练习'),
            ('exam', '考试'),
            ('culture', '文化学习'),
            ('university', '院校浏览')
        ],
        verbose_name='活动类型'
    )
    activity_id = models.IntegerField(null=True, verbose_name='活动ID')
    
    class Meta:
        verbose_name = '学习会话'
        verbose_name_plural = '学习会话'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()} - {self.start_time}"
    
    def end_session(self):
        """结束会话"""
        if not self.end_time:
            self.end_time = datetime.datetime.now()
            self.duration = int((self.end_time - self.start_time).total_seconds())
            self.save()
            
            # 更新统计
            study_minutes = self.duration // 60
            if study_minutes > 0:
                StudyStatistics.record_practice(
                    self.user,
                    study_time=study_minutes
                )


class AchievementBadge(models.Model):
    """成就徽章"""
    code = models.CharField(max_length=50, unique=True, verbose_name='徽章代码')
    name = models.CharField(max_length=100, verbose_name='徽章名称')
    description = models.TextField(verbose_name='描述')
    icon_url = models.URLField(max_length=500, blank=True, verbose_name='图标URL')
    requirement = models.JSONField(verbose_name='获取条件')
    points = models.IntegerField(default=0, verbose_name='奖励积分')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '成就徽章'
        verbose_name_plural = '成就徽章'
        ordering = ['code']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """用户成就"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    badge = models.ForeignKey(AchievementBadge, on_delete=models.CASCADE, verbose_name='徽章')
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name='获得时间')
    
    class Meta:
        verbose_name = '用户成就'
        verbose_name_plural = '用户成就'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class StudyReport(models.Model):
    """学习报告"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    report_type = models.CharField(
        max_length=20,
        choices=[
            ('daily', '日报'),
            ('weekly', '周报'),
            ('monthly', '月报'),
            ('custom', '自定义')
        ],
        verbose_name='报告类型'
    )
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    summary = models.JSONField(verbose_name='统计摘要')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')
    
    class Meta:
        verbose_name = '学习报告'
        verbose_name_plural = '学习报告'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_report_type_display()} - {self.start_date} to {self.end_date}"
    
    @classmethod
    def generate_report(cls, user, report_type='weekly', start_date=None, end_date=None):
        """生成学习报告"""
        if not end_date:
            end_date = datetime.date.today()
        
        if not start_date:
            if report_type == 'daily':
                start_date = end_date
            elif report_type == 'weekly':
                start_date = end_date - datetime.timedelta(days=6)
            elif report_type == 'monthly':
                start_date = end_date - datetime.timedelta(days=29)
        
        # 获取统计数据
        statistics = StudyStatistics.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        )
        
        # 计算汇总数据
        total_practice = sum(s.practice_count for s in statistics)
        total_correct = sum(s.correct_count for s in statistics)
        total_time = sum(s.study_time for s in statistics)
        total_points = sum(s.points_earned for s in statistics)
        
        accuracy_rate = round(total_correct / total_practice * 100, 2) if total_practice > 0 else 0
        
        summary = {
            'total_practice_count': total_practice,
            'total_correct_count': total_correct,
            'total_study_time': total_time,
            'total_points': total_points,
            'accuracy_rate': accuracy_rate,
            'study_days': statistics.count(),
            'average_daily_practice': round(total_practice / max(1, statistics.count()), 2),
            'average_daily_time': round(total_time / max(1, statistics.count()), 2)
        }
        
        report = cls.objects.create(
            user=user,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            summary=summary
        )
        
        return report
