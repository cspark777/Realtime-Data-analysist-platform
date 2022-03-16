from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from kpis.models import KPI
from kpis.api.serializers import KPISerializer
from streamprocessors.utils import choice_to_value_name


class KPIViewSet(viewsets.ModelViewSet):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)

    @action(methods=['get'], detail=False, url_path='indicator-types')
    def get_indicator_types(self, request, *args, **kwargs):
        data = {'indicator_types': choice_to_value_name(KPI.TYPE_CHOICES)}
        return Response(data=data, status=status.HTTP_200_OK)
