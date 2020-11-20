from django.contrib import admin
from .models import Inventory, Schedule, Reserve



admin.site.register(Schedule)
admin.site.register(Inventory)
admin.site.register(Reserve)

