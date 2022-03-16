from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from datadictionaries.models import DataDictionary, DataItem
from datadictionaries.api.serializers import DataDictionarySerializer, DataDictionaryBaseSerializer, DataItemSerializer


class DataDictionaryViewSet(viewsets.ModelViewSet):
    queryset = DataDictionary.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)

    def get_serializer_class(self):
        if self.action == 'list':
            return DataDictionaryBaseSerializer
        return DataDictionarySerializer


class DataItemViewSet(viewsets.ModelViewSet):
    queryset = DataItem.objects.all()
    serializer_class = DataItemSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('datadictionary',)
