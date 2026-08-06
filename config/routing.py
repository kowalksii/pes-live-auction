from participants.routing import (
    websocket_urlpatterns as participant_websocket_urlpatterns,
)

websocket_urlpatterns = [
    *participant_websocket_urlpatterns,
]