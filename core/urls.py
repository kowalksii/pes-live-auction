from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "tournaments/",
        views.TournamentListView.as_view(),
        name="tournament_list",
    ),

    path(
        "tournaments/create/",
        views.TournamentCreateView.as_view(),
        name="tournament_create",
    ),

    path(
        "tournaments/<int:pk>/",
        views.TournamentDetailView.as_view(),
        name="tournament_detail",
    ),

    path(
        "tournaments/<int:pk>/edit/",
        views.TournamentUpdateView.as_view(),
        name="tournament_update",
    ),

    path(
        "tournaments/<int:pk>/delete/",
        views.TournamentDeleteView.as_view(),
        name="tournament_delete",
    ),
]