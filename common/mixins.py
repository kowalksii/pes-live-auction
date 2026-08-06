from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from accounts.models import User, UserRole


class ApprovedParticipantRequiredMixin(LoginRequiredMixin):
    """
    Allows only approved participants.
    """

    def dispatch(self, request, *args, **kwargs):

        user = request.user

        if user.role != UserRole.PARTICIPANT:
            raise PermissionDenied(
                "Only approved participants can access this page."
            )

        if not user.is_approved:
            raise PermissionDenied(
                "Your account has not been approved yet."
            )

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(LoginRequiredMixin):
    """
    Allows only administrators.
    """

    def dispatch(self, request, *args, **kwargs):

        if request.user.role != UserRole.ADMIN:
            raise PermissionDenied(
                "Only administrators can access this page."
            )

        return super().dispatch(request, *args, **kwargs)