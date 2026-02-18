from django.contrib import admin
from django.utils.html import format_html
from .models import User
from .study_models import (
    StudyGoal, StudyStatistics, StudySession, 
    AchievementBadge, UserAchievement, StudyReport
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """用户管理"""
    list_display = ['id', 'username', 'chinese_name', 'english_name', 'hsk_level_badge',
                    'accuracy_display', 'practice_count', 'is_staff', 'date_joined']
    list_filter = ['hsk_level', 'nationality', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'chinese_name', 'english_name', 'phone']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        ('账号信息', {
            'fields': ('username', 'email', 'password')
        }),
        ('个人信息', {
            'fields': ('chinese_name', 'english_name', 'nationality', 'phone', 'avatar')
        }),
        ('学习信息', {
            'fields': ('hsk_level', 'total_practice_count', 'total_correct_count', 'total_score')
        }),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('重要日期', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    def hsk_level_badge(self, obj):
        """HSK等级徽章"""
        colors = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#52c41a', '#1890ff']
        color = colors[obj.hsk_level - 1] if obj.hsk_level <= 6 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 50%; font-weight: bold;">HSK{}</span>',
            color, obj.hsk_level
        )
    hsk_level_badge.short_description = 'HSK等级'
    
    def accuracy_display(self, obj):
        """正确率显示"""
        rate = obj.get_accuracy_rate()
        color = '#52c41a' if rate >= 80 else '#faad14' if rate >= 60 else '#f5222d'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, rate
        )
    accuracy_display.short_description = '正确率'
    
    def practice_count(self, obj):
        """练习次数"""
        return format_html('<span style="font-weight: bold;">{}</span>题', obj.total_practice_count)
    practice_count.short_description = '练习次数'


@admin.register(StudyGoal)
class StudyGoalAdmin(admin.ModelAdmin):
    """学习目标管理"""
    list_display = ['user', 'target_hsk_level_badge', 'target_date', 'progress_bar',
                    'daily_practice_count', 'days_remaining_display', 'is_completed']
    list_filter = ['target_hsk_level', 'is_completed', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('目标设置', {
            'fields': ('user', 'target_hsk_level', 'target_date', 'daily_practice_count')
        }),
        ('进度追踪', {
            'fields': ('current_progress', 'is_completed')
        }),
    )
    
    def target_hsk_level_badge(self, obj):
        """目标等级徽章"""
        colors = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#52c41a', '#1890ff']
        color = colors[obj.target_hsk_level - 1] if obj.target_hsk_level <= 6 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 50%; font-weight: bold;">HSK{}</span>',
            color, obj.target_hsk_level
        )
    target_hsk_level_badge.short_description = '目标等级'
    
    def progress_bar(self, obj):
        """进度条"""
        percentage = obj.get_progress_percentage()
        color = '#52c41a' if percentage >= 80 else '#faad14' if percentage >= 50 else '#f5222d'
        return format_html(
            '<div style="width: 120px; background: #f0f0f0; border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; height: 20px; border-radius: 10px; '
            'text-align: center; color: white; font-size: 12px; line-height: 20px;">{:.0f}%</div>'
            '</div>',
            percentage, color, percentage
        )
    progress_bar.short_description = '完成进度'
    
    def days_remaining_display(self, obj):
        """剩余天数"""
        days = obj.get_days_remaining()
        if days == 0:
            return format_html('<span style="color: #f5222d; font-weight: bold;">今天到期!</span>')
        elif days < 7:
            return format_html('<span style="color: #fa8c16; font-weight: bold;">剩余{}天</span>', days)
        return format_html('<span>剩余{}天</span>', days)
    days_remaining_display.short_description = '剩余天数'


