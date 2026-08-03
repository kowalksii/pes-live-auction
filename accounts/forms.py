from django.contrib.auth.forms import AuthenticationForm

from .utils import BootstrapFormMixin


class LoginForm(
    BootstrapFormMixin,
    AuthenticationForm,
):
    pass