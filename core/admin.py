from django.contrib import admin

from .models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "auction_room_status",
        "auction_engine_status",
        "auction_start_time",
        "max_participants",
        "total_coins",
        "created_by",
        "created_at",
    )

    list_filter = (
        "status",
        "auction_room_status",
        "auction_engine_status",
        "created_at",
    )

    search_fields = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (
        (
            "Tournament Information",
            {
                "fields": (
                    "name",
                    "description",
                    "status",
                    "auction_start_time",
                )
            },
        ),
        (
            "Auction Control",
            {
                "fields": (
                    "auction_room_status",
                    "auction_engine_status",
                ),
                "description": (
                    "Development only. "
                    "Later these values will be controlled "
                    "through the application instead of the admin."
                ),
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "total_coins",
                    "max_participants",
                    "created_by",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )