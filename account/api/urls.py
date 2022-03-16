from rest_framework.routers import DefaultRouter

from account.api.views import CustomUserViewSet


router = DefaultRouter()
router.register(r'user', CustomUserViewSet, basename='customuser')

urlpatterns = router.urls
