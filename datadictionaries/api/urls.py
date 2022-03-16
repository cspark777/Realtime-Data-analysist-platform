from rest_framework.routers import DefaultRouter

from datadictionaries.api.views import DataDictionaryViewSet, DataItemViewSet


router = DefaultRouter()
router.register(r'datadictionary', DataDictionaryViewSet, basename='datadictionary')
router.register(r'dataitem', DataItemViewSet, basename='dataitem')

urlpatterns = router.urls
