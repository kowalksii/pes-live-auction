from django.conf import settings
from django.db import models

from common.models import TimeStampedModel

class AuctionRoomStatus(models.TextChoices):
    CLOSED = "CLOSED", "Closed"
    OPEN = "OPEN", "Open"


class AuctionEngineStatus(models.TextChoices):
    NOT_STARTED = "NOT_STARTED", "Not Started"
    RUNNING = "RUNNING", "Running"
    PAUSED = "PAUSED", "Paused"
    FINISHED = "FINISHED", "Finished"

class TournamentStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    REGISTRATION = "REGISTRATION", "Registration Open"
    AUCTION = "AUCTION", "Live Auction"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"



class Tournament(TimeStampedModel):
    """
    Represents one tournament.

    Every participant, bid and purchased player belongs
    to exactly one Tournament.
    """

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    total_coins = models.PositiveIntegerField(
        default=500,
    )

    max_participants = models.PositiveIntegerField(
        default=10,
    )

    status = models.CharField(
        max_length=20,
        choices=TournamentStatus.choices,
        default=TournamentStatus.DRAFT,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_tournaments",
    )
    auction_start_time = models.DateTimeField(
    null=True,
    blank=True,
    help_text="Scheduled start time of the auction.",
    )

    auction_room_status = models.CharField(
        max_length=20,
        choices=AuctionRoomStatus.choices,
        default=AuctionRoomStatus.CLOSED,
    )

    auction_engine_status = models.CharField(
        max_length=20,
        choices=AuctionEngineStatus.choices,
        default=AuctionEngineStatus.NOT_STARTED,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name