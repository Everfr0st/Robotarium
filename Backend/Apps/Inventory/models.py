from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Inventory(models.Model):
    def element_directory_path(instance, filename):
        filename = 'element_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'inventory/{0}'.format(filename + ".jpg")

    name = models.CharField(max_length=40)
    code = models.CharField(max_length=5)
    quantity = models.IntegerField()
    photo = models.ImageField(upload_to=element_directory_path,blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "{0} from {1} to {2}".format(self.date, self.start_time, self.end_time)


class Reserve(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE)
    elements = models.ManyToManyField('self', through='Element', related_name='element_to')
    created = models.DateTimeField(auto_now_add=True)


class Element(models.Model):
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE)
