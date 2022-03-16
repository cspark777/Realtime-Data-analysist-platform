from rest_framework.routers import DefaultRouter

from searches.api.views import SearchViewSet


router = DefaultRouter()
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = router.urls