@admin.register(StudyStatistics)
class StudyStatisticsAdmin(admin.ModelAdmin):
    """学习统计管理"""
    list_display = ['user', 'date', 'practice_count', 'correct_count', 'accuracy_display',
                    'study_time_display', 'points_earned']
    list_filter = ['date', 'user']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    def accuracy_display(self, obj):
        """正确率"""
        rate = obj.get_accuracy_rate()
        color = '#52c41a' if rate >= 80 else '#faad14' if rate >= 60 else '#f5222d'
        return format_html('<span style="color: {}; font-weight: bold;">{:.1f}%</span>', color, rate)
    accuracy_display.short_description = '正确率'
    
    def study_time_display(self, obj):
        """学习时长"""
        return format_html('<span>{}</span>分钟', obj.study_time)
    study_time_display.short_description = '学习时长'


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    """学习会话管理"""
    list_display = ['user', 'activity_type_badge', 'start_time', 'duration_display', 'activity_id']
    list_filter = ['activity_type', 'start_time']
    search_fields = ['user__username']
    readonly_fields = ['start_time']
    
    def activity_type_badge(self, obj):
        """活动类型徽章"""
        type_colors = {
            'practice': '#1890ff',
            'exam': '#f5222d',
            'culture': '#52c41a',
            'university': '#722ed1'
        }
        color = type_colors.get(obj.activity_type, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{}</span>',
            color, obj.get_activity_type_display()
        )
    activity_type_badge.short_description = '活动类型'
    
    def duration_display(self, obj):
        """时长显示"""
        if obj.duration > 0:
            minutes = obj.duration // 60
            seconds = obj.duration % 60
            return format_html('<span>{}分{}秒</span>', minutes, seconds)
        return '-'
    duration_display.short_description = '时长'


@admin.register(AchievementBadge)
class AchievementBadgeAdmin(admin.ModelAdmin):
    """成就徽章管理"""
    list_display = ['code', 'name', 'description_preview', 'points', 'created_at']
    search_fields = ['code', 'name', 'description']
    
    fieldsets = (
        ('徽章信息', {
            'fields': ('code', 'name', 'description', 'icon_url')
        }),
        ('获取条件', {
            'fields': ('requirement', 'points'),
            'description': 'requirement格式：{"type": "practice_count", "value": 100}'
        }),
    )
    
    def description_preview(self, obj):
        """描述预览"""
        preview = obj.description[:40] + '...' if len(obj.description) > 40 else obj.description
        return format_html('<span title="{}">{}</span>', obj.description, preview)
    description_preview.short_description = '描述'


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """用户成就管理"""
    list_display = ['user', 'badge_name', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']
    readonly_fields = ['earned_at']
    
    def badge_name(self, obj):
        """徽章名称"""
        return obj.badge.name
    badge_name.short_description = '徽章'


@admin.register(StudyReport)
class StudyReportAdmin(admin.ModelAdmin):
    """学习报告管理"""
    list_display = ['user', 'report_type_badge', 'date_range', 'summary_preview', 'generated_at']
    list_filter = ['report_type', 'generated_at']
    search_fields = ['user__username']
    readonly_fields = ['generated_at']
    
    def report_type_badge(self, obj):
        """报告类型徽章"""
        type_colors = {
            'daily': '#52c41a',
            'weekly': '#1890ff',
            'monthly': '#722ed1',
            'custom': '#faad14'
        }
        color = type_colors.get(obj.report_type, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{}</span>',
            color, obj.get_report_type_display()
        )
    report_type_badge.short_description = '报告类型'
    
    def date_range(self, obj):
        """日期范围"""
        return format_html('<span>{} 至 {}</span>', obj.start_date, obj.end_date)
    date_range.short_description = '日期范围'
    
    def summary_preview(self, obj):
        """摘要预览"""
        if obj.summary:
            practice_count = obj.summary.get('total_practice_count', 0)
            accuracy = obj.summary.get('accuracy_rate', 0)
            return format_html(
                '<span>练习{}题 | 正确率{:.1f}%</span>',
                practice_count, accuracy
            )
        return '-'
    summary_preview.short_description = '摘要' 