from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from Apps.User.models import UserOnline
from django.contrib.auth.signals import user_logged_in, user_logged_out


@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserOnline.objects.create(user=instance)


@receiver(user_logged_in, sender=User)
def user_is_online(sender, **kwargs):
    user = kwargs["user"]
    is_online = UserOnline.objects.filter(user=user).first()
    if is_online:
        is_online.is_online = True
        is_online.save()



