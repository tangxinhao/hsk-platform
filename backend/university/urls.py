from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityViewSet, UniversityListView, UniversityRecommendView, UniversityCompareView

# 创建路由器
router = DefaultRouter()
router.register(r'', UniversityViewSet)  # 注册视图集，使用空字符串作为基础路径

urlpatterns = [
    # 包含路由器生成的URL
    path('', include(router.urls)),
    path('list/', UniversityListView.as_view(), name='university-list'),
    path('recommend/', UniversityRecommendView.as_view(), name='university-recommend'),
    path('compare/', UniversityCompareView.as_view(), name='university-compare'),
] 