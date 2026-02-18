from django.contrib import admin
from django.utils.html import format_html
from .models import Question, AnswerRecord, WrongBook, QuestionSet, QuestionCategory, Material


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    """题目分类管理"""
    list_display = ['id', 'name_display', 'parent_category', 'order', 'level_range_display', 
                    'is_active', 'question_count_display', 'created_at']
    list_filter = ['is_active', 'parent_category', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'id']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'description', 'parent_category')
        }),
        ('显示设置', {
            'fields': ('icon', 'color', 'order', 'is_active')
        }),
        ('等级范围', {
            'fields': ('level_range',),
            'description': '示例: {"min": 1, "max": 6}'
        }),
    )
    
    def name_display(self, obj):
        """显示分类名称"""
        return obj.get_name_display()
    name_display.short_description = '分类名称'
    
    def level_range_display(self, obj):
        """显示等级范围"""
        return obj.get_level_range_display()
    level_range_display.short_description = '适用等级'
    
    def question_count_display(self, obj):
        """显示题目数量"""
        count = obj.get_question_count()
        return format_html('<span style="font-weight: bold; color: #1890ff;">{}</span>', count)
    question_count_display.short_description = '题目数'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """题目管理 - 支持多种题型"""
    list_display = ['id', 'type_display', 'level_badge', 'content_preview', 'category_display',
                    'question_set', 'difficulty_stars', 'media_badge', 'points', 'created_at']
    list_filter = ['type', 'level', 'difficulty', 'category', 'question_set', 'created_at']
    search_fields = ['content', 'answer', 'explanation']
    list_per_page = 50
    
    fieldsets = (
        ('基本信息', {
            'fields': ('type', 'level', 'difficulty', 'category', 'question_set')
        }),
        ('题目内容', {
            'fields': ('content', 'answer', 'options', 'explanation')
        }),
        ('听力题目', {
            'fields': ('audio_file', 'audio_url', 'audio_duration'),
            'classes': ('collapse',),
            'description': '适用于听力类题目'
        }),
        ('图片题目', {
            'fields': ('image_file', 'image_url'),
            'classes': ('collapse',),
            'description': '适用于看图选择、看图写作等题型'
        }),
        ('阅读理解', {
            'fields': ('passage', 'passage_title', 'sub_questions'),
            'classes': ('collapse',),
            'description': '适用于阅读理解类题目，sub_questions格式: [{"id": 1, "question": "...", "answer": "..."}]'
        }),
        ('配对与排序', {
            'fields': ('matching_pairs', 'ordering_items'),
            'classes': ('collapse',),
            'description': 'matching_pairs格式: [{"left": "...", "right": "..."}], ordering_items格式: ["项目1", "项目2", ...]'
        }),
        ('元数据', {
            'fields': ('tags', 'points', 'time_limit'),
            'classes': ('collapse',)
        }),
    )
    
    def type_display(self, obj):
        """显示题型"""
        type_colors = {
            'single': '#52c41a',
            'multiple': '#1890ff',
            'listening': '#722ed1',
            'dialogue': '#eb2f96',
            'reading': '#fa8c16',
            'image_choice': '#13c2c2',
            'matching': '#faad14',
            'ordering': '#2f54eb',
        }
        color = type_colors.get(obj.type, '#8c8c8c')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px; font-size: 12px;">{}</span>',
            color, obj.get_type_display()
        )
    type_display.short_description = '题型'
    
    def level_badge(self, obj):
        """显示等级徽章"""
        colors = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#52c41a', '#1890ff']
        color = colors[min(obj.level - 1, 5)] if obj.level > 0 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 50%; font-weight: bold;">HSK{}</span>',
            color, obj.level
        )
    level_badge.short_description = '等级'
    
    def content_preview(self, obj):
        """内容预览"""
        preview = obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, preview)
    content_preview.short_description = '题目内容'
    
    def category_display(self, obj):
        """显示分类"""
        if obj.category:
            return obj.category.get_name_display()
        return '-'
    category_display.short_description = '分类'
    
    def difficulty_stars(self, obj):
        """难度星级"""
        stars = '★' * obj.difficulty + '☆' * (5 - obj.difficulty)
        colors = ['#52c41a', '#52c41a', '#faad14', '#fa8c16', '#f5222d']
        color = colors[obj.difficulty - 1]
        return format_html('<span style="color: {}; font-size: 16px;">{}</span>', color, stars)
    difficulty_stars.short_description = '难度'
    
    def media_badge(self, obj):
        """多媒体标记"""
        badges = []
        if obj.audio_url or obj.audio_file:
            badges.append('<span style="background: #722ed1; color: white; padding: 2px 6px; '
                         'border-radius: 3px; font-size: 11px; margin-right: 4px;">🎵 音频</span>')
        if obj.image_url or obj.image_file:
            badges.append('<span style="background: #13c2c2; color: white; padding: 2px 6px; '
                         'border-radius: 3px; font-size: 11px; margin-right: 4px;">🖼️ 图片</span>')
        if obj.passage:
            badges.append('<span style="background: #fa8c16; color: white; padding: 2px 6px; '
                         'border-radius: 3px; font-size: 11px;">📖 文章</span>')
        return format_html(''.join(badges)) if badges else '-'
    media_badge.short_description = '多媒体'
    
    def save_model(self, request, obj, form, change):
        """保存时的额外处理"""
        super().save_model(request, obj, form, change)
        # 如果有套卷，更新套卷的题目数量
        if obj.question_set:
            obj.question_set.question_count = Question.objects.filter(
                question_set=obj.question_set
            ).count()
            obj.question_set.save()


