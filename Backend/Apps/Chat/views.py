from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from rest_framework import generics

from Apps.Chat.models import Message, Conversation


def ChatMessages(request):
    print(request,request.POST)
    """sender = request.POST["sender"]
    receiver = request.POST["requestreceiver"]"""
    sender = "hola"
    receiver = "hola"

    conversation_messages = Message.objects.filter(
        (
                Q(conversation__owner__username=sender, conversation__opponent__username=receiver) |
                Q(conversation__owner__username=receiver, conversation__opponent__username=sender)
        )
    )
    if conversation_messages.exists():
        conversation_messages.order_by("-updated")
        conversation_messages_list = [messages.serializer() for messages in conversation_messages]
        return JsonResponse(conversation_messages_list, safe=False)
    else:
        try:
            Conversation.objects.create(owner__username=self, opponent__username=receiver)
            return JsonResponse({'conversation_created': True})
        except:
            return JsonResponse({'conversation_created': False})
