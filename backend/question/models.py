from django.db import models
from user.models import User


class Material(models.Model):
    """
    考试材料模型 - 用于存储听力/阅读材料
    一段音频/文章可以对应多道题目
    """
    title = models.CharField(max_length=200, verbose_name='材料标题')
    level = models.IntegerField(verbose_name='HSK等级', choices=[(i, f'HSK{i}') for i in range(1, 7)])
    section_type = models.CharField(max_length=20, verbose_name='部分类型', choices=[
        ('listening', '听力'),
        ('reading', '阅读'),
        ('writing', '书写')
    ])
    part_number = models.IntegerField(verbose_name='第几部分')
    content = models.TextField(blank=True, verbose_name='文字内容')
    audio_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='音频URL')
    audio_duration = models.IntegerField(default=0, verbose_name='音频时长（秒）')
    material_group = models.CharField(max_length=100, unique=True, verbose_name='材料组标识')
    play_times = models.IntegerField(default=2, verbose_name='播放次数')
    question_range_start = models.IntegerField(verbose_name='题号起始')
    question_range_end = models.IntegerField(verbose_name='题号结束')
    order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '考试材料'
        verbose_name_plural = '考试材料'
        ordering = ['level', 'section_type', 'part_number', 'order']
    
    def __str__(self):
        return f"HSK{self.level} {self.get_section_type_display()} Part{self.part_number} - {self.title}"


class QuestionCategory(models.Model):
    """题目分类模型 - 按HSK考试大纲分类"""
    CATEGORY_CHOICES = (
        # 听力部分
        ('listening_dialogue', '听力-对话理解'),
        ('listening_passage', '听力-短文理解'),
        ('listening_choice', '听力-听后选择'),
        
        # 阅读部分
        ('reading_vocabulary', '阅读-词汇理解'),
        ('reading_grammar', '阅读-语法运用'),
        ('reading_passage', '阅读-文章理解'),
        ('reading_cloze', '阅读-完形填空'),
        
        # 写作部分
        ('writing_character', '写作-汉字书写'),
        ('writing_sentence', '写作-句子造句'),
        ('writing_essay', '写作-作文'),
        ('writing_practical', '写作-应用文'),
        
        # 综合部分
        ('comprehensive_matching', '综合-词语搭配'),
        ('comprehensive_ordering', '综合-句子排序'),
        ('comprehensive_image', '综合-看图说话'),
        
        # 其他
        ('vocabulary', '词汇专项'),
        ('grammar', '语法专项'),
        ('culture', '文化常识'),
    )
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                       related_name='sub_categories', verbose_name='父分类')
    level_range = models.JSONField(blank=True, null=True, verbose_name='适用等级范围')
    icon = models.CharField(max_length=50, blank=True, verbose_name='图标')
    color = models.CharField(max_length=20, blank=True, verbose_name='颜色标识')
    order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '题目分类'
        verbose_name_plural = '题目分类'
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.get_name_display()
    
    def get_question_count(self):
        """获取该分类下的题目数量"""
        return self.question_set.count()
    
    def get_level_range_display(self):
        """获取适用等级范围显示"""
        if self.level_range:
            return f"HSK{self.level_range.get('min', 1)}-{self.level_range.get('max', 6)}"
        return "全部等级"

class QuestionSet(models.Model):
    """套卷模型"""
    EXAM_TYPE_CHOICES = [
        ('real', '真题'),
        ('mock', '模拟题'),
        ('sample', '样卷'),
        ('practice', '练习题'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='套卷标题')
    description = models.TextField(blank=True, verbose_name='描述')
    level = models.IntegerField(verbose_name='难度等级')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='practice', verbose_name='试卷类型')
    time_limit = models.IntegerField(default=120, verbose_name='时间限制(分钟)')
    question_count = models.IntegerField(default=0, verbose_name='题目数量')
    listening_audio_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='听力完整音频URL')
    listening_audio_duration = models.IntegerField(default=0, verbose_name='听力完整音频时长(秒)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '套卷'
        verbose_name_plural = '套卷'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} (HSK{self.level})"

