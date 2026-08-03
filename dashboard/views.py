from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import UserRole


@login_required
def dashboard_redirect(request):

    if request.user.role == UserRole.ADMIN:
        return render(
            request,
            "dashboard/admin_dashboard.html",
        )

    return render(
        request,
        "dashboard/participant_dashboard.html",
    )