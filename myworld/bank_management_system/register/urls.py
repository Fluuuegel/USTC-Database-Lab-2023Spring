from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserViewSet)

app_name = 'register'
urlpatterns = []
urlpatterns += router.urls
