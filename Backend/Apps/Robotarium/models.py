from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Robot(models.Model):
    def element_directory_path(self, filename):
        filename = 'robot_{0}'.format(self.id)
        return 'robotarium/{0}'.format(filename + ".jpg")

    name = models.CharField(max_length=30, unique=True)
    ip = models.CharField(max_length=30, unique=True)
    available = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=element_directory_path, blank=True)
    last_usage = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + ' is available' if self.available else self.name + " isn't available"


class RobotUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    robot = models.ForeignKey(Robot, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
