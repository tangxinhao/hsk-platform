from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, ContentViewSet, FavoriteViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'content', ContentViewSet)
router.register(r'favorite', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 