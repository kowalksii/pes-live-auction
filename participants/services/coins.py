from participants.models import Participant


def update_remaining_coins(
    participant: Participant,
    amount: int,
):

    participant.remaining_coins = amount

    participant.save(update_fields=["remaining_coins"])