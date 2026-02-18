from django.db import models


class HSKLevel(models.Model):
    """HSK等级介绍模型"""
    level = models.IntegerField(unique=True, verbose_name='HSK等级')
    name = models.CharField(max_length=50, verbose_name='等级名称')
    description = models.TextField(verbose_name='等级描述')
    
    # 能力要求
    vocabulary_count = models.IntegerField(verbose_name='词汇量要求')
    listening_ability = models.TextField(verbose_name='听力能力要求')
    reading_ability = models.TextField(verbose_name='阅读能力要求')
    writing_ability = models.TextField(blank=True, verbose_name='写作能力要求')
    
    # 考试信息
    exam_duration = models.IntegerField(verbose_name='考试时长(分钟)')
    total_score = models.IntegerField(default=300, verbose_name='总分')
    passing_score = models.IntegerField(verbose_name='及格分数')
    
    # 考试结构
    exam_structure = models.JSONField(verbose_name='考试结构', help_text='JSON格式：[{"part": "听力", "questions": 45, "time": 35}, ...]')
    
    # 适用人群
    target_audience = models.TextField(verbose_name='适用人群')
    study_hours = models.IntegerField(verbose_name='建议学习时长(小时)')
    
    # 等级图标和颜色
    icon = models.CharField(max_length=50, blank=True, verbose_name='图标')
    color = models.CharField(max_length=20, blank=True, verbose_name='颜色代码')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = 'HSK等级'
        verbose_name_plural = 'HSK等级'
        ordering = ['level']
    
    def __str__(self):
        return f"HSK{self.level} - {self.name}"


class ExamOutline(models.Model):
    """考试大纲模型"""
    hsk_level = models.ForeignKey(HSKLevel, on_delete=models.CASCADE, related_name='outlines', verbose_name='HSK等级')
    section = models.CharField(max_length=50, verbose_name='考试部分')
    part_number = models.IntegerField(verbose_name='部分序号')
    title = models.CharField(max_length=200, verbose_name='部分标题')
    description = models.TextField(verbose_name='部分描述')
    question_count = models.IntegerField(verbose_name='题目数量')
    time_limit = models.IntegerField(verbose_name='时间限制(分钟)')
    question_types = models.JSONField(verbose_name='题型说明', help_text='JSON格式：["听后选择", "听后判断", ...]')
    scoring_method = models.TextField(verbose_name='计分方式')
    tips = models.TextField(blank=True, verbose_name='答题技巧')
    
    order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '考试大纲'
        verbose_name_plural = '考试大纲'
        ordering = ['hsk_level', 'order', 'part_number']
    
    def __str__(self):
        return f"{self.hsk_level} - {self.section} - 第{self.part_number}部分"


class StudyGuide(models.Model):
    """学习指南模型"""
    hsk_level = models.ForeignKey(HSKLevel, on_delete=models.CASCADE, related_name='study_guides', verbose_name='HSK等级')
    title = models.CharField(max_length=200, verbose_name='指南标题')
    category = models.CharField(
        max_length=50,
        choices=[
            ('preparation', '备考准备'),
            ('vocabulary', '词汇学习'),
            ('grammar', '语法学习'),
            ('listening', '听力训练'),
            ('reading', '阅读训练'),
            ('writing', '写作训练'),
            ('exam_tips', '考试技巧'),
            ('resources', '学习资源')
        ],
        verbose_name='指南分类'
    )
    content = models.TextField(verbose_name='指南内容')
    tips = models.JSONField(blank=True, null=True, verbose_name='要点提示', help_text='JSON数组格式')
    resources = models.JSONField(blank=True, null=True, verbose_name='相关资源', help_text='JSON格式：[{"name": "...", "url": "..."}]')
    
    order = models.IntegerField(default=0, verbose_name='排序')
    is_featured = models.BooleanField(default=False, verbose_name='是否推荐')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '学习指南'
        verbose_name_plural = '学习指南'
        ordering = ['hsk_level', 'order']
    
    def __str__(self):
        return f"{self.hsk_level} - {self.title}"


class FAQ(models.Model):
    """常见问题模型"""
    category = models.CharField(
        max_length=50,
        choices=[
            ('exam_info', '考试信息'),
            ('registration', '报名相关'),
            ('preparation', '备考相关'),
            ('certificate', '证书相关'),
            ('other', '其他')
        ],
        verbose_name='问题分类'
    )
    question = models.CharField(max_length=500, verbose_name='问题')
    answer = models.TextField(verbose_name='答案')
    related_links = models.JSONField(blank=True, null=True, verbose_name='相关链接')
    
    order = models.IntegerField(default=0, verbose_name='排序')
    view_count = models.IntegerField(default=0, verbose_name='查看次数')
    is_featured = models.BooleanField(default=False, verbose_name='是否热门')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '常见问题'
        verbose_name_plural = '常见问题'
        ordering = ['-is_featured', 'order', '-view_count']
    
    def __str__(self):
        return self.question[:50]
