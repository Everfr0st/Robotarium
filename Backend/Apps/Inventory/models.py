from django.db import models
from django.contrib.auth.models import User

class Inventory(models.Model):
    name = models.CharField(max_length=30)
    ref = models.IntegerField()
    classification = models.CharField(max_length=10)
    location = models.CharField(max_length=5)
    added = models.DateTimeField(auto_now_add=True)

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