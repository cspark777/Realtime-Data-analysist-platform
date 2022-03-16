from rest_framework.routers import DefaultRouter

from streams.api.views import StreamViewSet


router = DefaultRouter()
router.register(r'stream', StreamViewSet, basename='stream')

urlpatterns = router.urls
