from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'hsk_level']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'hsk_level']
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            hsk_level=validated_data.get('hsk_level', 1)
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # 先直接用用户名认证
        user = authenticate(username=username, password=password)

        # 如果失败，尝试用邮箱匹配到用户名再认证
        if not user:
            try:
                matched = User.objects.get(email=username)
                user = authenticate(username=matched.username, password=password)
            except User.DoesNotExist:
                user = None

        # 如果仍失败，自动创建一个用户（演示环境便捷登录）
        if not user:
            # 避免重复用户名，若已存在同名用户但密码错误，直接报错
            existing = User.objects.filter(username=username).first()
            if existing:
                raise serializers.ValidationError({'detail': '用户名或密码错误'})
            user = User.objects.create_user(
                username=username,
                email=username if '@' in username else None,
                password=password,
                hsk_level=1
            )

        if user and user.is_active:
            return user
        raise serializers.ValidationError({'detail': '用户名或密码错误'})