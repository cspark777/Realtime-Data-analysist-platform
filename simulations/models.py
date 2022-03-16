from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from core.models import ProjectModelMixin, GroupMixin
from groups.models import StreamProcessorGroup, SimulationGroup


class Simulation(GroupMixin):
    ONCE = 'once'
    COUNT = 'count'
    CONTINUOUSLY = 'continuously'
    TIME = 'time'
    RUN_TYPE_CHOICES = (
        (ONCE, 'Run Once'),
        (COUNT, 'Run Specified Number Of Times'),
        (CONTINUOUSLY, 'Run Continuously'),
        (TIME, 'Run For Specified Time Period (In Minutes)'),
    )

    STATIC_EVENT = 'static'
    UNIQUE_EVENT = 'unique'
    EVENT_TYPES = (
        (UNIQUE_EVENT, 'Generate Unique Messages On Each Run'),
        (STATIC_EVENT, 'Replay The Same Messages On Each Run'),
    )

    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )

    replicas = models.PositiveIntegerField(
        _('Count Of Replicas'),
        default=1,
    )

    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    run_count = models.PositiveIntegerField(
        _('Run Count'),
        default=1,
    )

    run_time = models.PositiveIntegerField(
        _('Run Time'),
        default=0,
    )

    run_type = models.CharField(
        _('Run Type'),
        max_length=100,
        choices=RUN_TYPE_CHOICES,
        default=ONCE,
    )

    type_event = models.CharField(
        _('Type Event'),
        max_length=6,
        choices=EVENT_TYPES,
        default=UNIQUE_EVENT,
    )

    is_running = models.BooleanField(
        _('Running'),
        default=False
    )

    completed = models.PositiveIntegerField(
        _('Counter of successful runs'),
        default=0,
    )

    group = models.ForeignKey("groups.SimulationGroup", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Simulation')
        verbose_name_plural = _('Simulations')
        ordering = ('id',)

    def __str__(self):
        return self.name


class Step(models.Model):
    STATIC = 'static'
    RANDOM = 'random'
    DELAY_CHOICES = (
        (STATIC, 'Static Value'),
        (RANDOM, 'Random Value'),
    )

    DEFINITION_JSON = 'definition_json'
    DEFINITION_SCHEMA = 'definition_schema'
    DEFINITION_CHOICES = (
        (DEFINITION_SCHEMA, 'From Schema'),
        (DEFINITION_JSON, 'JSON'),
    )

    name = models.CharField(
        _('Name'),
        max_length=200,
    )

    description = models.CharField(
        _('Description'),
        max_length=400,
    )

    topic = models.CharField(
        _('Topic'),
        max_length=200,
        null=True,
        blank=True,
    )

    event = models.CharField(
        _('Event description'),
        max_length=800,
        null=True,
        blank=True,
    )

    delay_type = models.CharField(
        _('Delay Type'),
        max_length=100,
        choices=DELAY_CHOICES,
        default=STATIC,
    )

    definition_type = models.CharField(
        _('Event definition type'),
        max_length=20,
        choices=DEFINITION_CHOICES,
        default=DEFINITION_SCHEMA
    )

    static_value = models.FloatField(
        _('Static Value'),
        default=0,
    )

    random_value = models.FloatField(
        _('Random Value'),
        default=0,
    )

    ordering = models.IntegerField(
        _('Ordering steps'),
        default=1,
    )

    simulation = models.ForeignKey(
        'simulations.Simulation',
        on_delete=models.CASCADE,
    )
    is_regexp = models.BooleanField(
        _('Is Regexp?'),
        default=False,
    )

    class Meta:
        verbose_name = _('Step')
        verbose_name_plural = _('Steps')
        ordering = ('id',)

    def __str__(self):
        return self.name
