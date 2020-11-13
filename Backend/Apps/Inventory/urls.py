
# Inventory/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('inventory-list/', InventoryListApi.as_view(), name='inventory_list'),
]
