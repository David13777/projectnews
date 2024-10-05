from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from news.views import PostNewsViewSet, PostArticlesViewSet

router = routers.DefaultRouter()
router.register(prefix=r'news', viewset=PostNewsViewSet, basename='news')
router.register(prefix=r'articles', viewset=PostArticlesViewSet, basename='articles')


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('news.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include(arg='rest_framework.urls', namespace='rest_framework')),
]
