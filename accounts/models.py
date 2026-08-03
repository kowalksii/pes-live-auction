from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    PARTICIPANT = "PARTICIPANT", "Participant"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PARTICIPANT,
    )

    is_approved = models.BooleanField(default=False)

    is_online = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensure superusers always have the ADMIN role and are approved.
        """
        if self.is_superuser:
            self.role = UserRole.ADMIN
            self.is_approved = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username