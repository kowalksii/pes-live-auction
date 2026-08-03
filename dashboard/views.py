from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from accounts.mixins import AdminRequiredMixin, ApprovedParticipantMixin
from accounts.models import UserRole


class DashboardRedirectView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        if request.user.role == UserRole.ADMIN:
            return redirect("dashboard:admin")

        if request.user.role == UserRole.PARTICIPANT:
            if not request.user.is_approved:
                return redirect("accounts:pending_approval")
            
            return redirect("dashboard:participant")
        return redirect("home")

class AdminDashboardView(
    LoginRequiredMixin,
    AdminRequiredMixin,
    TemplateView,
):

    template_name = "dashboard/admin_dashboard.html"


class ParticipantDashboardView(
    LoginRequiredMixin,
    ApprovedParticipantMixin,
    TemplateView,
):

    template_name = "dashboard/participant_dashboard.html"