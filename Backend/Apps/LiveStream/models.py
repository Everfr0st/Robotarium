from django.db import models

# Create your models here.
class LiveStreamId(models.Model):
    live_id = models.CharField(max_length=50)