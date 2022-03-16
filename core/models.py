from django.db import models


class ProjectModelMixin(models.Model):
    """
    Adds a Project Foreign Key field.
    """

    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, null=True, blank=True,
    )

    class Meta:
        abstract = True


class DateInfoModelMixin(models.Model):
    """
    Adds updated and added fields.
    """

    modified_at = models.DateTimeField(auto_now=True, )
    created_at = models.DateTimeField(auto_now_add=True, )

    class Meta:
        abstract = True
        get_latest_by = "created_at"


class GroupMixin(ProjectModelMixin):
    """Define the sort order of objects in a group"""

    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        abstract = True
