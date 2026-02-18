from django.db import models
from user.models import User

class Category(models.Model):
    LEVEL_CHOICES = (
        ('初级', '初级'),
        ('中级', '中级'),
        ('高级', '高级'),
    )
    name = models.CharField(max_length=100, verbose_name='分类名称')
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='英文名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    description_en = models.TextField(blank=True, null=True, verbose_name='英文描述')
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['id']

    def __str__(self):
        return self.name

class Content(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('article', '文章'),
        ('video', '视频'),
        ('image', '图片'),
        ('audio', '音频'),
        ('interactive', '互动'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    title = models.CharField(max_length=255, verbose_name='标题')
    title_en = models.CharField(max_length=255, blank=True, null=True, verbose_name='英文标题')
    content = models.TextField(verbose_name='内容')
    content_en = models.TextField(blank=True, null=True, verbose_name='英文内容')
    paragraphs = models.JSONField(blank=True, null=True, verbose_name='段落内容(中英对照)')
    description = models.TextField(blank=True, null=True, verbose_name='简短描述')
    description_en = models.TextField(blank=True, null=True, verbose_name='英文描述')
    subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='副标题')
    subtitle_en = models.CharField(max_length=500, blank=True, null=True, verbose_name='英文副标题')
    
    # 结构化数据字段（用于菜系等特殊内容）
    structured_data = models.JSONField(blank=True, null=True, verbose_name='结构化数据', help_text='用于存储菜系特点、名菜、文化内涵等结构化信息')
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='article', verbose_name='内容类型')
    cover_image = models.URLField(max_length=500, blank=True, null=True, verbose_name='封面图片')
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='视频链接')
    audio_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='音频链接')
    duration = models.IntegerField(default=0, verbose_name='时长(分钟)')
    difficulty = models.IntegerField(default=3, choices=[(1, '简单'), (2, '较易'), (3, '中等'), (4, '较难'), (5, '困难')], verbose_name='难度系数')
    view_count = models.IntegerField(default=0, verbose_name='观看次数')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '文化内容'
        verbose_name_plural = '文化内容'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='内容')
    favorited_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ['user', 'content']

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"
