from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from core.models import ProjectModelMixin


class KPI(ProjectModelMixin):
    TYPE_COUNTER = 'kpi_type_counter'
    TYPE_MEASUREMENT = 'kpi_type_measurement'
    TYPE_CHOICES = (
        (TYPE_COUNTER, 'Counter'),
        (TYPE_MEASUREMENT, 'Measurement'),
    )

    category = models.CharField(
        _('Name'),
        max_length=200,
    )

    metric = models.CharField(
        _('Description'),
        max_length=400,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    indicator_type = models.CharField(
        _('Indicator Type'),
        max_length=30,
        choices=TYPE_CHOICES,
        default=TYPE_COUNTER,
    )

    class Meta:
        verbose_name = _('KPI')
        verbose_name_plural = _('KPIs')
        ordering = ('id', )

    def __str__(self):
        return self.category
