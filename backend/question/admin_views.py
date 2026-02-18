"""
管理后台API视图
提供套卷的CRUD操作
"""
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import QuestionSet
from .serializers import QuestionSetSerializer
import logging

logger = logging.getLogger(__name__)

# 自定义分页类
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class QuestionSetViewSet(viewsets.ModelViewSet):
    """
    套卷管理ViewSet
    提供完整的CRUD操作
    """
    queryset = QuestionSet.objects.all().order_by('-created_at')
    serializer_class = QuestionSetSerializer
    permission_classes = [AllowAny]  # 开发阶段使用AllowAny，生产环境应改为IsAdminUser
    pagination_class = LargeResultsSetPagination  # 使用自定义分页类
    
    def list(self, request, *args, **kwargs):
        """获取套卷列表"""
        try:
            level = request.GET.get('level')
            queryset = self.get_queryset()
            
            if level:
                try:
                    queryset = queryset.filter(level=int(level))
                except ValueError:
                    logger.warning(f"无效的level参数: {level}")
            
            # 使用分页
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                logger.info(f"成功获取{len(serializer.data)}个套卷 (分页)")
                return self.get_paginated_response(serializer.data)
            
            # 如果没有分页，返回所有数据
            serializer = self.get_serializer(queryset, many=True)
            logger.info(f"成功获取{len(serializer.data)}个套卷")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"获取套卷列表失败: {str(e)}", exc_info=True)
            return Response(
                {'error': '获取套卷列表失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def create(self, request, *args, **kwargs):
        """创建套卷"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info(f"成功创建套卷: {serializer.data['title']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"创建套卷失败: {str(e)}", exc_info=True)
            return Response(
                {'error': '创建套卷失败', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        """更新套卷"""
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            logger.info(f"成功更新套卷: {serializer.data['title']}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"更新套卷失败: {str(e)}", exc_info=True)
            return Response(
                {'error': '更新套卷失败', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        """删除套卷"""
        try:
            instance = self.get_object()
            title = instance.title
            self.perform_destroy(instance)
            logger.info(f"成功删除套卷: {title}")
            return Response(
                {'message': '删除成功'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            logger.error(f"删除套卷失败: {str(e)}", exc_info=True)
            return Response(
                {'error': '删除套卷失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """获取套卷下的所有题目"""
        try:
            question_set = self.get_object()
            from .models import Question
            from .serializers import QuestionSerializer
            
            questions = Question.objects.filter(question_set=question_set).order_by('id')
            serializer = QuestionSerializer(questions, many=True)
            
            return Response({
                'question_set': self.get_serializer(question_set).data,
                'questions': serializer.data,
                'total': questions.count()
            })
        except Exception as e:
            logger.error(f"获取套卷题目失败: {str(e)}", exc_info=True)
            return Response(
                {'error': '获取套卷题目失败'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
