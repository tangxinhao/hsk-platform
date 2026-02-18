from rest_framework import serializers
from .models import University

class UniversitySerializer(serializers.ModelSerializer):
    # 前端使用的字段映射（驼峰命名）
    englishName = serializers.CharField(source='english_name', required=False, allow_blank=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    # 从tags字段中提取的虚拟字段
    is985 = serializers.SerializerMethodField()
    is211 = serializers.SerializerMethodField()
    isDoubleFirstClass = serializers.SerializerMethodField()
    establishYear = serializers.SerializerMethodField()
    
    class Meta:
        model = University
        fields = '__all__'
    
    def get_is985(self, obj):
        """从tags中获取985标签"""
        if not obj.tags:
            return False
        if isinstance(obj.tags, list):
            return '985工程' in obj.tags
        if isinstance(obj.tags, dict):
            labels = obj.tags.get('labels', [])
            return '985工程' in labels
        return False
    
    def get_is211(self, obj):
        """从tags中获取211标签"""
        if not obj.tags:
            return False
        if isinstance(obj.tags, list):
            return '211工程' in obj.tags
        if isinstance(obj.tags, dict):
            labels = obj.tags.get('labels', [])
            return '211工程' in labels
        return False
    
    def get_isDoubleFirstClass(self, obj):
        """从tags中获取双一流标签"""
        if not obj.tags:
            return False
        if isinstance(obj.tags, list):
            return '双一流' in obj.tags
        if isinstance(obj.tags, dict):
            labels = obj.tags.get('labels', [])
            return '双一流' in labels
        return False
    
    def get_establishYear(self, obj):
        """从tags中获取建校年份"""
        if not obj.tags:
            return None
        if isinstance(obj.tags, dict):
            return obj.tags.get('establishYear')
        return None
    
    def to_internal_value(self, data):
        """处理前端发送的数据，将标签字段转换为tags"""
        # 先调用父类方法进行基本验证
        ret = super().to_internal_value(data)
        
        # 构建tags字段
        tags_dict = {}
        labels = []
        
        # 处理985/211/双一流标签
        if data.get('is985') is True:
            labels.append('985工程')
        if data.get('is211') is True:
            labels.append('211工程')
        if data.get('isDoubleFirstClass') is True:
            labels.append('双一流')
        
        # 处理建校年份
        establish_year = data.get('establishYear')
        if establish_year:
            tags_dict['establishYear'] = establish_year
        
        # 组装tags字段
        if labels:
            tags_dict['labels'] = labels
        
        # 如果有任何标签数据，保存到tags字段
        if tags_dict:
            ret['tags'] = tags_dict
        else:
            ret['tags'] = None
        
        return ret 