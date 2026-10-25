import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatConversation, ChatMessage

class SupportChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data.get('message')
        sender_type = data.get('sender_type', 'CUSTOMER')
        user = self.scope.get('user')

        if not message_text:
            return

        # Save message to database asynchronously
        await self.save_message(self.conversation_id, user if user.is_authenticated else None, sender_type, message_text)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_type': sender_type,
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket client
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_type': event['sender_type'],
        }))

    @database_sync_to_async
    def save_message(self, conversation_id, user, sender_type, message_text):
        conversation, _ = ChatConversation.objects.get_or_create(
            conversation_id=conversation_id,
            defaults={'customer': user if (user and not user.is_staff) else None}
        )
        ChatMessage.objects.create(
            conversation=conversation,
            sender=user if (user and user.is_authenticated) else None,
            sender_type=sender_type,
            message=message_text
        )