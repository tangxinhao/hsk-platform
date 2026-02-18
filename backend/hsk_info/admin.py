from django.contrib import admin
from django.utils.html import format_html
from .models import HSKLevel, ExamOutline, StudyGuide, FAQ


@admin.register(HSKLevel)
class HSKLevelAdmin(admin.ModelAdmin):
    """HSK等级管理"""
    list_display = ['level_badge', 'name', 'vocabulary_count', 'exam_duration',
                    'passing_score_display', 'target_audience_preview', 'updated_at']
    list_filter = ['level']
    search_fields = ['name', 'description', 'target_audience']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('level', 'name', 'description', 'icon', 'color')
        }),
        ('能力要求', {
            'fields': ('vocabulary_count', 'listening_ability', 'reading_ability', 'writing_ability')
        }),
        ('考试信息', {
            'fields': ('exam_duration', 'total_score', 'passing_score', 'exam_structure'),
            'description': 'exam_structure格式: [{"part": "听力", "questions": 45, "time": 35}, ...]'
        }),
        ('学习建议', {
            'fields': ('target_audience', 'study_hours')
        }),
    )
    
    def level_badge(self, obj):
        """等级徽章"""
        colors = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#52c41a', '#1890ff']
        color = colors[obj.level - 1] if obj.level <= 6 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 8px 15px; '
            'border-radius: 50%; font-weight: bold; font-size: 14px;">HSK {}</span>',
            color, obj.level
        )
    level_badge.short_description = '等级'
    
    def passing_score_display(self, obj):
        """及格分数显示"""
        percentage = (obj.passing_score / obj.total_score * 100)
        return format_html(
            '<span style="font-weight: bold;">{}/{}</span> ({:.0f}%)',
            obj.passing_score, obj.total_score, percentage
        )
    passing_score_display.short_description = '及格分'
    
    def target_audience_preview(self, obj):
        """适用人群预览"""
        preview = obj.target_audience[:30] + '...' if len(obj.target_audience) > 30 else obj.target_audience
        return format_html('<span title="{}">{}</span>', obj.target_audience, preview)
    target_audience_preview.short_description = '适用人群'


@admin.register(ExamOutline)
class ExamOutlineAdmin(admin.ModelAdmin):
    """考试大纲管理"""
    list_display = ['hsk_level', 'section_badge', 'part_number', 'title',
                    'question_count', 'time_limit', 'order']
    list_filter = ['hsk_level', 'section']
    search_fields = ['title', 'description']
    list_editable = ['order']
    ordering = ['hsk_level', 'order', 'part_number']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('hsk_level', 'section', 'part_number', 'title', 'order')
        }),
        ('考试详情', {
            'fields': ('description', 'question_count', 'time_limit', 'question_types', 'scoring_method')
        }),
        ('答题技巧', {
            'fields': ('tips',),
            'classes': ('collapse',)
        }),
    )
    
    def section_badge(self, obj):
        """考试部分徽章"""
        section_colors = {
            '听力': '#722ed1',
            '阅读': '#1890ff',
            '写作': '#52c41a'
        }
        color = section_colors.get(obj.section, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 10px; '
            'border-radius: 4px; font-weight: bold;">{}</span>',
            color, obj.section
        )
    section_badge.short_description = '考试部分'


@admin.register(StudyGuide)
class StudyGuideAdmin(admin.ModelAdmin):
    """学习指南管理"""
    list_display = ['hsk_level', 'title', 'category_badge', 'is_featured', 'order', 'updated_at']
    list_filter = ['hsk_level', 'category', 'is_featured']
    search_fields = ['title', 'content']
    list_editable = ['is_featured', 'order']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('hsk_level', 'title', 'category', 'order', 'is_featured')
        }),
        ('指南内容', {
            'fields': ('content', 'tips')
        }),
        ('相关资源', {
            'fields': ('resources',),
            'classes': ('collapse',),
            'description': 'JSON格式: [{"name": "资源名称", "url": "链接"}]'
        }),
    )
    
    def category_badge(self, obj):
        """分类徽章"""
        category_colors = {
            'preparation': '#faad14',
            'vocabulary': '#1890ff',
            'grammar': '#52c41a',
            'listening': '#722ed1',
            'reading': '#fa8c16',
            'writing': '#13c2c2',
            'exam_tips': '#f5222d',
            'resources': '#eb2f96'
        }
        color = category_colors.get(obj.category, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{}</span>',
            color, obj.get_category_display()
        )
    category_badge.short_description = '分类'


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """常见问题管理"""
    list_display = ['question_preview', 'category_badge', 'view_count', 'is_featured', 'order', 'updated_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['is_featured', 'order']
    ordering = ['-is_featured', 'order', '-view_count']
    
    fieldsets = (
        ('问题信息', {
            'fields': ('category', 'question', 'order', 'is_featured')
        }),
        ('答案', {
            'fields': ('answer',)
        }),
        ('相关链接', {
            'fields': ('related_links',),
            'classes': ('collapse',)
        }),
        ('统计', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        """问题预览"""
        preview = obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
        return format_html('<span title="{}">{}</span>', obj.question, preview)
    question_preview.short_description = '问题'
    
    def category_badge(self, obj):
        """分类徽章"""
        category_colors = {
            'exam_info': '#1890ff',
            'registration': '#52c41a',
            'preparation': '#faad14',
            'certificate': '#722ed1',
            'other': '#d9d9d9'
        }
        color = category_colors.get(obj.category, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{}</span>',
            color, obj.get_category_display()
        )
    category_badge.short_description = '分类'
