from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ProjectModelMixin


class Function(ProjectModelMixin):

    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    docker_image = models.CharField(
        _('Docker Image'),
        max_length=120
    )

    class Meta:
        verbose_name = _('Function')
        verbose_name_plural = _('Functions')
        ordering = ('id', )

    def __str__(self):
        return self.name


class FunctionEndpoint(models.Model):

    name = models.CharField(
        _('Field Name'),
        max_length=200,
    )

    inbound_schema = models.ForeignKey(
        'schemas.Schema',
        on_delete=models.CASCADE,
        related_name='inbound_schema_set',
    )

    outbound_schema = models.ForeignKey(
        'schemas.Schema',
        on_delete=models.CASCADE,
        related_name='outbound_schema_set',
    )

    Function = models.ForeignKey(
        'functions.Function',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('FunctionEndpoint')
        verbose_name_plural = _('FunctionEndpoint')
        ordering = ('id', )

    def __str__(self):
        return self.name
