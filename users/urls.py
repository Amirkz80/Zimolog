"""Defines url patterns"""

from django.urls import path, include
from . import views

app_name ='users'
urlpatterns =[
    # The login page
    path('', include('django.contrib.auth.urls')),
    # Registering new user.
    path('register/', views.register, name='register'),
    path('logout/', views.logged_out, name='logged_out')
] 