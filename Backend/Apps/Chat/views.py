from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from Apps.Chat.models import Message


class ChatMessages(TemplateView):

    def get(self, request, **kwargs):
        sender = request.GET["sender"]
        receiver = request.GET["receiver"]
        conversation_messages = Message.objects.filter(
            (
                Q(conversation__owner__username=sender, conversation__opponent__username=receiver) |
                Q(conversation__owner__username=receiver, conversation__opponent__username=sender)
            )
        ).order_by("-updated")
        conversation_messages_list = [messages.serializer() for messages in conversation_messages]
        return JsonResponse(conversation_messages_list, safe=False)
