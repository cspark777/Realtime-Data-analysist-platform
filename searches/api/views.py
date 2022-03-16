from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from searches.models import Search
from searches.api.serializers import SearchSerializer


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)
