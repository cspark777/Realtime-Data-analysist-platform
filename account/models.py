from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

import secrets
import uuid


class UserManager(BaseUserManager):
    """
    Define a model manager for User model with no username field.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    DEVELOPER = 'developer'
    USER = 'user'
    ROLES = (
        (DEVELOPER, 'Data Developer'),
        (USER, 'Data User'),
    )

    username = None

    first_name = models.CharField(
        _('first name'),
        max_length=30,
    )

    last_name = models.CharField(
        _('last name'),
        max_length=150,
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    role = models.CharField(
        _('Type'),
        max_length=9,
        choices=ROLES,
        default=DEVELOPER,
    )

    developer_key = models.CharField(
        _('developer key'),
        max_length=64,
        default=secrets.token_hex,
    )

    organisation = models.ForeignKey(
        'account.Organisation',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    organisation_owner = models.BooleanField(
        default=True
    )

    username_validator = None

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def save(self, *args, **kwargs):
        super(CustomUser, self).save(*args, **kwargs)
        self.developer_key = secrets.token_hex()


class Organisation(models.Model):
    """Organisation Model"""

    invite_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    company_name = models.CharField(
        _('company name'),
        max_length=200,
    )
    default_druid_url = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
    default_cluster_type = models.CharField(
        max_length=256,
        default="Docker Swarm"
    )
    default_cluster_endpoint = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        default="N/A"
    )
    default_kafka_url = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    kafka_url_public = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
