from django.contrib import admin

from .models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "max_participants",
        "total_coins",
        "created_by",
        "created_at",
    )

    list_filter = (
        "status",
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
                )
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