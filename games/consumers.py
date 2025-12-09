import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_id = f"game_{self.room_id}"

        # join room group
        await self.channel_layer.group_add(
            self.room_group_id, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_id, self.channel_name
        )

    async def receive(self, text_data):
        game_data = json.loads(text_data)

        # Game Logic
        new_data = game_data 

        await self.channel_layer.group_send(
            self.room_group_id,
            {"type": "my_function", "data": new_data}
        )

    async def my_function(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps({"my_data": data}))