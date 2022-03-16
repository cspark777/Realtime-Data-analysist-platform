from rest_framework import serializers

from groups.api.serializers import StreamProcessorGroupSerializer
from streamprocessors.models import StreamProcessor, StreamProcessorStep, WorkflowTask


class WorkflowTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowTask
        fields = (
            'id',
            'title',
            'description',
            'recipient',
            'type',
            'streamprocessor_step',
        )


class StreamProcessorStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamProcessorStep
        fields = '__all__'

    def update(self, instance, validated_data):
        if instance.steptype != validated_data.get('steptype'):
            instance.get_children().delete()
        super().update(instance, validated_data)
        return instance


class StreamProcessorBlockStepSerializer(StreamProcessorStepSerializer):
    blocks = StreamProcessorStepSerializer(source='children', many=True)
    workflow_task = WorkflowTaskSerializer(source='workflowtask_set', many=True)

    class Meta(StreamProcessorStepSerializer.Meta):
        fields = StreamProcessorStepSerializer.Meta.fields


class StreamProcessorBaseSerializer(serializers.ModelSerializer):
    group = StreamProcessorGroupSerializer(required=False)

    class Meta:
        model = StreamProcessor
        fields = (
            'id',
            'project',
            'name',
            'description',
            'replicas',
            'owning_user',
            'group',
            'sort_order',
        )


class StreamProcessorSerializer(StreamProcessorBaseSerializer):
    streamprocessorstep_set = StreamProcessorBlockStepSerializer(many=True, read_only=True)

    class Meta(StreamProcessorBaseSerializer.Meta):
        fields = StreamProcessorBaseSerializer.Meta.fields + (
            'streamprocessorstep_set',
        )

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['owning_user'] = user
        streamprocessor = super().create(validated_data)
        return streamprocessor


class SelectChoiceSerializer(serializers.Serializer):
    step_types_data = serializers.DictField()
    step_types = serializers.ListField()
    increment_key_types = serializers.ListField()
    update_key_types = serializers.ListField()
