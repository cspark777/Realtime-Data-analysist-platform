from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from functions.models import Function, FunctionEndpoint
from functions.api.serializers import FunctionSerializer, FunctionEndpointSerializer


class FunctionViewSet(viewsets.ModelViewSet):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)


class FunctionEndpointViewSet(viewsets.ModelViewSet):
    queryset = FunctionEndpoint.objects.all()
    serializer_class = FunctionEndpointSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('Function',)
