from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', lambda request: JsonResponse({'message': 'HSK API', 'endpoints': {
        'question': '/api/question/',
        'university': '/api/university/',
        'culture': '/api/culture/',
        'user': '/api/user/',
        'hsk_info': '/api/hsk-info/',
    }})),
    path('api/question/', include('question.urls')),
    path('api/university/', include('university.urls')),
    path('api/culture/', include('culture.urls')),
    path('api/user/', include('user.urls')),
    path('api/hsk-info/', include('hsk_info.urls')),
]

# 在开发环境中添加媒体文件的URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
