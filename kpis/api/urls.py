from rest_framework.routers import DefaultRouter

from kpis.api.views import KPIViewSet


router = DefaultRouter()
router.register(r'kpi', KPIViewSet, basename='kpi')

urlpatterns = router.urls
