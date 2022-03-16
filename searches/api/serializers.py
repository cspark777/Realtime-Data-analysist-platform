from rest_framework import serializers

from searches.models import Search


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = (
            'id',
            'name',
        )
