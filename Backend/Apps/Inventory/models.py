from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from icalendar import Calendar, Event as ICalEvent
from pytz import UTC


class Inventory(models.Model):
    def element_directory_path(instance, filename):
        filename = 'element_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'inventory/{0}'.format(filename + ".jpg")

    name = models.CharField(max_length=40)
    code = models.CharField(max_length=5)
    quantity = models.IntegerField()
    photo = models.ImageField(upload_to=element_directory_path, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.quantity)


class Schedule(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "{0} from {1} to {2}".format(self.date, self.start_time, self.end_time)

    def serializer(self):
        json_bj = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        return json_bj


class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    element = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "@{0} reservó {1} ({2})".format(self.user.username, self.element.name, self.quantity)

    def serializer(self):
        json_obj = {
            'user': {
                'username': self.user.username,
                'name': '{0} {1}'.format(self.user.first_name, self.user.last_name)
            },
            'schedule': self.schedule.serializer(),
            'element': self.element.name,
            'quantity': self.quantity,
            'created': self.created,
        }
        return json_obj

    def generate_event(self):
        cal = Calendar()
        site = Site.objects.get_current()
        start = str(self.schedule.date) + ' ' + str(self.schedule.start_time)
        end = str(self.schedule.date) + ' ' + str(self.schedule.end_time)
        start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

        cal.add('prodid', '-//UAO-RAS Reservation//{}//'.format(site.domain))
        cal.add('version', '2.0')

        ical_event = ICalEvent()
        ical_event.add('summary', '@{0} reservó el elemento {1}'.format(self.user.username, self.element.name))
        ical_event.add('dtstart', start_date)
        ical_event.add('dtend', end_date)
        ical_event.add('dtstamp', start_date - timedelta(minutes=30))
        ical_event.add('priority', 5)
        ical_event['uid'] = str(self.id)

        cal.add_component(ical_event)
        return cal.to_ical()
