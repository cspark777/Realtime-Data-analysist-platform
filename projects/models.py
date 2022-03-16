import secrets
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from core.models import ProjectModelMixin


class Project(models.Model):

    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        null=True,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    is_current = models.BooleanField(
        _('Is Current Project?'),
        default=True,
    )

    project_key = models.CharField(
        _('project_key'),
        max_length=64,
        default=secrets.token_hex,
    )

    druid_url = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    cluster_type = models.CharField(
        max_length=256,
        default="Docker Swarm"
    )
    cluster_endpoint = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    kafka_url = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('id', )

    def __str__(self):
        return self.name
