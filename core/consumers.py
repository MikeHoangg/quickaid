from channels.generic.websocket import AsyncWebsocketConsumer
import json

from medicine.models import Notification
from medicine.serializers import NotificationSerializer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = f"notifications_for_user_{self.user_id}"

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        notifications = NotificationSerializer(
            Notification.objects.filter(schedule__user=self.user_id, pending=True)).data
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'notifications': notifications
            }
        )

    async def chat_message(self, event):
        notifications = event['notifications']

        await self.send(text_data=json.dumps({
            'notifications': notifications
        }))
