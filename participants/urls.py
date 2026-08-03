from django.urls import path

from .views import JoinTournamentView

app_name = "participants"

urlpatterns = [
    path(
        "tournaments/<int:pk>/join/",
        JoinTournamentView.as_view(),
        name="join_tournament",
    ),
]