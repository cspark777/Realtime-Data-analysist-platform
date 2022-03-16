import requests
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, APIException, NotFound
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import CustomUser, Organisation
from admin import settings
from api.serializers import (
    ConfigSerializer,
    StreamSerializer,
    StreamProcessorSerializer,
    FunctionSerializer,
    FunctionEndpointSerializer,
    SimulationSerializer,
    CustomUserSerializer,
    OrganisationSerializer,
    ProjectSerializer,
    EntityReorder,
)
from core.utils import get_database_data
from functions.models import Function, FunctionEndpoint
from functions.views import handle_function
from groups.models import StreamGroup
from projects.models import Project
from simulations.models import Simulation
from simulations.views.index import handle_simulation
from streamprocessors.druid_utils import get_payload_interval
from streamprocessors.models import StreamProcessor
from streamprocessors.views import (
    public_streamprocessor_run,
    public_streamprocessor_stop,
)
from streams.models import Stream


def get_project(request):
    developer_key = request.query_params.get("developer_key")
    project_key = request.query_params.get("project_key")

    if not developer_key:
        raise APIException("developer_key parameter is required", code=400)
    if not project_key:
        raise APIException("project_key parameter is required", code=400)

    try:
        user = CustomUser.objects.get(developer_key=developer_key)
    except CustomUser.DoesNotExist:
        raise NotFound("User not found")
    try:
        project = Project.objects.get(project_key=project_key)
    except Project.DoesNotExist:
        raise NotFound("Project not found")

    if project.created_by.id != user.id:
        raise PermissionDenied("You are note allowed to perform this action", code=403)

    return project


class ConfigDetail(RetrieveAPIView):
    serializer_class = ConfigSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ["get"]

    def get_object(self):
        project = get_project(self.request)
        return {
            "KAFKA_URL": project.kafka_url,
            "DRUID_URL": project.druid_url,
            "project_id": project.id,
        }


class Streams(ListAPIView):
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the streams for
        the user as determined by the developer_key portion of the query params.
        """
        project = get_project(self.request)

        return Stream.objects.filter(project=project.id)


class StreamProcessors(ListAPIView):
    serializer_class = StreamProcessorSerializer
    queryset = StreamProcessor.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the streamprocessors for
        the user as determined by the developer_key portion of the query params.
        """
        project = get_project(self.request)

        return StreamProcessor.objects.filter(project=project.id)


class StreamViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = StreamSerializer
    queryset = Stream.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]

    def list(self, request, **kwargs):
        project_id = request.query_params.get("project")

        if not project_id:
            raise APIException("project parameter is required", code=400)

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound("Project not found")

        streams = self.queryset.filter(project=project.id)
        shared_streams = self.queryset.filter(
            created_by__organisation=request.user.organisation
        ).filter(share=True)
        # shared_streams = self.queryset.filter(share=True)

        serializer = self.serializer_class(
            shared_streams.union(streams).order_by("sort_order"), many=True
        )
        return Response(serializer.data)

    def update_stream(self, data):
        try:
            stream = Stream.objects.get(pk=data["id"])
        except Stream.DoesNotExist:
            raise NotFound("Stream  not found.")

        is_shared_group = StreamGroup.objects.filter(
            pk=data["group"], is_organisation_shared=True
        ).exists()

        if is_shared_group:
            stream.share = True

        stream_serializer = StreamSerializer(stream, data=data, partial=True)

        if stream_serializer.is_valid():
            stream_serializer.save()

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        serializer = EntityReorder(data=request.data)
        serializer.is_valid(raise_exception=True)

        # update dragged item
        self.update_stream(data=serializer.data)

        # update sibling items
        with transaction.atomic():
            for item in serializer.data["items"]:
                self.update_stream(data=item)

        return Response(status=200)


class SimulationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SimulationSerializer
    queryset = Simulation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]

    def update_simulation(self, data):
        try:
            simulation = Simulation.objects.get(pk=data["id"])
        except Simulation.DoesNotExist:
            raise NotFound("Simulation  not found.")

        simulation_serializer = SimulationSerializer(
            simulation, data=data, partial=True
        )

        if simulation_serializer.is_valid():
            simulation_serializer.save()

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        serializer = EntityReorder(data=request.data)
        serializer.is_valid(raise_exception=True)

        # update dragged item
        self.update_simulation(data=serializer.data)

        # update sibling items
        with transaction.atomic():
            for item in serializer.data["items"]:
                self.update_simulation(data=item)

        return Response(status=200)


class StreamProcessorViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = StreamProcessorSerializer
    queryset = StreamProcessor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project"]

    def update_streamprocessor(self, data):
        try:
            streamprocessor = StreamProcessor.objects.get(pk=data["id"])
        except StreamProcessor.DoesNotExist:
            raise NotFound("Stream processor not found.")

        streamprocessor_serializer = StreamProcessorSerializer(
            streamprocessor, data=data, partial=True
        )

        if streamprocessor_serializer.is_valid():
            streamprocessor_serializer.save()

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        serializer = EntityReorder(data=request.data)
        serializer.is_valid(raise_exception=True)

        # update moved item
        self.update_streamprocessor(data=serializer.data)

        # update sibling items
        with transaction.atomic():
            for item in serializer.data["items"]:
                self.update_streamprocessor(data=item)

        return Response(status=200)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class UserView(RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        try:
            user = self.queryset.get(pk=self.request.user.pk)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")

        return user


class OrganisationView(RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update an organisation.
    """

    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.all()
    permission_classes = (AllowAny,)


class FunctionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows functions to be viewed or edited.
    """

    serializer_class = FunctionSerializer

    def get_permissions(self):
        return [permission() for permission in [AllowAny]]

    def get_queryset(self):
        project_id = None

        if self.action == "list":
            project_id = self.request.query_params.get("project_id")
            if not project_id:
                raise APIException("project_id param is required", code=400)

        if self.action == "create":
            project_id = self.request.data.get("project")
            if not project_id:
                raise APIException("project_id param is required", code=400)

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound("Project not found")

        return Function.objects.filter(project=project.id)


class FunctionEndpointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows function endpoints to be viewed or edited.
    """

    serializer_class = FunctionEndpointSerializer

    def get_permissions(self):
        print(self.request.data)
        return [permission() for permission in [AllowAny]]

    def get_queryset(self):
        function = None

        if self.action == "list":
            function = self.request.query_params.get("function")
            if not function:
                raise APIException("function param is required", code=400)

        if self.action == "create":
            function = self.request.data.get("Function")
            if not function:
                raise APIException("Function field is required", code=400)

        try:
            function = Function.objects.get(pk=function)
        except Function.DoesNotExist:
            raise NotFound("Function not found")

        return FunctionEndpoint.objects.filter(Function=function)


class StreamEventView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        event_count = 0
        try:
            stream = Stream.objects.get(id=request.query_params.get("stream"))
            payload = {
                "queryType": "timeseries",
                "dataSource": {"type": "table", "name": stream.name},
                "intervals": [get_payload_interval(default=True)],
                "granularity": {"type": "all"},
                "aggregations": [{"type": "count", "name": "cnt"}],
                "postAggregations": [],
            }
            druid_host, druid_port = get_database_data()
            response = requests.post(
                f"http://{druid_host}:{druid_port}/druid/v2/?pretty",
                headers={"Content-Type": "application/json"},
                json=payload,
            )

            if response.status_code == 200:
                try:
                    data = response.json()
                    count = data[0]["result"]["cnt"]
                    event_count = count
                except:
                    pass

        except Exception:
            pass

        return Response({"eventCount": event_count}, status=200)


class SiteConfigurationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        # Arseniy - Need to come from organisation record
        response = {
            "websocket_server": settings.WEBSOCKET_SERVER,
            "kafka_url": settings.KAFKA_URL,
            "kafka_url_public": settings.KAFKA_URL_PUBLIC,
            "druid_url": settings.DRUID_URL,
            "pivot_url": settings.PIVOT_URL,
            "superset_url": settings.SUPERSET,
            "jupyter_url": settings.JUPYTER_URL,
        }

        return Response(response, status=200)


class StreamProcessorActionView(APIView):
    permission_classes = (IsAuthenticated,)
    action = "run"

    def post(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        streamprocessor_id = request.data.get("streamprocessor_id")
        response = None

        if not project_id:
            raise APIException("project_id field is required", code=400)

        if not streamprocessor_id:
            raise APIException("streamprocessor_id field is required", code=400)

        if self.action == "run":
            status_code = public_streamprocessor_run(
                request, project_id, streamprocessor_id
            )
            response = {"status": "success" if status_code == 200 else "failed"}

        if self.action == "stop":
            status_code = public_streamprocessor_stop(
                request, project_id, streamprocessor_id
            )
            response = {"status": "success" if status_code == 200 else "failed"}

        return Response(response, status=200)


class SimulationActionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        simulation_id = request.data.get("simulation_id")

        if not project_id:
            raise APIException("project_id field is required", code=400)

        if not simulation_id:
            raise APIException("simulation_id field is required", code=400)

        response, status_runner = handle_simulation(request, project_id, simulation_id)
        status = response.status_code

        data = {
            "status": "success" if status == 200 else "failed",
            "status_runner": status_runner,
        }

        if status != 200:
            data["reason"] = response.json().get("reason")

        return Response(data, status=200)


class FunctionActionView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        function_id = request.data.get("function_id")

        if not project_id:
            raise APIException("project_id field is required", code=400)

        if not function_id:
            raise APIException("function_id field is required", code=400)

        try:
            function = Function.objects.get(pk=function_id)
        except Function.DoesNotExist:
            raise NotFound("Function not found")

        response = handle_function(request, project_id, function.docker_image)
        status = response.status_code

        data = {
            "status": "success" if status == 200 else "failed",
        }

        if status != 200:
            data["reason"] = response.json().get("reason")

        return Response(data, status=200)
