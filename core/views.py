from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView,DetailView,ListView,UpdateView,DeleteView,)

from common.mixins import AdminRequiredMixin
from accounts.models import UserRole
from participants.models import AuctionJoinRequest, Participant
from participants.services.membership import TournamentMembershipService

from .forms import TournamentForm
from .models import Tournament, TournamentStatus
from .services.tournament_service import TournamentService


def home(request):
    return render(request, "core/home.html")


class TournamentListView(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = "core/tournament/list.html"
    context_object_name = "tournaments"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tournaments = context["tournaments"]
        user = self.request.user

        for tournament in tournaments:

            # Default values
            tournament.can_join = False
            tournament.is_member = False

            # Only approved participants can join tournaments
            if (
                user.is_authenticated
                and user.role == UserRole.PARTICIPANT
                and user.is_approved
            ):

                tournament.is_member = (
                    TournamentMembershipService.is_member(
                        user=user,
                        tournament=tournament,
                    )
                )

                tournament.can_join = (
                    tournament.status == TournamentStatus.REGISTRATION
                    and not tournament.is_member
                )

        return context


class TournamentDetailView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = "core/tournament/detail.html"
    context_object_name = "tournament"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        tournament = self.object

        membership = None
        is_member = False
        can_join = False
        can_request_auction = False
        has_pending_request = False
        is_participant = False

        if (
            user.is_authenticated
            and user.role == UserRole.PARTICIPANT
            and user.is_approved
        ):

            membership = TournamentMembershipService.get_membership(
                user,
                tournament,
            )

            is_member = membership is not None

            can_join = (
                tournament.status == TournamentStatus.REGISTRATION
                and not is_member
            )

            if membership:

                has_pending_request = AuctionJoinRequest.objects.filter(
                    membership=membership,
                    status=AuctionJoinRequest.Status.PENDING,
                ).exists()

                is_participant = Participant.objects.filter(
                    user=user,
                    tournament=tournament,
                ).exists()

                can_request_auction = (
                    not has_pending_request
                    and not is_participant
                    and tournament.status == TournamentStatus.REGISTRATION
                )

        context.update(
            {
                "membership": membership,
                "is_member": is_member,
                "can_join": can_join,
                "can_request_auction": can_request_auction,
                "has_pending_request": has_pending_request,
                "is_participant": is_participant,
            }
        )

        return context


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