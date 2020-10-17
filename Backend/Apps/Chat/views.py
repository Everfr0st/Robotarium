from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse

from Apps.Chat.models import Message, Conversation


def ChatMessages(request):
    try:
        sender = request.GET["sender"]
        receiver = request.GET["receiver"]
    except:
        return JsonResponse({'conversation_created': False})

    conversation_messages = Message.objects.filter(
        (
                Q(conversation__owner__username=sender, conversation__opponent__username=receiver) |
                Q(conversation__owner__username=receiver, conversation__opponent__username=sender)
        )
    ).order_by("-updated")
    if conversation_messages.exists():
        conversation_messages_list = [messages.serializer() for messages in conversation_messages]
        return JsonResponse(conversation_messages_list, safe=False)
    else:
        current_conversation = Conversation.objects.filter(
            Q(owner__username=sender, opponent__username=receiver) |
            Q(owner__username=receiver, opponent__username=sender)
        )
        if (current_conversation.exists()):
            return JsonResponse({'conversation_created': False, 'conversation': current_conversation[0].pk})
        else:
            try:
                receiver_obj = User.objects.get(username=receiver)
                seder_obj = User.objects.get(username=sender)
                new_conversation = Conversation.objects.create(owner=seder_obj, opponent=receiver_obj)
                return JsonResponse({'conversation_created': True, 'conversation': new_conversation.pk})
            except:
                return JsonResponse({'conversation_created': False, 'error': True})



