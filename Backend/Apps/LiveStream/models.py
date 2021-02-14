from django.db import models

# Create your models here.
class LiveStreamId(models.Model):
    live_id = models.CharField(max_length=50)

    def __str__(self):
        return self.live_id