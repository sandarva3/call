import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = f"user_{self.scope['user'].id}"
        self.room_group_name = f"signaling_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        callee_id = data.get("calleeID")
        caller_id = data.get("callerID")
        sdp = data.get("sdp")
        ice_candidate = data.get("iceCandidate")

        if callee_id:
            await self.channel_layer.group_send(
                f"signaling_user_{callee_id}",
                {
                    "type": "signaling_message",
                    "callerID": caller_id,
                    "calleeID": callee_id,
                    "sdp": sdp,
                    "iceCandidate": ice_candidate,
                }
            )

    async def signaling_message(self, event):
        await self.send(text_data=json.dumps(event))
