from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "role",
        "is_approved",
        "is_online",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_approved",
        "is_staff",
        "is_superuser",
    )

    actions = (
        "approve_users",
        "revoke_users",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Auction Information",
            {
                "fields": (
                    "role",
                    "is_approved",
                    "is_online",
                )
            },
        ),
    )

    @admin.action(description="Approve selected participants")
    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Revoke selected participants")
    def revoke_users(self, request, queryset):
        queryset.update(is_approved=False)