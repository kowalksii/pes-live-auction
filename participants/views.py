from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.views.generic import FormView

from common.mixins import ApprovedParticipantRequiredMixin

from core.models import Tournament, AuctionRoomStatus, TournamentStatus
from .forms import AuctionJoinRequestForm
from .models import TournamentMembership
from .services.auction_request import AuctionJoinRequestService

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

class RequestAuctionEntryView(FormView):

    template_name = "participants/request_auction_entry.html"

    form_class = AuctionJoinRequestForm

    def dispatch(self, request, *args, **kwargs):

        self.tournament = get_object_or_404(
            Tournament,
            pk=kwargs["pk"],
        )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["tournament"] = self.tournament

        return context

    def form_valid(self, form):

        membership = get_object_or_404(
            TournamentMembership,
            tournament=self.tournament,
            user=self.request.user,
            is_active=True,
        )

        if (
            self.tournament.status
            != TournamentStatus.AUCTION
        ):
            messages.error(
                self.request,
                "Auction has not started yet.",
            )

            return redirect(
                "core:tournament_detail",
                self.tournament.pk,
            )

        if (
            self.tournament.auction_room_status
            != AuctionRoomStatus.OPEN
        ):
            messages.error(
                self.request,
                "Auction room is not open.",
            )

            return redirect(
                "core:tournament_detail",
                self.tournament.pk,
            )

        try:

            AuctionJoinRequestService.create_request(
                membership=membership,
                team_name=form.cleaned_data["team_name"],
            )

            messages.success(
                self.request,
                "Auction entry request submitted successfully.",
            )

        except Exception as exc:

            messages.error(
                self.request,
                str(exc),
            )

        return redirect(
            "core:tournament_detail",
            self.tournament.pk,
        )