from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = (
        "team_name",
        "user",
        "remaining_coins",
        "is_active",
    )

    search_fields = (
        "team_name",
        "user__username",
        "user__email",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "team_name",
    )