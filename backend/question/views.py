from rest_framework import generics, permissions, filters, viewsets, status
from rest_framework.pagination import PageNumberPagination
from .models import Question, AnswerRecord, WrongBook, Material, QuestionSet, QuestionCategory
from .serializers import (
    QuestionSerializer, AnswerRecordSerializer, WrongBookSerializer,
    MaterialSerializer, QuestionSetSerializer, QuestionCategorySerializer
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

# 自定义分页类，允许客户端指定page_size
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['type', 'level']
    
    def get_queryset(self):
        queryset = Question.objects.all()
        q_type = self.request.query_params.get('type')
        level = self.request.query_params.get('level')
        if q_type:
            queryset = queryset.filter(type=q_type)
        if level:
            queryset = queryset.filter(level=level)
        return queryset
    
    def get_serializer_context(self):
        """传递request到serializer以获取用户练习状态"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class AnswerSubmitView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = request.user
        question_id = request.data.get('question_id')
        user_answer = request.data.get('user_answer')
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': '题目不存在'}, status=404)
        is_correct = (user_answer == question.answer)
        # 如果用户已登录，记录答题历史
        if user.is_authenticated:
            record = AnswerRecord.objects.create(user=user, question=question, user_answer=user_answer, is_correct=is_correct)
            # 错题本逻辑
            if not is_correct:
                WrongBook.objects.get_or_create(user=user, question=question)
        return Response({'is_correct': is_correct})

class AnswerRecordListView(generics.ListAPIView):
    """答题记录查询API"""
    serializer_class = AnswerRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        queryset = AnswerRecord.objects.filter(user=user).select_related('question').order_by('-created_at')
        return queryset

class WrongBookListView(generics.ListAPIView):
    serializer_class = WrongBookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        queryset = WrongBook.objects.filter(user=user).select_related('question')
        
        # 等级筛选
        level = self.request.query_params.get('level')
        if level and level != '0':
            queryset = queryset.filter(question__level=level)
        
        # 题目类型筛选
        q_type = self.request.query_params.get('type')
        if q_type:
            queryset = queryset.filter(question__type=q_type)
        
        return queryset.order_by('-created_at')

class QuestionViewSet(viewsets.ModelViewSet):
    """
    问题视图集，提供增删改查功能
    支持参数：
    - question_set: 试卷套卷ID，只显示该套卷的题目
    - exclude_groups: true 排除听力/材料题组中的题目
    - type: 精确类型匹配（如reading_fill_blank）
    - type_like: 前缀模糊匹配（如listening，reading，writing）
    - level: 等级过滤
    - difficulty: 难度过滤
    - search: 搜索关键词
    - is_practiced: true/false 筛选已练习/未练习题目
    - is_correct: false 筛选错题（需配合is_practiced=true）
    """
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    pagination_class = LargeResultsSetPagination  # 使用自定义分页类
    
    def get_queryset(self):
        # 按创建时间倒序，避免新建题目看不到
        queryset = Question.objects.all().order_by('-id')
        
        # 试卷套卷过滤（用于管理后台显示特定套卷的题目）
        question_set = self.request.query_params.get('question_set')
        if question_set:
            queryset = queryset.filter(question_set_id=question_set)
        
        # 排除听力/材料题组中的题目，同时排除所有听力题型
        exclude_groups = self.request.query_params.get('exclude_groups', 'false').lower()
        if exclude_groups == 'true':
            queryset = queryset.filter(audio_group__isnull=True, material_group__isnull=True).exclude(type='listening')
        
        # 精确类型
        q_type = self.request.query_params.get('type')
        if q_type:
            queryset = queryset.filter(type=q_type)
        
        # 前缀匹配类型（如listening、reading、writing）
        type_like = self.request.query_params.get('type_like')
        if type_like:
            queryset = queryset.filter(type__startswith=type_like)
        
        # 等级过滤
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # 难度过滤
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # 搜索关键词
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(content__icontains=search)
        
        # 根据用户练习状态筛选（需要登录）
        is_practiced = self.request.query_params.get('is_practiced')
        is_correct = self.request.query_params.get('is_correct')
        
        if self.request.user.is_authenticated and is_practiced:
            if is_practiced.lower() == 'true':
                # 只显示已练习的题目
                practiced_question_ids = AnswerRecord.objects.filter(
                    user=self.request.user
                ).values_list('question_id', flat=True).distinct()
                queryset = queryset.filter(id__in=practiced_question_ids)
                
                # 进一步筛选：只显示答错的题目（错题本）
                if is_correct and is_correct.lower() == 'false':
                    wrong_question_ids = AnswerRecord.objects.filter(
                        user=self.request.user,
                        is_correct=False
                    ).values_list('question_id', flat=True).distinct()
                    queryset = queryset.filter(id__in=wrong_question_ids)
            elif is_practiced.lower() == 'false':
                # 只显示未练习的题目
                practiced_question_ids = AnswerRecord.objects.filter(
                    user=self.request.user
                ).values_list('question_id', flat=True).distinct()
                queryset = queryset.exclude(id__in=practiced_question_ids)
        
        return queryset

    def get_serializer_context(self):
        """传递request到serializer以获取用户练习状态"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        """创建题目"""
        logger.info(f"创建题目请求数据: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"创建题目验证失败: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"题目创建成功: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """更新题目"""
        logger.info(f"更新题目请求数据: {request.data}")
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            logger.error(f"更新题目验证失败: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        logger.info(f"题目更新成功: {serializer.data}")
        return Response(serializer.data)


class MaterialViewSet(viewsets.ModelViewSet):
    """考试材料视图集"""
    queryset = Material.objects.all().order_by('level', 'section_type', 'part_number', 'order')
    serializer_class = MaterialSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['level', 'section_type', 'part_number', 'is_active']
    
    @action(detail=False, methods=['get'])
    def by_structure(self, request):
        """按HSK结构获取材料"""
        level = request.query_params.get('level')
        section_type = request.query_params.get('section_type')
        part_number = request.query_params.get('part_number')
        
        queryset = self.get_queryset()
        if level:
            queryset = queryset.filter(level=level)
        if section_type:
            queryset = queryset.filter(section_type=section_type)
        if part_number:
            queryset = queryset.filter(part_number=part_number)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class QuestionCategoryViewSet(viewsets.ModelViewSet):
    """题目分类视图集"""
    queryset = QuestionCategory.objects.filter(is_active=True).order_by('order')
    serializer_class = QuestionCategorySerializer
    permission_classes = [AllowAny] 