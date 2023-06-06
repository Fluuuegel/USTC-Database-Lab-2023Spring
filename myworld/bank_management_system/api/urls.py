# from rest_framework.routers import DefaultRouter
from . import views
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('client', views.ClientViewSet)

app_name = 'api'
urlpatterns = []
urlpatterns += router.urls

