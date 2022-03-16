from rest_framework.routers import DefaultRouter

from functions.api.views import FunctionViewSet, FunctionEndpointViewSet


router = DefaultRouter()
router.register(r'function', FunctionViewSet, basename='function')
router.register(r'function-endpoint', FunctionEndpointViewSet, basename='functionendpoint')

urlpatterns = router.urls
