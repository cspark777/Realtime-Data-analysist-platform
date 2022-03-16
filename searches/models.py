from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ProjectModelMixin


class Search(ProjectModelMixin):
    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    stream = models.CharField(
        _('Stream'),
        max_length=200,
    )

    time_window = models.CharField(
        _('Time Window'),
        max_length=200,
        default='1 hour',
        blank=True
    )

    search_data = models.TextField(
        _('Search Data'),
        blank=True
    )

    def __str__(self):
        return self.name
