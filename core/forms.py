from django import forms

from common.forms import BootstrapFormMixin

from .models import Tournament


class TournamentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Tournament

        fields = (
            "name",
            "description",
            "total_coins",
            "max_participants",
            "status",
        )

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Tournament name cannot be empty."
            )

        return name