
# User/urls.py
from django.urls import path
from .views import *


urlpatterns = [
    path('retrieve-liveId/',RetrieveLivestreamId.as_view(), name='live_id'),
]
