from functools import wraps

from django.core.exceptions import PermissionDenied

from accounts.models import User


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if request.user.role != User.UserRole.ADMIN:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def approved_participant_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        user = request.user

        if user.role != User.UserRole.PARTICIPANT:
            raise PermissionDenied

        if not user.is_approved:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper