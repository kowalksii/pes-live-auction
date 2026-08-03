from django.core.exceptions import ValidationError

from core.models import TournamentStatus
from participants.models import TournamentMembership


class TournamentMembershipService:
    """
    Business logic for tournament memberships.
    """

    @staticmethod
    def join_tournament(*, user, tournament):
        """
        Join a tournament if all business rules are satisfied.
        """

        # Rule 1: Tournament must be open for registration
        if tournament.status == TournamentStatus.DRAFT:
            raise ValidationError(
                "Tournament registration has not opened yet."
            )
        
        if tournament.status == TournamentStatus.AUCTION:
            raise ValidationError(
                "The auction has already started."
            )
        
        if tournament.status == TournamentStatus.COMPLETED:
            raise ValidationError(
                "This tournament has already been completed."
            )
        
        if tournament.status == TournamentStatus.CANCELLED:
            raise ValidationError(
                "This tournament has been cancelled."
            )
        
        # Rule 2: User cannot join twice
        membership = TournamentMembership.objects.filter(
            user=user,
            tournament=tournament,
            is_active=True,
        ).first()

        if membership:
            raise ValidationError(
                "You have already joined this tournament."
            )

        # Rule 3: Reactivate previous inactive membership if it exists
        membership = TournamentMembership.objects.filter(
            user=user,
            tournament=tournament,
            is_active=False,
        ).first()

        if membership:
            membership.is_active = True
            membership.save(update_fields=["is_active"])
            return membership

        # Rule 4: Create a new membership
        return TournamentMembership.objects.create(
            user=user,
            tournament=tournament,
            is_active=True,
        )

    @staticmethod
    def leave_tournament(membership):
        """
        Leave a tournament.
        """

        membership.is_active = False
        membership.save(update_fields=["is_active"])