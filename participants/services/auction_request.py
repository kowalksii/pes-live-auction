from django.core.exceptions import ValidationError
from django.db import transaction

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
                "This display name is already in use."
            )

        return AuctionJoinRequest.objects.create(
            membership=membership,
            team_name=team_name.strip(),
        )

    @staticmethod
    @transaction.atomic
    def approve_request(request_obj):
    
        if request_obj.status != AuctionJoinRequest.Status.PENDING:
            raise ValidationError(
                "Only pending requests can be approved."
            )
    
        membership = request_obj.membership
        tournament = membership.tournament
    
        participant, created = Participant.objects.get_or_create(
            tournament=tournament,
            user=membership.user,
            defaults={
                "team_name": request_obj.team_name,
                "initial_coins": tournament.total_coins,
                "remaining_coins": tournament.total_coins,
                "is_active": True,
                "is_connected": False,
                "joined_room_at": None,
            },
        )
    
        if not created:
            participant.team_name = request_obj.team_name
            participant.initial_coins = tournament.total_coins
            participant.remaining_coins = tournament.total_coins
            participant.is_active = True
            participant.is_connected = False
            participant.joined_room_at = None
    
            participant.save(
                update_fields=[
                    "team_name",
                    "initial_coins",
                    "remaining_coins",
                    "is_active",
                    "is_connected",
                    "joined_room_at",
                ]
            )
    
        request_obj.status = AuctionJoinRequest.Status.APPROVED
    
        request_obj.save(
            update_fields=[
                "status",
            ]
        )
    
        return participant
    
    @staticmethod
    def reject_request(
        request_obj,
        reason="",
    ):

        if request_obj.status != AuctionJoinRequest.Status.PENDING:
            raise ValidationError(
                "Only pending requests can be rejected."
            )

        request_obj.status = AuctionJoinRequest.Status.REJECTED
        request_obj.rejection_reason = reason

        request_obj.save(
            update_fields=[
                "status",
                "rejection_reason",
            ]
        )

        return request_obj