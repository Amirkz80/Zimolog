"""Defines url patterns"""

from django.urls import path, include
from . import views

app_name ='users'
urlpatterns =[
    # The login page
    path('', include('django.contrib.auth.urls')),
    # Registering new user.
    path('register/', views.register, name='register'),
    # A page to see logging out result
    path('logout/', views.logged_out, name='logged_out'),
     # page that shows user's profile and posts
    path('dashboard/', views.dashboard, name='dashboard'),
    # The authenticated_user followers page
    path('<str:user_name>/followers', views.followers, name='followers'),
    # The authenticated_user followeing page
    path('<str:user_name>/following', views.following, name='following'),
    # The page that shows user's(not authenticated one!) page
    path('<str:user_name>/', views.user_info, name='user_info'),
    # page that informs users if they followed or unfollowed somone else
    path('<str:user_name>/follow_status', views.follow_unfollow, name='follow_unfollow' )
] 