from django.http import JsonResponse
from django.shortcuts import render
from notify.models import Notification
from rest_framework import generics

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Apps.User.models import UserProfilePhoto


class NotificationsListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Notification

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(recipient_id=request.user.pk)
        notifications_list = []
        for notification in notifications:
            notification_dictionary = self.get_obj_context(notification)
            notifications_list.append(notification_dictionary)
            return JsonResponse(notifications_list, safe=False)

    def get_obj_context(self, notification):
        try:
            actor_profile_picture = UserProfilePhoto.objects.get(user=notification.actor).profile_picture.url
        except:
            actor_profile_picture = ''

        target = self.get_target(notification)
        return {
            'type': notification.nf_type,
            'actor': {
                'username': notification.actor.username,
                'name': '{0} {1}'.format(notification.actor.first_name, notification.actor.last_name),
                'profile_picture': actor_profile_picture
            },
            'verb': notification.verb,
            'description': notification.description,
            'target': target,
            'created': notification.created,
        }

    def get_target(self, notification):
        if notification.nf_type == 'tagged_by_one_user':
            target = notification.target.body
        elif notification.nf_type == 'reported_by_one_user':
            target = ''  # Create Report Model
        else:
            target = ''
        return target
