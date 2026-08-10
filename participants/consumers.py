from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Participant


class WaitingRoomConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        self.tournament_id = self.scope["url_route"]["kwargs"]["tournament_id"]

        self.group_name = f"waiting_room_{self.tournament_id}"

        participant_exists = await self.participant_exists()

        if not participant_exists:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

        await self.set_connected(True)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "participant_connected",
            },
        )

        await self.participant_connected({})

    async def disconnect(self, close_code):

        participant_exists = await self.participant_exists()

        if participant_exists:

            await self.set_connected(False)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "participant_connected",
                },
            )

            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

    async def participant_connected(self, event):

        await self.send_json(
            {
                "type": "participant_status",
                "connected_count": await self.connected_count(),
                "approved_count": await self.approved_count(),
            }
        )

    @database_sync_to_async
    def participant_exists(self):

        return Participant.objects.filter(
            tournament_id=self.tournament_id,
            user=self.scope["user"],
            is_active=True,
        ).exists()

    @database_sync_to_async
    def set_connected(self, value):

        Participant.objects.filter(
            tournament_id=self.tournament_id,
            user=self.scope["user"],
        ).update(
            is_connected=value,
        )

    @database_sync_to_async
    def connected_count(self):

        return Participant.objects.filter(
            tournament_id=self.tournament_id,
            is_connected=True,
            is_active=True,
        ).count()

    @database_sync_to_async
    def approved_count(self):

        return Participant.objects.filter(
            tournament_id=self.tournament_id,
            is_active=True,
        ).count()