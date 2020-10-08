from django.contrib import admin
from .models import Inventory, Schedule, Reserve, Element

class ElementAdmin(admin.TabularInline):
    model = Element
    fields = ('item', 'reserve')
    fk_name = 'reserve'

class ReserveAdmin(admin.ModelAdmin):
    inlines = (ElementAdmin,)

admin.site.register(Schedule)
admin.site.register(Inventory)
admin.site.register(Reserve, ReserveAdmin)

