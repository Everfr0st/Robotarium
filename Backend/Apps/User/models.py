from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class UserOnline(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        message = self.user.username
        message += ' is Online' if self.is_online else ' is Offline'
        return message


class UserProfilePhoto(models.Model):
    def user_directory_path(instance, filename):
        filename = 'user_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'profile_pictures/{0}'.format(filename + ".jpg")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return "@" + self.user.username + "'s profile picture"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    career = models.CharField(max_length=30)
    semester = models.IntegerField()

    def __str__(self):
        return self.user.username + " studies " + self.career

    def serializer(self):
        return {
            "role": "Estudiante",
            "user": self.user.username,
            "career": self.career,
            "semester": self.semester
        }


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=30)
    date_start = models.DateField()

    def __str__(self):
        return self.user.username + " works in " + self.department

    def serializer(self):
        return {
            "role": "Docente",
            "user": self.user.username,
            "department": self.department,
            "date_start": self.date_start
        }


class UserReport(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from_report')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to_report')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
