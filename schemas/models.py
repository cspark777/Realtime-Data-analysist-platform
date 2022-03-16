from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ProjectModelMixin


class Schema(ProjectModelMixin):

    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemas')
        ordering = ('id', )

    def __str__(self):
        return self.name

    def list_fields(self):
        return list(self.schemafield_set.values_list('name', flat=True))

    def to_druid_dimensions(self):
        dimensions = [{'type': 'long' if field.type_field == 'int' else field.type_field, 'name': field.name}
                      for field in self.schemafield_set.all()]
        dimensions.append({'type': 'string', 'name': 'uuid'})
        return dimensions


class SchemaField(models.Model):

    STR = 'string'
    INT = 'int'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    DATE = 'date'

    AVRO_TYPES = (
        (STR, 'String'),
        (INT, 'Integer'),
        (FLOAT, 'Float'),
        (BOOLEAN, 'Boolean'),
        (DATE, 'Date'),
    )

    CATEGORICAL = 'categorical'
    CONTINUOUS = 'continuous'
    CATEGORICAL_TYPES = (
        (CATEGORICAL, 'Categorical'),
        (CONTINUOUS, 'Continuous'),
    )

    name = models.CharField(
        _('Field Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    type_field = models.CharField(
        _('Type Field'),
        max_length=10,
        choices=AVRO_TYPES,
        default=STR,
    )

    required = models.BooleanField(
        _('Required'),
        default=False
    )

    categorical = models.CharField(
        _('Categorical'),
        max_length=30,
        choices=CATEGORICAL_TYPES,
        default=CATEGORICAL,
    )

    schema = models.ForeignKey(
        'schemas.Schema',
        on_delete=models.CASCADE,
     #   related_name='fields',
    )

    class Meta:
        verbose_name = _('SchemaField')
        verbose_name_plural = _('SchemaFields')
        ordering = ('id', )

    def __str__(self):
        return self.name
