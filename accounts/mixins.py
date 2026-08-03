from django.contrib.auth.mixins import UserPassesTestMixin

from .models import UserRole


class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):

        return (
            self.request.user.is_authenticated
            and self.request.user.role == UserRole.ADMIN
        )


class ParticipantRequiredMixin(UserPassesTestMixin):

    def test_func(self):

        return (
            self.request.user.is_authenticated
            and self.request.user.role == UserRole.PARTICIPANT
        )


class ApprovedParticipantMixin(UserPassesTestMixin):

    def test_func(self):

        return (
            self.request.user.is_authenticated
            and self.request.user.role == UserRole.PARTICIPANT
            and self.request.user.is_approved
        )