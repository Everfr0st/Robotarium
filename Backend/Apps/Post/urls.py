
# User/urls.py
from django.urls import path

from .views import *


urlpatterns = [
    path('new-post/', CreatePost.as_view(), name='create_post'),
]
