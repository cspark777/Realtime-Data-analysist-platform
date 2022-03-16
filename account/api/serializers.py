from rest_framework import serializers

from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'organisation',
            'organisation_owner',
        )


class CustomUserEmailListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'name',
        )

    def get_name(self, obj):
        return f'{obj.first_name} {obj.last_name} < {obj.email} >'
