from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class Participant(TimeStampedModel):
    """
    Auction participant profile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_profile",
    )

    team_name = models.CharField(
        max_length=100,
        unique=True,
    )

    initial_coins = models.PositiveIntegerField(
        default=1000,
    )

    remaining_coins = models.PositiveIntegerField(
        default=1000,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["team_name"]

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.remaining_coins = self.initial_coins

        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name