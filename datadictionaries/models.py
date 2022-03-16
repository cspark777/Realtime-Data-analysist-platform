from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core.models import ProjectModelMixin


class DataDictionary(ProjectModelMixin):
    name = models.CharField(
        _('Name'),
        max_length=32,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def to_dict(self):
        return {item.source_value: item.mapped_value for item in self.items.all()}

    def __str__(self):
        return self.name


class DataItem(models.Model):
    source_value = models.CharField(
        _('Source value'),
        unique=True,
        max_length=64,
    )

    mapped_value = models.CharField(
        _('Mapped value'),
        max_length=64,
    )

    datadictionary = models.ForeignKey(
        DataDictionary,
        related_name='items',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.source_value
