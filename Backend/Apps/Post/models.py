from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    elements = models.ManyToManyField('self', through='TagUser', related_name='taguser_to_post')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "@" + self.user.username + " publicó: " + self.body[:50]

class PostPhoto(models.Model):
    def user_directory_path(instance, filename):
        filename = 'post_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'posts_photos/{0}'.format(filename + ".jpg")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)


class TagUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


