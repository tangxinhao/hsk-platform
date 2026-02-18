from django.contrib import admin
from django.utils.html import format_html
from .models import University


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """大学信息管理"""
    list_display = ['id', 'name', 'city_badge', 'ranking_display', 'hsk_requirement',
                    'student_count', 'tuition_display', 'created_at']
    list_filter = ['city', 'min_hsk_level', 'region', 'created_at']
    search_fields = ['name', 'english_name', 'city', 'description']
    list_per_page = 30
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'english_name', 'region', 'city')
        }),
        ('排名信息', {
            'fields': ('ranking', 'ranking_national', 'ranking_world')
        }),
        ('学校简介', {
            'fields': ('description', 'history', 'features')
        }),
        ('入学条件', {
            'fields': ('min_hsk_level', 'language_requirements', 'tuition_fee', 'scholarship'),
            'description': 'HSK要求、语言要求、学费和奖学金信息'
        }),
        ('联系方式', {
            'fields': ('website', 'email', 'phone', 'address'),
            'classes': ('collapse',)
        }),
        ('图片资源', {
            'fields': ('logo_url', 'campus_image_url'),
            'classes': ('collapse',)
        }),
        ('专业信息', {
            'fields': ('majors', 'popular_majors'),
            'classes': ('collapse',),
            'description': 'JSON格式：["专业1", "专业2", ...]'
        }),
        ('统计信息', {
            'fields': ('international_students', 'total_students', 'tags'),
            'classes': ('collapse',)
        }),
    )
    
    def city_badge(self, obj):
        """城市徽章"""
        # 一线城市用红色，二线用橙色，其他用蓝色
        first_tier = ['北京', '上海', '广州', '深圳']
        second_tier = ['杭州', '成都', '重庆', '武汉', '西安', '南京', '天津', '苏州']
        
        if obj.city in first_tier:
            color = '#f5222d'
            icon = '🔥'
        elif obj.city in second_tier:
            color = '#fa8c16'
            icon = '⭐'
        else:
            color = '#1890ff'
            icon = '📍'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 10px; '
            'border-radius: 4px;">{} {}</span>',
            color, icon, obj.city
        )
    city_badge.short_description = '城市'
    
    def ranking_display(self, obj):
        """排名显示"""
        parts = []
        if obj.ranking:
            parts.append(f'综合: {obj.ranking}名')
        if obj.ranking_national:
            parts.append(f'国内: {obj.ranking_national}名')
        if obj.ranking_world:
            parts.append(f'世界: {obj.ranking_world}名')
        
        if parts:
            return format_html('<span>{}</span>', ' | '.join(parts))
        return '-'
    ranking_display.short_description = '排名'
    
    def hsk_requirement(self, obj):
        """HSK要求徽章"""
        colors = ['#52c41a', '#52c41a', '#faad14', '#fa8c16', '#f5222d', '#722ed1']
        color = colors[obj.min_hsk_level - 1] if obj.min_hsk_level <= 6 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 50%; font-weight: bold;">HSK{}</span>',
            color, obj.min_hsk_level
        )
    hsk_requirement.short_description = 'HSK要求'
    
    def student_count(self, obj):
        """学生数量"""
        if obj.total_students > 0:
            international_percentage = (obj.international_students / obj.total_students * 100) if obj.total_students > 0 else 0
            return format_html(
                '<div>总数: {}<br/>留学生: {} ({:.1f}%)</div>',
                obj.total_students, obj.international_students, international_percentage
            )
        return '-'
    student_count.short_description = '学生数'
    
    def tuition_display(self, obj):
        """学费显示"""
        if obj.tuition_fee:
            # 将学费格式化为千分位
            tuition_str = '{:,.0f}'.format(obj.tuition_fee)
            return format_html('<span style="font-weight: bold; color: #fa8c16;">¥{}/年</span>', tuition_str)
        return '-'
    tuition_display.short_description = '学费'
    
    def save_model(self, request, obj, form, change):
        """保存时计算匹配分数等"""
        super().save_model(request, obj, form, change)
        # 这里可以添加额外的保存逻辑，如自动计算某些字段 