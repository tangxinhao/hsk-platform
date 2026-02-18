from rest_framework import serializers
from .models import HSKLevel, ExamOutline, StudyGuide, FAQ


class HSKLevelSerializer(serializers.ModelSerializer):
    """HSK等级序列化器"""
    class Meta:
        model = HSKLevel
        fields = '__all__'


class ExamOutlineSerializer(serializers.ModelSerializer):
    """考试大纲序列化器"""
    hsk_level_name = serializers.CharField(source='hsk_level.name', read_only=True)
    
    class Meta:
        model = ExamOutline
        fields = '__all__'


class StudyGuideSerializer(serializers.ModelSerializer):
    """学习指南序列化器"""
    hsk_level_name = serializers.CharField(source='hsk_level.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = StudyGuide
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    """常见问题序列化器"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = FAQ
        fields = '__all__'
