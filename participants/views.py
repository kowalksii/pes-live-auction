from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.core.exceptions import ValidationError
from django.views.generic import FormView

from common.mixins import ApprovedParticipantRequiredMixin, AdminRequiredMixin

from core.models import Tournament, AuctionRoomStatus, TournamentStatus, AuctionEngineStatus
from .forms import AuctionJoinRequestForm
from .models import TournamentMembership, AuctionJoinRequest, Participant
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

class PendingAuctionRequestListView(
    AdminRequiredMixin,
    FormView,
):
    template_name = "participants/pending_requests.html"
    form_class = AuctionJoinRequestForm

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        tournament = get_object_or_404(
            Tournament,
            pk=self.kwargs["pk"],
        )

        context["tournament"] = tournament

        context["requests"] = (
            AuctionJoinRequest.objects
            .filter(
                membership__tournament=tournament,
                status=AuctionJoinRequest.Status.PENDING,
            )
            .select_related(
                "membership",
                "membership__user",
            )
            .order_by("created_at")
        )

        return context

class ApproveAuctionRequestView(
    AdminRequiredMixin,
    View,
):

    def post(self, request, pk):

        request_obj = get_object_or_404(
            AuctionJoinRequest,
            pk=pk,
        )

        try:

            AuctionJoinRequestService.approve_request(
                request_obj
            )

            messages.success(
                request,
                "Participant approved successfully.",
            )

        except ValidationError as exc:

            messages.error(
                request,
                exc.message,
            )

        return redirect(
            "participants:pending_requests",
            request_obj.membership.tournament.pk,
        )

class RejectAuctionRequestView(
    AdminRequiredMixin,
    View,
):

    def post(self, request, pk):

        request_obj = get_object_or_404(
            AuctionJoinRequest,
            pk=pk,
        )

        try:

            AuctionJoinRequestService.reject_request(
                request_obj,
            )

            messages.success(
                request,
                "Request rejected.",
            )

        except ValidationError as exc:

            messages.error(
                request,
                exc.message,
            )

        return redirect(
            "participants:pending_requests",
            request_obj.membership.tournament.pk,
        )

class WaitingRoomView(
    ApprovedParticipantRequiredMixin,
    View,
):

    def get(self, request, pk):

        tournament = get_object_or_404(
            Tournament,
            pk=pk,
        )

        participant = get_object_or_404(
            Participant,
            tournament=tournament,
            user=request.user,
        )

        if (
            tournament.auction_engine_status
            == AuctionEngineStatus.RUNNING
        ):
            return redirect(
                "auctions:live_room",
                pk=tournament.pk,
            )

        approved_count = Participant.objects.filter(
            tournament=tournament,
            is_active=True,
        ).count()

        connected_count = Participant.objects.filter(
            tournament=tournament,
            is_connected=True,
        ).count()

        return render(
            request,
            "participants/waiting_room.html",
            {
                "tournament": tournament,
                "participant": participant,
                "approved_count": Participant.objects.filter(
                    tournament=tournament,
                    is_active=True,
                ).count(),
                "connected_count": Participant.objects.filter(
                    tournament=tournament,
                    is_connected=True,
                ).count(),
            },
        )

class AdminWaitingRoomView(
    AdminRequiredMixin,
    View,
):

    def get(self, request, pk):

        tournament = get_object_or_404(
            Tournament,
            pk=pk,
        )

        participants = (
            Participant.objects
            .filter(
                tournament=tournament,
                is_active=True,
            )
            .select_related("user")
            .order_by("team_name")
        )

        connected_count = participants.filter(
            is_connected=True,
        ).count()

        return render(
            request,
            "participants/admin_waiting_room.html",
            {
                "tournament": tournament,
                "participants": participants,
                "connected_count": connected_count,
                "total_count": participants.count(),
            },
        )