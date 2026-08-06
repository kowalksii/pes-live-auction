from django.urls import path

from .views import LiveAuctionRoomView

app_name = "auctions"

urlpatterns = [
    path(
        "tournaments/<int:pk>/live/",
        LiveAuctionRoomView.as_view(),
        name="live_room",
    ),
]