from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ArtWorkConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Извлечение artwork_id из URL
        self.artwork_id = self.scope['url_route']['kwargs']['artwork_id']
        self.room_group_name = f'artwork_{self.artwork_id}'

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отключение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Обработка полученных сообщений
        data = json.loads(text_data)
        action = data['action']

        # Логика обработки сообщений
        if action == 'like':
            # Логика для лайков
            pass
        elif action == 'comment':
            # Логика для комментариев
            pass

        # Отправка обновлений в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'data': data
            }
        )

    async def send_message(self, event):
        # Отправка сообщения обратно клиенту
        await self.send(text_data=json.dumps(event['data']))
