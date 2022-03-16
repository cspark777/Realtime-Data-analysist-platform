from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from schemas.models import Schema, SchemaField
from schemas.api.serializers import SchemaBaseSerializer, SchemaSerializer, SchemaFieldSerializer


class SchemaViewSet(viewsets.ModelViewSet):
    queryset = Schema.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)

    def get_serializer_class(self):
        if self.action == 'list':
            return SchemaBaseSerializer
        return SchemaSerializer


class SchemaFieldViewSet(viewsets.ModelViewSet):
    queryset = SchemaField.objects.all()
    serializer_class = SchemaFieldSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('schema',)