class Question(models.Model):
    """题目模型 - 简化题目类型系统"""
    QUESTION_TYPE_CHOICES = [
        ('listening', '听力题'),
        ('reading', '阅读题'),
        ('writing', '书写题'),
        ('fill', '填空题'),
        ('single', '单选题'),
        ('multiple', '多选题'),
        ('judge', '判断题'),
    ]
    
    OPTION_TYPE_CHOICES = [
        ('text', '文字选项'),
        ('image', '图片选项'),
    ]
    
    type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES, verbose_name='题目类型')
    level = models.IntegerField(verbose_name='HSK等级 (1-6)')
    content = models.TextField(verbose_name='题目内容')
    answer = models.TextField(verbose_name='答案')
    options = models.TextField(default='', blank=True, verbose_name='选项(JSON格式)')
    option_type = models.CharField(max_length=10, choices=OPTION_TYPE_CHOICES, default='text', verbose_name='选项类型')
    explanation = models.TextField(blank=True, null=True, verbose_name='答案解析')
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='题目分类')
    question_set = models.ForeignKey(QuestionSet, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所属套卷')
    difficulty = models.IntegerField(default=3, choices=[(1, '简单'), (2, '较易'), (3, '中等'), (4, '较难'), (5, '困难')], verbose_name='难度系数')
    
    # ========== HSK考试结构字段（新增）==========
    section_type = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('listening', '听力'),
            ('reading', '阅读'),
            ('writing', '书写')
        ],
        verbose_name='部分类型'
    )
    part_number = models.IntegerField(blank=True, null=True, verbose_name='第几部分')
    question_number = models.IntegerField(blank=True, null=True, verbose_name='题号')
    
    # 关联材料（用于一段材料对应多题）
    material_group = models.CharField(max_length=100, blank=True, null=True, 
                                     verbose_name='材料组标识',
                                     help_text='与Material模型的material_group关联')
    
    # 听力相关字段
    audio_file = models.FileField(upload_to='audio/%Y/%m/', blank=True, null=True, verbose_name='音频文件')
    audio_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='音频URL或路径')
    audio_duration = models.IntegerField(default=0, blank=True, verbose_name='音频时长(秒)')
    audio_group = models.CharField(max_length=100, blank=True, null=True, verbose_name='音频分组标识')
    
    # 图片相关字段
    image_file = models.FileField(upload_to='images/%Y/%m/', blank=True, null=True, verbose_name='题目图片文件')
    image_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片URL或路径')
    
    # 阅读理解/对话相关字段
    passage = models.TextField(blank=True, null=True, verbose_name='文章/对话内容')
    passage_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='文章标题')
    
    # 复杂题型数据字段（JSON格式）
    sub_questions = models.JSONField(blank=True, null=True, verbose_name='子题目列表')
    matching_pairs = models.JSONField(blank=True, null=True, verbose_name='匹配对信息')
    ordering_items = models.JSONField(blank=True, null=True, verbose_name='排序项列表')
    
    # 元数据字段
    tags = models.JSONField(blank=True, null=True, verbose_name='标签')
    points = models.IntegerField(default=1, verbose_name='分值')
    time_limit = models.IntegerField(default=0, blank=True, verbose_name='答题时限(秒)')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['id']  # 添加默认排序，避免分页警告

    def __str__(self):
        return f"{self.type}-{self.level}: {self.content[:20]}"
    
    def get_options_list(self):
        """将options字段解析为列表"""
        import json
        if self.options:
            try:
                return json.loads(self.options)
            except:
                return []
        return []
    
    def get_matching_pairs(self):
        """获取匹配题的配对信息"""
        if self.type == 'matching' and self.matching_pairs:
            return self.matching_pairs
        return []
    
    def get_ordering_items(self):
        """获取排序题的项目列表"""
        if self.type == 'ordering' and self.ordering_items:
            return self.ordering_items
        return []
    
    def get_sub_questions(self):
        """获取子题目列表（用于阅读理解等）"""
        if self.sub_questions:
            return self.sub_questions
        return []
    
    def has_media(self):
        """判断题目是否包含多媒体"""
        return bool(self.audio_url or self.audio_file or self.image_url or self.image_file)
    
    def get_media_type(self):
        """获取多媒体类型"""
        if self.audio_url or self.audio_file:
            return 'audio'
        if self.image_url or self.image_file:
            return 'image'
        return None

class AnswerRecord(models.Model):
    """答题记录模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='题目')
    user_answer = models.TextField(verbose_name='用户答案')
    is_correct = models.BooleanField(verbose_name='是否正确')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录'

    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {'正确' if self.is_correct else '错误'}"

class WrongBook(models.Model):
    """错题本模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='题目')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '错题本'
        verbose_name_plural = '错题本'
        unique_together = ['user', 'question']  # 确保每个用户的每道题只记录一次

    def __str__(self):
        return f"{self.user.username} - {self.question.id}"
