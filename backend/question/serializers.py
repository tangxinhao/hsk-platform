from rest_framework import serializers
from .models import Question, AnswerRecord, WrongBook, QuestionSet, QuestionCategory, Material
from user.serializers import UserSerializer
import json

class QuestionSerializer(serializers.ModelSerializer):
    """题目序列化器 - 支持扩展题型"""
    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    has_media = serializers.BooleanField(read_only=True)
    media_type = serializers.SerializerMethodField()
    
    # 用户练习状态（需要上下文中的request）
    is_practiced = serializers.SerializerMethodField()
    practice_count = serializers.SerializerMethodField()
    last_practiced_at = serializers.SerializerMethodField()
    user_last_answer = serializers.SerializerMethodField()
    is_correct_last_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = [
            'id', 'type', 'type_display', 'level', 'content', 'answer', 'options', 'option_type',
            'explanation', 'category', 'category_name', 'question_set', 'difficulty',
            # 多媒体字段
            'audio_url', 'audio_duration', 'audio_group', 'image_url', 
            # 扩展字段
            'passage', 'passage_title', 'sub_questions', 'matching_pairs', 'ordering_items',
            # 元数据
            'tags', 'points', 'time_limit',
            'has_media', 'media_type',
            # HSK结构字段（新增）
            'section_type', 'part_number', 'question_number', 'material_group',
            'created_at', 'updated_at',
            # 用户练习状态
            'is_practiced', 'practice_count', 'last_practiced_at', 'user_last_answer', 'is_correct_last_time'
        ]
        read_only_fields = ['created_at', 'updated_at', 'has_media', 'is_practiced', 'practice_count', 'last_practiced_at']
    
    def to_representation(self, instance):
        """自定义序列化输出，将options从JSON字符串转换为数组"""
        data = super().to_representation(instance)
        
        # 将options字段从JSON字符串解析为数组
        if data.get('options') and isinstance(data['options'], str):
            try:
                data['options'] = json.loads(data['options'])
            except (json.JSONDecodeError, TypeError):
                data['options'] = []
        
        return data
    
    def get_media_type(self, obj):
        """获取多媒体类型"""
        return obj.get_media_type()
    
    def get_is_practiced(self, obj):
        """用户是否练习过此题"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import AnswerRecord
            return AnswerRecord.objects.filter(user=request.user, question=obj).exists()
        return False
    
    def get_practice_count(self, obj):
        """用户练习此题的次数"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import AnswerRecord
            return AnswerRecord.objects.filter(user=request.user, question=obj).count()
        return 0
    
    def get_last_practiced_at(self, obj):
        """最后一次练习时间"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import AnswerRecord
            record = AnswerRecord.objects.filter(user=request.user, question=obj).order_by('-created_at').first()
            return record.created_at.isoformat() if record else None
        return None
    
    def get_user_last_answer(self, obj):
        """用户最后一次的答案"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import AnswerRecord
            record = AnswerRecord.objects.filter(user=request.user, question=obj).order_by('-created_at').first()
            return record.user_answer if record else None
        return None
    
    def get_is_correct_last_time(self, obj):
        """最后一次是否正确"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from .models import AnswerRecord
            record = AnswerRecord.objects.filter(user=request.user, question=obj).order_by('-created_at').first()
            return record.is_correct if record else None
        return None
    
    def validate_level(self, value):
        """验证level字段（HSK等级1-6）"""
        if value is None:
            return 1
        if value < 1 or value > 6:
            raise serializers.ValidationError("HSK等级必须在1-6之间")
        return value
    
    def validate_audio_url(self, value):
        """验证audio_url字段，允许空值"""
        if not value or value.strip() == '':
            return ''  # 空值是允许的
        # 如果不是空值，Django的URLField会自动验证URL格式
        return value
    
    def validate_image_url(self, value):
        """验证image_url字段，允许空值"""
        if not value or value.strip() == '':
            return ''  # 空值是允许的
        return value
    
    def validate_options(self, value):
        """验证options字段，确保是有效的JSON数组"""
        if value and isinstance(value, str) and value.strip():
            try:
                # 尝试解析JSON
                parsed = json.loads(value)
                # 严格要求必须是列表
                if not isinstance(parsed, list):
                    raise serializers.ValidationError("选项必须是有效的JSON数组")
                # 注意：空数组是允许的，某些题型（如听力、判断题）可能不需要选项
            except json.JSONDecodeError:
                raise serializers.ValidationError("选项必须是有效的JSON格式")
        return value
    
    def to_internal_value(self, data):
        """在验证之前，将options字段转换为字符串（如果是列表/字典）"""
        # 获取原始数据
        options = data.get('options')
        if options and isinstance(options, (list, dict)):
            # 如果是列表或字典，转换为JSON字符串
            data = data.copy()
            data['options'] = json.dumps(options, ensure_ascii=False)

        # 兜底：如果未提供level/difficulty/points，则给默认值，避免校验失败
        if 'level' not in data or data.get('level') in (None, ''):
            data = data.copy()
            data['level'] = 1
        if 'difficulty' not in data or data.get('difficulty') in (None, ''):
            data = data.copy()
            data['difficulty'] = 3
        if 'points' not in data or data.get('points') in (None, ''):
            data = data.copy()
            data['points'] = 1

        return super().to_internal_value(data)

class AnswerRecordSerializer(serializers.ModelSerializer):
    """答题记录序列化器"""
    user = UserSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = AnswerRecord
        fields = ['id', 'user', 'question', 'user_answer', 'is_correct', 'created_at']
        read_only_fields = ['is_correct', 'created_at']

class WrongBookSerializer(serializers.ModelSerializer):
    """错题本序列化器"""
    question = QuestionSerializer(read_only=True)
    wrong_count = serializers.SerializerMethodField()
    reviewed_count = serializers.SerializerMethodField()
    is_mastered = serializers.BooleanField(default=False)
    last_reviewed_at = serializers.SerializerMethodField()
    
    class Meta:
        model = WrongBook
        fields = ['id', 'question', 'created_at', 'wrong_count', 'reviewed_count', 'is_mastered', 'last_reviewed_at']
        read_only_fields = ['created_at']
    
    def get_wrong_count(self, obj):
        # 统计该题目的错误次数
        return AnswerRecord.objects.filter(
            user=obj.user,
            question=obj.question,
            is_correct=False
        ).count()
    
    def get_reviewed_count(self, obj):
        # 统计加入错题本后的复习次数（答题记录）
        return AnswerRecord.objects.filter(
            user=obj.user,
            question=obj.question,
            created_at__gte=obj.created_at
        ).count()
    
    def get_last_reviewed_at(self, obj):
        # 最后复习时间
        last_record = AnswerRecord.objects.filter(
            user=obj.user,
            question=obj.question,
            created_at__gte=obj.created_at
        ).order_by('-created_at').first()
        return last_record.created_at if last_record else None


class QuestionSetSerializer(serializers.ModelSerializer):
    """套卷序列化器"""
    question_count = serializers.SerializerMethodField()
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    
    class Meta:
        model = QuestionSet
        fields = [
            'id', 'title', 'description', 'level', 'exam_type', 'exam_type_display',
            'time_limit', 'question_count', 'listening_audio_url', 'listening_audio_duration',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_question_count(self, obj):
        """获取题目数量"""
        return Question.objects.filter(question_set=obj).count()


class QuestionCategorySerializer(serializers.ModelSerializer):
    """题目分类序列化器"""
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    question_count = serializers.SerializerMethodField()
    level_range_display = serializers.CharField(source='get_level_range_display', read_only=True)
    
    class Meta:
        model = QuestionCategory
        fields = [
            'id', 'name', 'name_display', 'description', 'parent_category', 
            'level_range', 'level_range_display', 'icon', 'color', 'order', 
            'is_active', 'question_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_question_count(self, obj):
        """获取该分类下的题目数量"""
        return obj.get_question_count()


class MaterialSerializer(serializers.ModelSerializer):
    """考试材料序列化器"""
    section_type_display = serializers.CharField(source='get_section_type_display', read_only=True)
    question_range_display = serializers.SerializerMethodField()
    related_questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Material
        fields = [
            'id', 'title', 'level', 'section_type', 'section_type_display',
            'part_number', 'content', 'audio_url', 'audio_duration',
            'material_group', 'play_times', 'question_range_start',
            'question_range_end', 'question_range_display', 'order',
            'is_active', 'related_questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_question_range_display(self, obj):
        """获取题号范围显示"""
        if obj.question_range_start == obj.question_range_end:
            return f'第{obj.question_range_start}题'
        return f'第{obj.question_range_start}-{obj.question_range_end}题'
    
    def get_related_questions(self, obj):
        """获取关联的题目ID列表"""
        questions = Question.objects.filter(material_group=obj.material_group).values_list('id', flat=True)
        return list(questions)
