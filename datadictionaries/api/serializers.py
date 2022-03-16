from rest_framework import serializers

from datadictionaries.models import DataDictionary, DataItem


class DataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataItem
        fields = (
            'id',
            'source_value',
            'mapped_value',
            'datadictionary',
        )


class DataDictionaryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataDictionary
        fields = (
            'id',
            'name',
        )


class DataDictionarySerializer(DataDictionaryBaseSerializer):
    items = DataItemSerializer(many=True, read_only=True)

    class Meta(DataDictionaryBaseSerializer.Meta):
        fields = DataDictionaryBaseSerializer.Meta.fields + (
            'project',
            'description',
            'created_by',
            'items',
        )