@admin.register(QuestionSet)
class QuestionSetAdmin(admin.ModelAdmin):
    """套卷管理"""
    list_display = ['id', 'title', 'level_badge', 'exam_type_badge', 'question_count_display', 
                    'time_limit', 'created_at']
    list_filter = ['level', 'exam_type', 'created_at']
    search_fields = ['title', 'description']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'level', 'exam_type')
        }),
        ('配置', {
            'fields': ('time_limit', 'question_count')
        }),
    )
    
    def level_badge(self, obj):
        """等级徽章"""
        colors = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#52c41a', '#1890ff']
        color = colors[min(obj.level - 1, 5)] if obj.level > 0 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 50%; font-weight: bold;">HSK{}</span>',
            color, obj.level
        )
    level_badge.short_description = '等级'
    
    def exam_type_badge(self, obj):
        """试卷类型徽章"""
        type_colors = {
            'real': '#f5222d',
            'mock': '#1890ff',
            'sample': '#52c41a',
            'practice': '#faad14'
        }
        color = type_colors.get(obj.exam_type, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{}</span>',
            color, obj.get_exam_type_display()
        )
    exam_type_badge.short_description = '试卷类型'
    
    def question_count_display(self, obj):
        """题目数量"""
        actual_count = Question.objects.filter(question_set=obj).count()
        if actual_count != obj.question_count:
            return format_html(
                '<span style="color: #fa8c16;" title="实际数量与记录不符">{}题 (实际{})</span>',
                obj.question_count, actual_count
            )
        return format_html('<span style="font-weight: bold;">{}</span>题', actual_count)
    question_count_display.short_description = '题目数'


