from django.db import models
from core.models import ProjectModelMixin
from django.contrib.auth import get_user_model
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Collaboration(ProjectModelMixin):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
    )
    email = models.EmailField(
        _('email address'),
    )
    user = models.ForeignKey(
        get_user_model(),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    access_type = models.CharField(
        _('Type'),
        max_length=9,
        choices=CustomUser.ROLES,
        default=CustomUser.DEVELOPER,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_by"
    )

    class Meta:
        unique_together = ("email", "project")

    def __str__(self):
        return self.email
