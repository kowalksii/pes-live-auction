from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from common.mixins import ApprovedParticipantRequiredMixin

from core.models import Tournament, AuctionEngineStatus
from participants.models import Participant


class LiveAuctionRoomView(
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
            is_active=True,
        )

        if (
            tournament.auction_engine_status
            != AuctionEngineStatus.RUNNING
        ):
            return redirect(
                "participants:waiting_room",
                pk=tournament.pk,
            )

        return render(
            request,
            "auctions/live_room.html",
            {
                "tournament": tournament,
                "participant": participant,
            },
        )