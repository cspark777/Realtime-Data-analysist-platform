from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import ProjectModelMixin, GroupMixin
from groups.models import SimulationGroup, StreamGroup


class Stream(GroupMixin):
    name = models.CharField(
        max_length=200,
        null=False,
    )

    display_name = models.CharField(
        max_length=200,
        null=True,
    )

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

    schema = models.ForeignKey(
        'schemas.Schema',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    is_countable = models.BooleanField(
        default=False,
        verbose_name="Archive The Stream For Later Analysis"
    )

    share = models.BooleanField(
        default=False,
        verbose_name="Share This Stream With Other Members Of My Organisation"
    )

    retention_period = models.CharField(
        max_length=200,
        null=True,
    )

    group = models.ForeignKey("groups.StreamGroup", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Stream')
        verbose_name_plural = _('Streams')
        ordering = ('sort_order',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = f'{self.project_id}_{self.created_by_id}_{self.display_name.strip().replace(" ", "_")}'
        super(Stream, self).save(*args, **kwargs)
