from rest_framework import serializers

from streams.models import Stream


class StreamBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = (
            'id',
            'name',
            'display_name',
            'schema',
        )


class StreamSerializer(StreamBaseSerializer):
    class Meta(StreamBaseSerializer.Meta):
        model = Stream
        depth = 1
        fields = StreamBaseSerializer.Meta.fields + (
            'project',
            'description',
            'created_by',
            'schema',
            'is_countable',
            'share',
            'retention_period',
        )
