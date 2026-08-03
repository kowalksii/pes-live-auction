from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from common.mixins import AdminRequiredMixin

from .forms import TournamentForm
from .models import Tournament
from .services.tournament_service import TournamentService


def home(request):
    return render(request, "core/home.html")


class TournamentListView(AdminRequiredMixin, ListView):
    model = Tournament
    template_name = "core/tournament/list.html"
    context_object_name = "tournaments"
    ordering = ["-created_at"]


class TournamentDetailView(AdminRequiredMixin, DetailView):
    model = Tournament
    template_name = "core/tournament/detail.html"
    context_object_name = "tournament"


class TournamentCreateView(AdminRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "core/tournament/form.html"
    success_url = reverse_lazy("core:tournament_list")

    def form_valid(self, form):
        TournamentService.create_tournament(
            created_by=self.request.user,
            **form.cleaned_data,
        )

        messages.success(
            self.request,
            "Tournament created successfully.",
        )

        return redirect(self.success_url)


class TournamentUpdateView(AdminRequiredMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = "core/tournament/form.html"
    success_url = reverse_lazy("core:tournament_list")

    def form_valid(self, form):
        TournamentService.update_tournament(
            self.object,
            **form.cleaned_data,
        )

        messages.success(
            self.request,
            "Tournament updated successfully.",
        )

        return redirect(self.success_url)


class TournamentDeleteView(AdminRequiredMixin, DeleteView):
    model = Tournament
    template_name = "core/tournament/delete.html"
    success_url = reverse_lazy("core:tournament_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Tournament deleted successfully.",
        )

        return super().form_valid(form)