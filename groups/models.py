from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from core.models import ProjectModelMixin
from django.utils.translation import gettext_lazy as _


class GroupBase(ProjectModelMixin):
    name = models.CharField(max_length=200, null=False)
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )
    sort_order = models.IntegerField(default=0)

    class Meta:
        abstract = True


class StreamGroup(GroupBase):
    organisation = models.ForeignKey(
        "account.Organisation", on_delete=models.CASCADE, null=True, blank=True
    )
    is_organisation_shared = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = _("Stream Group")
        verbose_name_plural = _("Stream Groups")
        ordering = ("sort_order",)
        constraints = [
            UniqueConstraint(
                fields=["project", "name"], name="unique_project_stream_group"
            )
        ]

    def __str__(self):
        return self.name


class StreamProcessorGroup(GroupBase):
    class Meta:
        verbose_name = _("Stream Processor Group")
        verbose_name_plural = _("Stream Processor Groups")
        ordering = ("sort_order",)
        constraints = [
            UniqueConstraint(
                fields=["project", "name"], name="unique_project_streamprocessor_group"
            )
        ]

    def __str__(self):
        return self.name


class SimulationGroup(GroupBase):
    class Meta:
        verbose_name = _("Simulation Groups")
        verbose_name_plural = _("Simulation Groups")
        ordering = ("sort_order",)
        constraints = [
            UniqueConstraint(
                fields=["project", "name"], name="unique_project_simulation_group"
            )
        ]

    def __str__(self):
        return self.name
