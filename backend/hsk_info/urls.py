from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'levels', views.HSKLevelViewSet)
router.register(r'outlines', views.ExamOutlineViewSet)
router.register(r'guides', views.StudyGuideViewSet)
router.register(r'faq', views.FAQViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
