
# User/urls.py
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *


urlpatterns = [
    path('new-post/', csrf_exempt(CreatePost.as_view()), name='create_post'),
    path('post-list/', PostList.as_view(), name='post_list'),
]
