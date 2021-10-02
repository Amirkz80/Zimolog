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
    path('users/<str:user_name>', views.followers, name='followers'),
] 