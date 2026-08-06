from django.urls import re_path

from .consumers import WaitingRoomConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/waiting-room/(?P<tournament_id>\d+)/$",
        WaitingRoomConsumer.as_asgi(),
    ),
]