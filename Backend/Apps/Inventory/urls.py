
# Inventory/urls.py
from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('inventory-list/', InventoryListApi.as_view(), name='inventory_list'),
    path('item-detail/', ItemDetailApi.as_view(), name='item_detail'),
    path('reserve-list/', ReserveListApi.as_view(), name='reserve_list'),
    path('create-reservation/', CreateReservationApi.as_view(), name='post_reservation'),
    path('history-reservation/', ReservationHistoryApi.as_view(), name='reservation_history'),
    path(r'element-Info/<int:pk>', ElementInfoApi.as_view(), name='element_info'),
    path(r'schedule-Info/<int:pk>', ScheduleInfoApi.as_view(), name='eschedule_info'),
]
