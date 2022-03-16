from django.db import IntegrityError
from rest_framework import serializers

from api.serializers import (
    CustomUserSerializer,
    StreamSerializer,
    SimulationSerializer,
    StreamProcessorSerializer,
)
from groups.models import StreamGroup, StreamProcessorGroup, SimulationGroup
from simulations.models import Simulation
from streamprocessors.models import StreamProcessor
from streams.models import Stream


class StreamGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(
        read_only=True, required=False, help_text="User who made stream."
    )

    streams = serializers.SerializerMethodField()

    def get_streams(self, obj):
        streams = Stream.objects.filter(group=obj).order_by("sort_order")
        return StreamSerializer(streams, many=True).data

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["created_by"] = user
        try:
            group = super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Group with the same name already exists."
            )

        return group

    class Meta:
        model = StreamGroup
        fields = "__all__"


class SimulationGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(
        read_only=True, required=False, help_text="User who made stream."
    )

    simulations = serializers.SerializerMethodField()

    def get_simulations(self, obj):
        streams = Simulation.objects.filter(group=obj).order_by("sort_order")
        return SimulationSerializer(streams, many=True).data

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["created_by"] = user
        try:
            group = super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Group with the same name already exists."
            )

        return group

    class Meta:
        model = SimulationGroup
        fields = "__all__"


class StreamProcessorGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(
        read_only=True, required=False, help_text="User who made stream."
    )

    streamprocessors = serializers.SerializerMethodField()

    def get_streamprocessors(self, obj):
        streamprocessors = StreamProcessor.objects.filter(group=obj).order_by(
            "sort_order"
        )
        return StreamProcessorSerializer(streamprocessors, many=True).data

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["created_by"] = user
        try:
            group = super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Group with the same name already exists."
            )

        return group

    class Meta:
        model = StreamProcessorGroup
        fields = "__all__"
