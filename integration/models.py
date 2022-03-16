import os

from django.contrib.postgres.fields import JSONField
from django.db import models

from core.models import ProjectModelMixin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class DataSource(ProjectModelMixin):
    TAIL_CSV = "TailCSV"
    TAIL_JSON = "TailJSON"
    KAFKA = "Kafka"
    S3 = "S3"
    SOURCE_TYPES = (
        (TAIL_CSV, "Tail CSV"),
        (TAIL_JSON, "Tail JSON"),
        (S3, "S3"),
        (KAFKA, "Kafka"))
    
    stream = models.ForeignKey(
        'streams.Stream',
        on_delete=models.CASCADE,

    )

    name = models.CharField(
        max_length=200,
        null=False,)

    description = models.TextField(
        blank=True,
        null=True,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    source_type = models.CharField(
        max_length=200,
        choices=SOURCE_TYPES,
        null=False,
    )

    def __str__(self):
        return self.name


class ImportData(ProjectModelMixin):

    NEW = 'new'
    EXISTING = 'existing'

    SCHEMA_CHOICES = (
        (NEW, 'New Event Definition'),
        (EXISTING, 'Existing Event Definition'),
    )

    json = JSONField(
        _('Table Data'),
        null=True,
    )

    headers = JSONField(
        _('Table Headers'),
        null=True,
    )

    file = models.FileField(
        _('JSON/CSV File'),
        upload_to='files',
        null=True,
    )

    content_type = models.CharField(
        _('Content Type'),
        max_length=100,
        null=True,
    )

    count = models.PositiveIntegerField(
        _('Table Data Count'),
        default=0,
    )

    stream_data = JSONField(
        _('Map Data To Definition Fields'),
        null=True,
    )

    use_schema = models.CharField(
        _('Destination Of New Or Existing Definition'),
        max_length=100,
        choices=SCHEMA_CHOICES,
        default=NEW,
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Import Data')
        verbose_name_plural = _('Import Data')
        ordering = ('id', )

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'Import data for user [{self.user_id}]'
