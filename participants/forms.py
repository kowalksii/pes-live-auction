from django import forms

from common.forms import BootstrapFormMixin

from .models import Participant


class ParticipantForm(
    BootstrapFormMixin,
    forms.ModelForm,
):

    class Meta:
        model = Participant

        fields = (
            "team_name",
            "initial_coins",
            "is_active",
        )