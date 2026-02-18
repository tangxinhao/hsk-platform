from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Content, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """文化分类管理"""
    list_display = ['id', 'name', 'level_badge', 'description_preview', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['level', 'id']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'level', 'description')
        }),
    )
    
    def level_badge(self, obj):
        """等级徽章"""
        level_colors = {
            '初级': '#52c41a',
            '中级': '#faad14',
            '高级': '#f5222d'
        }
        color = level_colors.get(obj.level, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 4px; font-weight: bold;">{}</span>',
            color, obj.level
        )
    level_badge.short_description = '等级'
    
    def description_preview(self, obj):
        """描述预览"""
        if obj.description:
            preview = obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
            return format_html('<span title="{}">{}</span>', obj.description, preview)
        return '-'
    description_preview.short_description = '描述'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """文化内容管理"""
    list_display = ['id', 'title', 'category_name', 'content_type_badge', 'difficulty_stars',
                    'view_count', 'like_count', 'duration_display', 'created_at']
    list_filter = ['content_type', 'difficulty', 'category', 'created_at']
    search_fields = ['title', 'content']
    list_per_page = 30
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'title_en', 'subtitle', 'subtitle_en', 'category', 'content_type', 'difficulty')
        }),
        ('描述', {
            'fields': ('description', 'description_en')
        }),
        ('内容', {
            'fields': ('content', 'content_en', 'cover_image')
        }),
        ('结构化数据', {
            'fields': ('structured_data',),
            'classes': ('collapse',),
            'description': 'JSON格式：用于菜系特点、名菜等结构化信息'
        }),
        ('多媒体', {
            'fields': ('video_url', 'audio_url', 'duration'),
            'classes': ('collapse',),
            'description': '选填：视频、音频链接和时长'
        }),
        ('统计信息', {
            'fields': ('view_count', 'like_count'),
            'classes': ('collapse',)
        }),
    )
    
    def category_name(self, obj):
        """分类名称"""
        return obj.category.name if obj.category else '-'
    category_name.short_description = '分类'
    
    def content_type_badge(self, obj):
        """内容类型徽章"""
        type_icons = {
            'article': '📄',
            'video': '🎬',
            'image': '🖼️',
            'audio': '🎵',
            'interactive': '🎮'
        }
        type_colors = {
            'article': '#1890ff',
            'video': '#722ed1',
            'image': '#13c2c2',
            'audio': '#eb2f96',
            'interactive': '#52c41a'
        }
        icon = type_icons.get(obj.content_type, '📋')
        color = type_colors.get(obj.content_type, '#d9d9d9')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; '
            'border-radius: 4px;">{} {}</span>',
            color, icon, obj.get_content_type_display()
        )
    content_type_badge.short_description = '类型'
    
    def difficulty_stars(self, obj):
        """难度星级"""
        stars = '★' * obj.difficulty + '☆' * (5 - obj.difficulty)
        colors = ['#52c41a', '#52c41a', '#faad14', '#fa8c16', '#f5222d']
        color = colors[obj.difficulty - 1]
        return format_html('<span style="color: {}; font-size: 16px;">{}</span>', color, stars)
    difficulty_stars.short_description = '难度'
    
    def duration_display(self, obj):
        """时长显示"""
        if obj.duration > 0:
            return format_html('<span>{}分钟</span>', obj.duration)
        return '-'
    duration_display.short_description = '时长'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """收藏管理"""
    list_display = ['id', 'user', 'content_title', 'favorited_at']
    list_filter = ['favorited_at']
    search_fields = ['user__username', 'content__title']
    readonly_fields = ['favorited_at']
    
    def content_title(self, obj):
        """内容标题"""
        return obj.content.title if obj.content else '-'
    content_title.short_description = '内容' 