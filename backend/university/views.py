from rest_framework import generics, serializers, views, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from .models import University
from .serializers import UniversitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# 自定义分页类
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class UniversityListView(generics.ListAPIView):
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = University.objects.all()
        region = self.request.query_params.get('region')
        if region:
            queryset = queryset.filter(region=region)
        return queryset

class UniversityRecommendView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        hsk_level = getattr(request.user, 'hsk_level', None)
        region = request.query_params.get('region')
        queryset = University.objects.all()
        if region:
            queryset = queryset.filter(region=region)
        # 简单推荐逻辑：按HSK等级和排名排序
        queryset = queryset.order_by('ranking')[:10]
        return Response(UniversitySerializer(queryset, many=True).data)

class UniversityCompareView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        ids = request.data.get('ids', [])
        queryset = University.objects.filter(id__in=ids)
        return Response(UniversitySerializer(queryset, many=True).data)

class UniversityViewSet(viewsets.ModelViewSet):
    """
    大学视图集，提供增删改查功能
    """
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]  # 已经是AllowAny
    pagination_class = LargeResultsSetPagination  # 使用自定义分页类 