from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class UserOnline(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    updated = models.DateField(auto_now=True)


class UserProfilePhoto(models.Model):
    def user_directory_path(instance, filename):
        filename = 'user_{0}{1}'.format(instance.pk, datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
        return 'profile_pictures/{0}'.format(filename + ".jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_directory_path,blank=True)

    def __str__(self):
        return "@" + self.user.username +"'s profile picture"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    career = models.CharField(max_length=30)
    semester = models.IntegerField()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=30)
    date_start = models.DateField()


class UserReport(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from_report')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to_report')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
