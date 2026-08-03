from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from accounts.models import User


class ApprovedParticipantRequiredMixin(LoginRequiredMixin):
    """
    Allows only approved participants.
    """

    def dispatch(self, request, *args, **kwargs):

        user = request.user

        if user.role != User.UserRole.PARTICIPANT:
            raise PermissionDenied

        if not user.is_approved:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(LoginRequiredMixin):
    """
    Allows only administrators.
    """

    def dispatch(self, request, *args, **kwargs):

        if request.user.role != User.UserRole.ADMIN:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)