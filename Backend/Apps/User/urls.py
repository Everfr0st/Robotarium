# User/urls.py
from django.urls import path, include

from .views import *

urlpatterns = [
    path('user-auth/', include('dj_rest_auth.urls')),
    path('create-user/', CreateUserApi.as_view(), name='create_user'),
    path('user-role/', SignUpMoreInfo.as_view(), name='signup_more'),
    #path('logout/<str:token>', Logout.as_view(), name='logout'),
    path('navbar-info/', NavBar.as_view(), name='navbar_info'),
    path('users-list/', UsersList.as_view(), name='users_list'),
    path('user-detail', UserDetail.as_view(), name='user_detail'),
    path('user-Info/', UserInfoApi.as_view(), name='user_info'),
    path('user-profile-picture/', ProfilePictureApi.as_view(), name='user_profile')
]
