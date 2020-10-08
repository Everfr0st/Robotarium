from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carreer = models.CharField(max_length=30)
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

