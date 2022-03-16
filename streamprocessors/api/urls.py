from rest_framework.routers import DefaultRouter

from streamprocessors.api.views import StreamProcessorViewSet, StreamProcessorStepViewSet, WorkflowTaskViewSet


router = DefaultRouter()
router.register(r'streamprocessor', StreamProcessorViewSet, basename='streamprocessor')
router.register(r'streamprocessorstep', StreamProcessorStepViewSet, basename='streamprocessorstep')
router.register(r'workflowtask', WorkflowTaskViewSet, basename='workflowtask')

urlpatterns = router.urls