@admin.register(AnswerRecord)
class AnswerRecordAdmin(admin.ModelAdmin):
    """答题记录管理"""
    list_display = ['id', 'user', 'question_preview', 'user_answer_preview', 'is_correct_badge', 'created_at']
    list_filter = ['is_correct', 'created_at']
    search_fields = ['user__username', 'question__content']
    readonly_fields = ['user', 'question', 'user_answer', 'is_correct', 'created_at']
    
    def question_preview(self, obj):
        """题目预览"""
        content = obj.question.content[:30] + '...' if len(obj.question.content) > 30 else obj.question.content
        return content
    question_preview.short_description = '题目'
    
    def user_answer_preview(self, obj):
        """用户答案预览"""
        answer = str(obj.user_answer)[:20] + '...' if len(str(obj.user_answer)) > 20 else str(obj.user_answer)
        return answer
    user_answer_preview.short_description = '用户答案'
    
    def is_correct_badge(self, obj):
        """正确标记"""
        if obj.is_correct:
            return format_html('<span style="color: #52c41a; font-weight: bold;">✓ 正确</span>')
        return format_html('<span style="color: #f5222d; font-weight: bold;">✗ 错误</span>')
    is_correct_badge.short_description = '结果'


@admin.register(WrongBook)
class WrongBookAdmin(admin.ModelAdmin):
    """错题本管理"""
    list_display = ['id', 'user', 'question_info', 'question_type', 'created_at']
    list_filter = ['created_at', 'question__type', 'question__level']
    search_fields = ['user__username', 'question__content']
    readonly_fields = ['user', 'question', 'created_at']
    
    def question_info(self, obj):
        """题目信息"""
        content = obj.question.content[:40] + '...' if len(obj.question.content) > 40 else obj.question.content
        return format_html(
            '<div><strong>HSK{}</strong> - {}</div>',
            obj.question.level, content
        )
    question_info.short_description = '题目信息'
    
    def question_type(self, obj):
        """题目类型"""
        return obj.question.get_type_display()
    question_type.short_description = '题型'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """考试材料管理"""
    list_display = ['id', 'title', 'level_badge', 'section_badge', 'part_number', 
                    'question_range_display', 'media_badge', 'play_times', 'is_active']
    list_filter = ['level', 'section_type', 'part_number', 'is_active']
    search_fields = ['title', 'content', 'material_group']
    list_editable = ['is_active', 'play_times']
    ordering = ['level', 'section_type', 'part_number', 'order']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'level', 'section_type', 'part_number', 'material_group')
        }),
        ('材料内容', {
            'fields': ('content', 'audio_url', 'audio_duration')
        }),
        ('关联题目', {
            'fields': ('question_range_start', 'question_range_end', 'play_times')
        }),
        ('其他', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def level_badge(self, obj):
        """等级徽章"""
        colors = ['#f5222d', '#fa541c', '#fa8c16', '#faad14', '#52c41a', '#1890ff']
        color = colors[min(obj.level - 1, 5)] if obj.level > 0 else '#d9d9d9'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; '
            'border-radius: 50%; font-weight: bold;">HSK{}</span>',
            color, obj.level
        )
    level_badge.short_description = '等级'
    
    def section_badge(self, obj):
        """部分徽章"""
        colors = {
            'listening': '#722ed1',
            'reading': '#fa8c16',
            'writing': '#52c41a'
        }
        color = colors.get(obj.section_type, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{}</span>',
            color, obj.get_section_type_display()
        )
    section_badge.short_description = '部分'
    
    def question_range_display(self, obj):
        """题号范围"""
        if obj.question_range_start == obj.question_range_end:
            return f'第{obj.question_range_start}题'
        return f'第{obj.question_range_start}-{obj.question_range_end}题'
    question_range_display.short_description = '题号范围'
    
    def media_badge(self, obj):
        """多媒体标记"""
        badges = []
        if obj.audio_url:
            badges.append(f'<span style="background: #722ed1; color: white; padding: 2px 6px; '
                         f'border-radius: 3px; font-size: 11px; margin-right: 4px;">🎵 {obj.audio_duration}秒</span>')
        if obj.content:
            badges.append('<span style="background: #fa8c16; color: white; padding: 2px 6px; '
                         'border-radius: 3px; font-size: 11px;">📖 文字</span>')
        return format_html(''.join(badges)) if badges else '-'
    media_badge.short_description = '材料类型' 