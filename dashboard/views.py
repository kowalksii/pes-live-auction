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

        return redirect("dashboard:participant")

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