from rest_framework import serializers
from .models import Inventory, Reserve, Schedule


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['name', 'code', 'quantity', 'photo', 'added']


class ReserveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserve
        fields = ['user', 'schedule', 'element', 'quantity', 'created']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['date_start', 'date_end', 'start_time', 'end_time']
