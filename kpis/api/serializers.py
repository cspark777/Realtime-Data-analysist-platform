from rest_framework import serializers

from kpis.models import KPI


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = (
            'id',
            'project',
            'category',
            'metric',
            'indicator_type',
        )
