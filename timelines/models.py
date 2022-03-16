from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ProjectModelMixin


class Timeline(ProjectModelMixin):

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

    class Meta:
        verbose_name = _('Timeline')
        verbose_name_plural = _('Timelines')
        ordering = ('id', )

    def __str__(self):
        return self.name


class TimelineItem(models.Model):

    timeline = models.ForeignKey(
        'timelines.Timeline',
        on_delete=models.CASCADE,
    )

    stream = models.CharField(
        _('stream'),
        max_length=200,
    )

    key = models.CharField(
        _('key'),
        max_length=200,
        null=True,
        blank=True,
    )

    description = models.CharField(
        _('Description'),
        max_length=400,
        null=True,
        blank=True,
    )

    ordering = models.IntegerField(
        _('Ordering steps'),
        default=1,
    )

    title_field = models.CharField(
        _('Title fields'),
        max_length=200,
    )

    description_field = models.CharField(
        _('Description fields'),
        max_length=400,
    )

    class Meta:
        verbose_name = _('TimelineItem')
        verbose_name_plural = _('TimelineItems')
        ordering = ('id', )

    def __str__(self):
        return self.stream
