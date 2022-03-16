from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from groups.api.serializers import (
    StreamGroupSerializer,
    SimulationGroupSerializer,
    StreamProcessorGroupSerializer,
)
from groups.models import StreamGroup, SimulationGroup, StreamProcessorGroup
from streams.models import Stream

ORGANISATION_SHARED_STREAMS = "Organisation Shared Streams"


class StreamGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = StreamGroup.objects.all()
    serializer_class = StreamGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]

    def list(self, request, *args, **kwargs):
        project = self.request.query_params.get("project")

        shared_streams = Stream.objects.filter(
            created_by__organisation=self.request.user.organisation
        ).filter(share=True)

        # shared_streams = Stream.objects.filter(share=True)

        organisation_group, created = StreamGroup.objects.get_or_create(
            name=ORGANISATION_SHARED_STREAMS,
            is_organisation_shared=True,
            organisation=self.request.user.organisation,
        )

        if created:
            for stream in shared_streams:
                stream.group = organisation_group

            Stream.objects.bulk_update(shared_streams, ["group"])

        qs = self.queryset
        if project:
            qs = self.queryset.filter(
                Q(name=ORGANISATION_SHARED_STREAMS) | Q(project=project)
            )

        if not shared_streams.exists():
            qs = self.queryset.filter(Q(project=project))

        serializer = self.serializer_class(qs, many=True)

        return Response(serializer.data)


class SimulationGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = SimulationGroup.objects.all()
    serializer_class = SimulationGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]


class StreamProcessorGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = StreamProcessorGroup.objects.all()
    serializer_class = StreamProcessorGroupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]
