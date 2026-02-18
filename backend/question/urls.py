from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuestionViewSet, QuestionListView, AnswerSubmitView, AnswerRecordListView, WrongBookListView,
    MaterialViewSet, QuestionCategoryViewSet
)
from .admin_views import QuestionSetViewSet
from . import exam_views
from .listening_views import (
    create_listening_group, get_listening_group, 
    list_listening_groups, update_listening_group, delete_listening_group
)

# 创建路由器
router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'sets', QuestionSetViewSet, basename='question-set')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'categories', QuestionCategoryViewSet, basename='category')

urlpatterns = [
    # 考试套卷详情（必须在路由器之前）
    path('sets/<int:pk>/structured/', exam_views.question_set_structured, name='question-set-structured'),
    
    # 题目相关
    path('list/', QuestionListView.as_view(), name='question-list'),
    path('answer/', AnswerSubmitView.as_view(), name='answer-submit'),
    path('answer-records/', AnswerRecordListView.as_view(), name='answer-records'),
    path('wrong-book/', WrongBookListView.as_view(), name='wrong-book'),
    
    # 考试相关（用户端API）
    path('exam/start/', exam_views.start_exam, name='start-exam'),
    path('exam/<int:exam_id>/submit-answer/', exam_views.submit_answer, name='submit-answer'),
    path('exam/<int:exam_id>/complete/', exam_views.complete_exam, name='complete-exam'),
    path('exam/<int:exam_id>/abandon/', exam_views.abandon_exam, name='abandon-exam'),
    path('exam/history/', exam_views.exam_history, name='exam-history'),
    path('exam/<int:exam_id>/report/', exam_views.exam_report, name='exam-report'),
    path('exam/<int:exam_id>/ranking/', exam_views.exam_ranking, name='exam-ranking'),
    path('exam/statistics/', exam_views.exam_statistics, name='exam-statistics'),
    
    # 听力题组管理
    path('listening-group/', create_listening_group, name='create-listening-group'),
    path('listening-groups/', list_listening_groups, name='list-listening-groups'),
    path('listening-group/<str:material_group>/', get_listening_group, name='get-listening-group'),
    path('listening-group/<str:material_group>/update/', update_listening_group, name='update-listening-group-post'),
    path('listening-group/<str:material_group>/', update_listening_group, name='update-listening-group-put'),
    path('listening-group/<str:material_group>/delete/', delete_listening_group, name='delete-listening-group'),
    
    # 路由器生成的URL（包含套卷管理）
    path('', include(router.urls)),
] 