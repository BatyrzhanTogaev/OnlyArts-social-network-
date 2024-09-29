# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ArtWorkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.artwork_id = self.scope['url_route']['kwargs']['artwork_id']
        self.room_group_name = f'artwork_{self.artwork_id}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'artwork_message',
                'message': message
            }
        )

    async def artwork_message(self, event):
        message = event['message']

        # Отправляем сообщение на WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
