# User/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('chat/chat-messages', ChatMessages.as_view(), name='chat_messages'),

]
