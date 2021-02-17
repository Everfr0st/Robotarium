import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime

from django.contrib.auth.models import User

from Apps.Chat.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "chat_message":
            text_data_json = self.save_message(text_data_json)
            text_data_json["unread_messages"] = self.unread_msgs(text_data_json)
        elif text_data_json["type"] == "seen_message":
            self.mark_as_read_messages(text_data_json)
            text_data_json["unread_messages"] = 0
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data_json
        )

    # Receive message from room group
    def chat_message(self, event):
        # self.save_message(event)
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))

    def type_message(self, event):
        self.send(text_data=json.dumps(event))

    def seen_message(self, event):
        self.send(text_data=json.dumps(event))

    def save_message(self, msg_obj):
        sender = User.objects.get(username=msg_obj['sender'])
        return Message.objects.create(conversation_id=msg_obj['conversation'], sender=sender,
                                      text=msg_obj['text']).serializer()

    def mark_as_read_messages(self, seen_obj):
        messages = Message.objects.filter(conversation_id=seen_obj['room'], sender__username=seen_obj['receiver'],
                                          read=False)
        for message in messages:
            message.read = True
            message.save()

    def unread_msgs(self, msg_obj):
        messages = Message.objects.filter(conversation_id=msg_obj['conversation'],
                                          sender__username=msg_obj['sender'],
                                          read=False).count()
        return messages
