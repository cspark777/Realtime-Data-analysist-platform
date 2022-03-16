from rest_framework import serializers

from functions.models import Function, FunctionEndpoint


class FunctionEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionEndpoint
        fields = (
            'id',
            'name',
            'Function',
        )


class FunctionSerializer(serializers.ModelSerializer):
    functionendpoint_set = FunctionEndpointSerializer(many=True, read_only=True)

    class Meta:
        model = Function
        fields = (
            'id',
            'name',
            'functionendpoint_set',
        )
