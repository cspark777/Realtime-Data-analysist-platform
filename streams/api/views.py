from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from streams.models import Stream
from streams.api.serializers import StreamBaseSerializer, StreamSerializer


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('project',)

    def get_serializer_class(self):
        if self.action == 'list':
            return StreamBaseSerializer
        return StreamSerializer
