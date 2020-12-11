# User/urls.py
from django.urls import path, include

from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('create-user/', CreateUserApi.as_view(), name='create_user'),
    path('signup-more/', SignUpMoreInfo.as_view(), name='signup_more'),
    #path('logout/<str:token>', Logout.as_view(), name='logout'),
    path('navbar-info/', NavBar.as_view(), name='navbar_info'),
    path('users-list/', UsersList.as_view(), name='users_list'),
    path('user-detail', UserDetail.as_view(), name='user_detail')
]
