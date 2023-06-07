# from rest_framework.routers import DefaultRouter
from . import views
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('client', views.ClientViewSet)
router.register('branch', views.BranchViewSet)
router.register('account', views.AccountViewSet)

app_name = 'api'
urlpatterns = []
urlpatterns += router.urls

