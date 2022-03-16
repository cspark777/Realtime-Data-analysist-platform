from abc import ABC

from rest_framework import serializers

from account.models import CustomUser, Organisation
from functions.models import Function, FunctionEndpoint
from projects.models import Project
from simulations.models import Simulation
from streamprocessors.models import StreamProcessor
from streams.models import Stream


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "developer_key",
            "organisation_owner",
            "organisation",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = [
            "default_druid_url",
            "default_cluster_type",
            "default_cluster_endpoint",
            "default_kafka_url",
            "kafka_url_public",
        ]


class EntityReorder(serializers.Serializer):
    sort_order = serializers.IntegerField(required=True)
    group = serializers.IntegerField(required=True, allow_null=True)
    id = serializers.IntegerField(required=True)
    items = serializers.ListField(required=False)


class ConfigSerializer(serializers.Serializer):
    KAFKA_URL = serializers.CharField()
    DRUID_URL = serializers.CharField()
    project_id = serializers.IntegerField()


class StreamSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(
        read_only=True, required=False, help_text="User who made stream."
    )

    project = ProjectSerializer(
        read_only=True, required=False, help_text="Project associated with this stream"
    )

    class Meta:
        model = Stream
        fields = [
            "id",
            "name",
            "display_name",
            "description",
            "is_countable",
            "share",
            "retention_period",
            "project",
            "created_by",
            "schema",
            "group",
            "sort_order"
        ]


class StreamProcessorSerializer(serializers.ModelSerializer):
    owning_user = CustomUserSerializer(
        read_only=True, required=False, help_text="User who made stream processor."
    )

    project = ProjectSerializer(
        read_only=True, required=False, help_text="Project associated with this stream"
    )

    class Meta:
        model = StreamProcessor
        fields = "__all__"


class SimulationSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(
        read_only=True, required=False, help_text="User who made stream processor"
    )

    project = ProjectSerializer(
        read_only=True, required=False, help_text="Project associated with this stream"
    )

    class Meta:
        model = Simulation
        fields = "__all__"


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = "__all__"


class FunctionEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionEndpoint
        fields = "__all__"
