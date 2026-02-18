from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import HSKLevel, ExamOutline, StudyGuide, FAQ
from .serializers import HSKLevelSerializer, ExamOutlineSerializer, StudyGuideSerializer, FAQSerializer


class HSKLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """HSK等级视图集（只读）"""
    queryset = HSKLevel.objects.all()
    serializer_class = HSKLevelSerializer
    permission_classes = [AllowAny]


class ExamOutlineViewSet(viewsets.ReadOnlyModelViewSet):
    """考试大纲视图集（只读）"""
    queryset = ExamOutline.objects.all()
    serializer_class = ExamOutlineSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ExamOutline.objects.all()
        hsk_level = self.request.query_params.get('hsk_level')
        if hsk_level:
            queryset = queryset.filter(hsk_level__level=hsk_level)
        return queryset


class StudyGuideViewSet(viewsets.ReadOnlyModelViewSet):
    """学习指南视图集（只读）"""
    queryset = StudyGuide.objects.all()
    serializer_class = StudyGuideSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = StudyGuide.objects.all()
        hsk_level = self.request.query_params.get('hsk_level')
        category = self.request.query_params.get('category')
        is_featured = self.request.query_params.get('is_featured')
        
        if hsk_level:
            queryset = queryset.filter(hsk_level__level=hsk_level)
        if category:
            queryset = queryset.filter(category=category)
        if is_featured:
            queryset = queryset.filter(is_featured=True)
        
        return queryset


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """常见问题视图集（只读）"""
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        category = self.request.query_params.get('category')
        is_featured = self.request.query_params.get('is_featured')
        
        if category:
            queryset = queryset.filter(category=category)
        if is_featured:
            queryset = queryset.filter(is_featured=True)
        
        return queryset
