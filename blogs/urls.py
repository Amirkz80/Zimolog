from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns= [
    # Home page
    path('', views.index, name='index'),
    # Page that adds new post
    path('add_post/', views.add_post, name='add_post' ),
    # page that edits posts
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]