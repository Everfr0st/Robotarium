from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from Apps.Chat.models import Message, Conversation
from Apps.User.models import UserProfilePhoto, UserOnline


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
    ).order_by("-created")
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


class InboxApi(generics.ListAPIView):
    model = Message
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(
            Q(conversation__owner_id=request.user.pk) |
            Q(conversation__opponent_id=request.user.pk)).distinct("conversation").order_by('conversation','-created')
        messages_list = []
        for message in messages:
            msg_dictionary = message.serializer()
            opponent = self.get_opponent(request.user, message)
            user_online = UserOnline.objects.get(user=opponent)
            msg_dictionary["opponent"] = {
                'username': opponent.username,
                'name': '{0} {1}'.format(opponent.first_name, opponent.last_name),
                'profile_picture': self.get_profile_picture(opponent),
                'online': user_online.is_online,
            }
            msg_dictionary["unread_messages"] = Message.objects.filter(conversation=message.conversation, read=False).exclude(sender=request.user).count()
            messages_list.append(msg_dictionary)

        return JsonResponse(messages_list, safe=False)

    def get_opponent(self, user, msg):
        if user.username == msg.conversation.owner.username:
            opponent = msg.conversation.opponent
        else:
            opponent = msg.conversation.owner
        return opponent

    def get_profile_picture(self, user_obj):
        try:
            user_profile_photo = UserProfilePhoto.objects.get(user=user_obj).profile_picture.url
        except:
            user_profile_photo = ''
        return user_profile_photo
