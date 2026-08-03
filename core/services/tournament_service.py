from core.models import Tournament


class TournamentService:
    """
    Service layer for Tournament-related business logic.
    """

    @staticmethod
    def create_tournament(**validated_data) -> Tournament:
        return Tournament.objects.create(**validated_data)

    @staticmethod
    def update_tournament(tournament: Tournament, **validated_data) -> Tournament:
        for field, value in validated_data.items():
            setattr(tournament, field, value)

        tournament.save()

        return tournament