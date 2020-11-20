
# Inventory/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('inventory-list/', InventoryListApi.as_view(), name='inventory_list'),
    path('item-detail/', ItemDetailApi.as_view(), name='item_detail'),
    path('reserve-list/', ReserveListApi.as_view(), name='reserve_list'),
]
