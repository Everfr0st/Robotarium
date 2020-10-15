from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime

from django.contrib.auth.models import User


class Conversation(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Conversation_owner")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Conversation_opponent")


class Message(SoftDeletableModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
    updated = models.DateTimeField() #When user Postgres, change this name to created or send

    def __str__(self):
        return self.sender.username + " (" + str(self.updated)[0:19] + ") - '" + self.text + "'"

    def serializer(self):
        serializer = {
            "conversation": self.conversation.pk,
            "sender": self.sender.username,
            "text": self.text,
            "read": self.read,
            "send": self.updated.strftime("%b %d, %Y - %H:%M")
        }
        return serializer
