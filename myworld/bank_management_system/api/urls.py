from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('client', views.ClientViewSet)
router.register('staff', views.StaffViewSet)
router.register('branch', views.BranchViewSet)
router.register('account', views.AccountViewSet)
router.register('loan', views.LoanViewSet)
router.register('client_loan', views.ClientLoanViewSet)
router.register('client_branch', views.ClientBranchViewSet)
router.register('client_search', views.ClientSearchViewSet)

app_name = 'api'
urlpatterns = []
urlpatterns += router.urls

