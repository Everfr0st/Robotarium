import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime

from django.contrib.auth.models import User
from notify.models import Notification

from Apps.Chat.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'notification_%s' % self.room_name
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
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data_json
        )

    # Receive message from room group
    def new_notification(self, event):
        # Send message to WebSocket
        unread_notifications = self.get_unread_notifications(event)
        event['unread_notifications'] = unread_notifications
        self.send(text_data=json.dumps(event))

    def get_unread_notifications(self, event):
        return Notification.objects.filter(recipient__username=event['receiver'], read=False).count()
