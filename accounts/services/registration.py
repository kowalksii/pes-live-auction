from django.db import transaction

from accounts.models import User


@transaction.atomic
def register_participant(form):
    """
    Register a new participant.

    New users:
    - become PARTICIPANT
    - remain pending until approved
    """

    user = form.save(commit=False)

    user.role = User.UserRole.PARTICIPANT
    user.is_approved = False

    user.save()

    if hasattr(form, "save_m2m"):
        form.save_m2m()

    return user