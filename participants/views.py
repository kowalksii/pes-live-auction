from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.core.exceptions import ValidationError

from common.mixins import ApprovedParticipantRequiredMixin

from core.models import Tournament

from .services.membership import TournamentMembershipService


class JoinTournamentView(ApprovedParticipantRequiredMixin, View):

    def post(self, request, pk):
    
        tournament = get_object_or_404(
            Tournament,
            pk=pk,
        )
    
        try:
            TournamentMembershipService.join_tournament(
                user=request.user,
                tournament=tournament,
            )
    
            messages.success(
                request,
                "You have successfully joined the tournament.",
            )
    
        except ValidationError as exc:
            messages.error(
                request,
                exc.message,
            )
    
        return redirect(
            "core:tournament_detail",
            pk=tournament.pk,
        )