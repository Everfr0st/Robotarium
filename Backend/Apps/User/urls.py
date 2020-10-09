# User/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup-more/', SignUpMoreInfo.as_view(), name='signup-more'),
    path('login/', SignIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('navbar-info/', NavBar.as_view(), name='logout')
]
