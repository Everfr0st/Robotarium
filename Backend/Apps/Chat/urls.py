# User/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('chat/chat-messages', csrf_exempt(ChatMessages), name='chat_messages'),
    path('inbox/', InboxApi.as_view(), name='inbox'),

]
