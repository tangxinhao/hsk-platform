from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class User(AbstractUser):
    # 基础信息
    hsk_level = models.IntegerField(default=1, verbose_name='HSK水平')
    nationality = models.CharField(max_length=100, blank=True, verbose_name='国籍')
    chinese_name = models.CharField(max_length=50, blank=True, verbose_name='中文名')
    english_name = models.CharField(max_length=50, blank=True, verbose_name='英文名')
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    avatar = models.URLField(max_length=500, blank=True, null=True, verbose_name='头像URL')
    
    # 学习统计
    total_practice_count = models.IntegerField(default=0, verbose_name='总练习次数')
    total_correct_count = models.IntegerField(default=0, verbose_name='总正确次数')
    total_score = models.IntegerField(default=0, verbose_name='总得分')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.chinese_name or self.english_name or self.username})"
    
    def get_accuracy_rate(self):
        """计算正确率"""
        if self.total_practice_count == 0:
            return 0
        return round(self.total_correct_count / self.total_practice_count * 100, 2)
    
    def get_average_score(self):
        """计算平均分"""
        if self.total_practice_count == 0:
            return 0
        return round(self.total_score / self.total_practice_count, 2)
