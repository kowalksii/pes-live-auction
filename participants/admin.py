from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Participant, TournamentMembership


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = (
        "team_name",
        "tournament",
        "user",
        "remaining_coins",
        "is_active",
    )

    search_fields = (
        "team_name",
        "tournament__name",
        "user__username",
        "user__email",
    )

    list_filter = (
        "tournament",
        "is_active",
    )

    ordering = (
        "team_name",
    )

@admin.register(TournamentMembership)
class TournamentMembershipAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "tournament",
        "is_active",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "tournament__name",
    )

    list_filter = (
        "tournament",
        "is_active",
    )

    ordering = (
        "tournament",
        "user",
    )