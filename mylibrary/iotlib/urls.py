from django.db import router
from django.urls import path, include
from rest_framework import routers

from . import views
from rest_framework.authtoken import views as tokenviews

router = routers.DefaultRouter()
router.register(r'shelf-info', views.ShelfInfoViewSet)
router.register(r'shelf-update', views.ShelfStateViewSet)

urlpatterns = [
    path('test', views.index, name='index'),
    path('api-auth', include('rest_framework.urls', namespace='rest-framework')),
    path('', include(router.urls)),
        ] + [path('api-token-auth/', tokenviews.obtain_auth_token)]
