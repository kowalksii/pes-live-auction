from django.core.exceptions import ValidationError

from participants.models import (
    AuctionJoinRequest,
    Participant,
)


class AuctionJoinRequestService:

    @staticmethod
    def create_request(
        membership,
        team_name,
    ):

        if AuctionJoinRequest.objects.filter(
            membership=membership,
            status=AuctionJoinRequest.Status.PENDING,
        ).exists():
            raise ValidationError(
                "You already have a pending auction request."
            )

        if Participant.objects.filter(
            tournament=membership.tournament,
            team_name__iexact=team_name,
        ).exists():
            raise ValidationError(
                "This team name is already in use."
            )

        return AuctionJoinRequest.objects.create(
            membership=membership,
            team_name=team_name.strip(),
        )