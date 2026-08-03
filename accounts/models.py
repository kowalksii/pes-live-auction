from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import TimeStampedModel


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    PARTICIPANT = "PARTICIPANT", "Participant"


class User(AbstractUser, TimeStampedModel):

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PARTICIPANT,
    )

    is_approved = models.BooleanField(default=False)

    is_online = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if self.is_superuser:
            self.role = UserRole.ADMIN
            self.is_approved = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username