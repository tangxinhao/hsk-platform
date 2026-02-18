from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserInfoView, get_csrf_token
from .views_progress import UserProgressView, UserStudyHistoryView, UniversityRecommendationView
from .dashboard_views import (
    get_user_dashboard, 
    get_admin_dashboard, 
    set_study_goal, 
    export_study_report
)
from .progress_views import (
    get_progress_overview,
    get_level_progress,
    get_recent_activities,
    get_study_goals,
    get_weak_points,
    get_study_trend
)

# 创建路由器
router = DefaultRouter()
# 如果有其他视图集，可以在这里注册

urlpatterns = [
    # 认证相关
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', UserInfoView.as_view()),
    path('csrf-token/', get_csrf_token, name='csrf-token'),
    
    # Dashboard相关
    path('dashboard/', get_user_dashboard, name='user-dashboard'),
    path('admin-dashboard/', get_admin_dashboard, name='admin-dashboard'),
    path('set-goal/', set_study_goal, name='set-study-goal'),
    path('export-report/', export_study_report, name='export-report'),
    
    # 学习进度相关
    path('progress/', UserProgressView.as_view(), name='user-progress'),
    path('study-history/', UserStudyHistoryView.as_view(), name='study-history'),
    path('university-recommendations/', UniversityRecommendationView.as_view(), name='university-recommendations'),
    
    # 学习进度详细API
    path('progress/overview/', get_progress_overview, name='progress-overview'),
    path('progress/level/', get_level_progress, name='level-progress'),  # 修正：去掉s
    path('progress/levels/', get_level_progress, name='level-progress-alias'),  # 保留兼容
    path('progress/trend/', get_study_trend, name='study-trend'),  # 新增：学习趋势
    path('progress/activities/', get_recent_activities, name='recent-activities'),
    path('progress/goals/', get_study_goals, name='study-goals'),
    path('progress/weak-points/', get_weak_points, name='weak-points'),
    
    path('', include(router.urls)),
]
