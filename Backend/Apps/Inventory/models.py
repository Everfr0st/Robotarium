from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Inventory(models.Model):
    def element_directory_path(instance, filename):
        filename = 'element_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'inventory/{0}'.format(filename + ".jpg")

    name = models.CharField(max_length=40)
    code = models.CharField(max_length=5, unique=True)
    quantity = models.IntegerField()
    photo = models.ImageField(upload_to=element_directory_path,blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.quantity)



class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "{0} from {1} to {2}".format(self.date, self.start_time, self.end_time)

    def serializer(self):
        json_bj = {
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        return json_bj
class Reserve(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE)
    element = models.OneToOneField(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "@{0} reservó {1} ({2})".format(self.user.username, self.element.name, self.quantity)

    def serializer(self):
        json_obj = {
            'user': self.user.username,
            'schedule': self.schedule.serializer(),
            'element': self.element.name,
            'quantity': self.quantity,
            'created': self.created,
        }
        return json_obj




