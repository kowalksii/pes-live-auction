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

class AuctionJoinRequestForm(
    BootstrapFormMixin,
    forms.Form,
):
    team_name = forms.CharField(
        max_length=100,
        label="Auction Display Name",
        help_text="This name will be shown during the live auction.",
    )