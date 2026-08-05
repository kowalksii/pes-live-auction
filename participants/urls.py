from django.urls import path

from . import views

app_name = "participants"

urlpatterns = [
    path(
        "tournaments/<int:pk>/join/",
        views.JoinTournamentView.as_view(),
        name="join_tournament",
    ),
    path(
        "tournaments/<int:pk>/request/",
        views.RequestAuctionEntryView.as_view(),
        name="request_auction_entry",
    ),
]