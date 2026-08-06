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
    path(
        "tournaments/<int:pk>/requests/",
        views.PendingAuctionRequestListView.as_view(),
        name="pending_requests",
    ),
    
    path(
        "requests/<int:pk>/approve/",
        views.ApproveAuctionRequestView.as_view(),
        name="approve_request",
    ),
    
    path(
        "requests/<int:pk>/reject/",
        views.RejectAuctionRequestView.as_view(),
        name="reject_request",
    ),
    path(
        "tournaments/<int:pk>/waiting-room/",
        views.WaitingRoomView.as_view(),
        name="waiting_room",
    ),
    path(
        "tournaments/<int:pk>/admin-waiting-room/",
        views.AdminWaitingRoomView.as_view(),
        name="admin_waiting_room",
    ),
    
]