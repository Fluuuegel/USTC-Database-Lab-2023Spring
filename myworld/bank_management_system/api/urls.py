from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('client', views.ClientViewSet)

app_name = 'api'
urlpatterns = router.urls