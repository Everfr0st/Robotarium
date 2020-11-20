from rest_framework import serializers
from .models import Inventory, Reserve


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['name', 'code', 'quantity', 'photo', 'added']


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['user', 'schedule', 'element', 'quantity', 'created']
