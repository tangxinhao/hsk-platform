from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Category, Content, Favorite
from .serializers import CategorySerializer, ContentSerializer, FavoriteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging

logger = logging.getLogger(__name__)

# 自定义分页类
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()

class ContentListView(generics.ListAPIView):
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        queryset = Content.objects.all()
        category = self.request.query_params.get('category')
        level = self.request.query_params.get('level')
        if category:
            queryset = queryset.filter(category_id=category)
        if level:
            queryset = queryset.filter(category__level=level)
        return queryset

class ContentDetailView(generics.RetrieveAPIView):
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]
    queryset = Content.objects.all()

class FavoriteView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        content_id = request.data.get('content_id')
        user = request.user
        if user.is_authenticated:
            favorite, created = Favorite.objects.get_or_create(user=user, content_id=content_id)
            return Response({'favorited': True})
        return Response({'error': '未登录'}, status=401)
        
    def delete(self, request):
        content_id = request.data.get('content_id')
        user = request.user
        if user.is_authenticated:
            Favorite.objects.filter(user=user, content_id=content_id).delete()
            return Response({'favorited': False})
        return Response({'error': '未登录'}, status=401)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    文化分类视图集，提供增删改查功能
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination  # 使用自定义分页类

    def create(self, request, *args, **kwargs):
        """
        重写创建方法，添加更多错误处理和日志
        """
        logger.info(f"接收到创建分类请求: {request.data}")
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"分类创建验证失败: {serializer.errors}")
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"分类创建成功: {serializer.data}")
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class ContentViewSet(viewsets.ModelViewSet):
    """
    文化内容视图集，提供增删改查功能
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination  # 使用自定义分页类
    
    def get_queryset(self):
        """
        支持按分类筛选内容
        """
        queryset = Content.objects.all()
        category = self.request.query_params.get('category')
        level = self.request.query_params.get('level')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category_id=category)
        if level:
            queryset = queryset.filter(category__level=level)
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def increment_view(self, request, pk=None):
        """
        增加内容的浏览次数
        """
        try:
            content = self.get_object()
            content.view_count += 1
            content.save(update_fields=['view_count'])
            return Response({
                'success': True,
                'view_count': content.view_count
            })
        except Content.DoesNotExist:
            return Response({
                'success': False,
                'error': '内容不存在'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"增加浏览次数失败: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [AllowAny] 