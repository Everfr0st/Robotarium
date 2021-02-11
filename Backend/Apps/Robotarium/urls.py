
# Inventory/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('robot-list/', RobotsListApi.as_view(), name='robots_list'),
    path('robot-status/', RobotUpdateAvailableStatusApi.as_view(), name='robot_status'),
]
