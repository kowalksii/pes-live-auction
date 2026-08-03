from accounts.models import User


def approve_participant(user: User):
    """
    Approve a participant account.
    """
    user.is_approved = True
    user.save(update_fields=["is_approved"])


def revoke_participant(user: User):
    """
    Revoke participant approval.
    """
    user.is_approved = False
    user.save(update_fields=["is_approved"])