from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class Participant(TimeStampedModel):
    """
    Auction participant profile.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participant_profile",
    )

    tournament = models.ForeignKey(
        "core.Tournament",
        on_delete=models.CASCADE,
        related_name="participants",
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

        constraints = [
            models.UniqueConstraint(
                fields=["tournament", "user"],
                name="unique_user_per_tournament",
            ),
            models.UniqueConstraint(
                fields=["tournament", "team_name"],
                name="unique_team_name_per_tournament",
            ),
        ]

    def save(self, *args, **kwargs):

        if self._state.adding:
            self.remaining_coins = self.initial_coins

        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name

class TournamentMembership(TimeStampedModel):
    """
    Represents a user's membership in a tournament.

    Membership allows users to join a tournament before
    requesting entry into the live auction.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tournament_memberships",
    )

    tournament = models.ForeignKey(
        "core.Tournament",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["tournament__name", "user__username"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "tournament"],
                name="unique_membership_per_tournament",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.tournament.name}"
    