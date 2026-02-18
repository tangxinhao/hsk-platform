from rest_framework import serializers
from .models import Category, Content, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, data):
        """
        添加额外的验证逻辑
        """
        # 确保name字段存在且不为空
        if 'name' not in data or not data['name']:
            raise serializers.ValidationError({"name": "分类名称不能为空"})
        
        # 添加其他字段验证
        
        return data

    def create(self, validated_data):
        """
        自定义创建逻辑，添加日志记录以便调试
        """
        print(f"创建分类，数据: {validated_data}")
        return super().create(validated_data)

class ContentSerializer(serializers.ModelSerializer):
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Content
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__' 