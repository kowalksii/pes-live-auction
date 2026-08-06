from participants.models import Participant


def get_participant_by_user(user):

    return Participant.objects.select_related("user").get(user=user)