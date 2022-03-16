from rest_framework.routers import DefaultRouter

from schemas.api.views import SchemaViewSet, SchemaFieldViewSet


router = DefaultRouter()
router.register(r'schema', SchemaViewSet, basename='schema')
router.register(r'schemafield', SchemaFieldViewSet, basename='schemafield')

urlpatterns = router.urls
