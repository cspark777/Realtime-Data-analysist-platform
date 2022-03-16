from rest_framework import serializers

from schemas.models import Schema, SchemaField


class SchemaFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemaField
        fields = (
            'id',
            'name',
            'description',
            'type_field',
            'required',
            'categorical',
            'schema',
        )


class SchemaBaseSerializer(serializers.ModelSerializer):
    schemafield_set = SchemaFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Schema
        fields = (
            'id',
            'name',
            'schemafield_set',
        )


class SchemaSerializer(SchemaBaseSerializer):
    class Meta(SchemaBaseSerializer.Meta):
        fields = SchemaBaseSerializer.Meta.fields + (
            'project',
            'description',
        )
