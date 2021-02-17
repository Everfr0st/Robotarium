from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel, SoftDeletableModel


class Conversation(TimeStampedModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Conversation_owner")
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Conversation_opponent")

    def __str__(self):
        return '{0} -> {1}'.format(self.owner.username, self.opponent.username)


class Message(SoftDeletableModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)  # When user Postgres, change this name to created or send

    def __str__(self):
        return self.sender.username + " (" + str(self.created)[0:19] + ") - '" + self.text + "'"

    def serializer(self):
        serializer = {
            "type": "chat_message",
            "conversation": self.conversation.pk,
            "sender": self.sender.username,
            "text": self.text,
            "read": self.read,
            "send": self.created.strftime("%b %d, %Y - %I:%M %p")
        }
        return serializer
