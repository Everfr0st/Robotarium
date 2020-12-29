
# User/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('notifications-list/', NotificationsListApi.as_view(), name='notifications_list'),
]
