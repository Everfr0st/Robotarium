# User/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('chat/chat-messages', csrf_exempt(chat_messages), name='chat_messages'),
    path('chat/unread-msgs', UnreadMsgsApi.as_view(), name='unread_messages'),
    path('inbox/', InboxApi.as_view(), name='inbox'),

]
