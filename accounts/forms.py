from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .utils import BootstrapFormMixin
from.models import User

class LoginForm(
    BootstrapFormMixin,
    AuthenticationForm,
):
    pass

class RegistrationForm(BootstrapFormMixin, UserCreationForm):

    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )