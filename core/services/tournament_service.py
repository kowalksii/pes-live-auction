from django.core.exceptions import ValidationError

from core.models import (
    Tournament,
    TournamentStatus,
    AuctionRoomStatus,
    AuctionEngineStatus,
)


class TournamentService:
    """
    Service layer for Tournament-related business logic.
    """

    @staticmethod
    def create_tournament(**validated_data) -> Tournament:
        return Tournament.objects.create(**validated_data)

    @staticmethod
    def update_tournament(
        tournament: Tournament,
        **validated_data,
    ) -> Tournament:

        for field, value in validated_data.items():
            setattr(tournament, field, value)

        tournament.save()

        return tournament

    @staticmethod
    def open_auction_room(
        tournament: Tournament,
    ) -> Tournament:
        """
        Open the auction room so tournament members
        can request entry into the live auction.
        """

        if tournament.status != TournamentStatus.AUCTION:
            raise ValidationError(
                "Auction room can only be opened during the auction phase."
            )

        if (
            tournament.auction_room_status
            == AuctionRoomStatus.OPEN
        ):
            raise ValidationError(
                "Auction room is already open."
            )

        tournament.auction_room_status = (
            AuctionRoomStatus.OPEN
        )

        tournament.save(
            update_fields=["auction_room_status"]
        )

        return tournament

    @staticmethod
    def close_auction_room(
        tournament: Tournament,
    ) -> Tournament:
        """
        Close the auction room.
        """

        if (
            tournament.auction_room_status
            == AuctionRoomStatus.CLOSED
        ):
            raise ValidationError(
                "Auction room is already closed."
            )

        if (
            tournament.auction_engine_status
            == AuctionEngineStatus.RUNNING
        ):
            raise ValidationError(
                "Cannot close the room while the auction is running."
            )

        tournament.auction_room_status = (
            AuctionRoomStatus.CLOSED
        )

        tournament.save(
            update_fields=["auction_room_status"]
        )

        return tournament

    @staticmethod
    def start_auction(
        tournament: Tournament,
    ) -> Tournament:
        """
        Start the live auction.
        """

        if tournament.status != TournamentStatus.AUCTION:
            raise ValidationError(
                "Tournament is not in the auction phase."
            )

        if (
            tournament.auction_room_status
            != AuctionRoomStatus.OPEN
        ):
            raise ValidationError(
                "Open the auction room before starting the auction."
            )

        if (
            tournament.auction_engine_status
            == AuctionEngineStatus.RUNNING
        ):
            raise ValidationError(
                "Auction is already running."
            )

        if (
            tournament.auction_engine_status
            == AuctionEngineStatus.FINISHED
        ):
            raise ValidationError(
                "Auction has already finished."
            )

        tournament.auction_engine_status = (
            AuctionEngineStatus.RUNNING
        )

        tournament.save(
            update_fields=["auction_engine_status"]
        )

        return tournament

    @staticmethod
    def pause_auction(
        tournament: Tournament,
    ) -> Tournament:
        """
        Pause the running auction.
        """

        if (
            tournament.auction_engine_status
            != AuctionEngineStatus.RUNNING
        ):
            raise ValidationError(
                "Auction is not running."
            )

        tournament.auction_engine_status = (
            AuctionEngineStatus.PAUSED
        )

        tournament.save(
            update_fields=["auction_engine_status"]
        )

        return tournament

    @staticmethod
    def resume_auction(
        tournament: Tournament,
    ) -> Tournament:
        """
        Resume a paused auction.
        """

        if (
            tournament.auction_engine_status
            != AuctionEngineStatus.PAUSED
        ):
            raise ValidationError(
                "Auction is not paused."
            )

        tournament.auction_engine_status = (
            AuctionEngineStatus.RUNNING
        )

        tournament.save(
            update_fields=["auction_engine_status"]
        )

        return tournament

    @staticmethod
    def finish_auction(
        tournament: Tournament,
    ) -> Tournament:
        """
        Finish the auction.
        """

        if (
            tournament.auction_engine_status
            == AuctionEngineStatus.FINISHED
        ):
            raise ValidationError(
                "Auction is already finished."
            )

        tournament.auction_engine_status = (
            AuctionEngineStatus.FINISHED
        )

        tournament.status = TournamentStatus.COMPLETED

        tournament.auction_room_status = (
            AuctionRoomStatus.CLOSED
        )

        tournament.save(
            update_fields=[
                "auction_engine_status",
                "auction_room_status",
                "status",
            ]
        )

        return tournament