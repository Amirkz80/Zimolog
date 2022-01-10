from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns= [
    # Home page
    path('', views.index, name='index'),
    
    # About page
    path('about/', views.about ,name='about' ),
    
    # Page that adds new post
    path('add_post/', views.add_post, name='add_post' ),
    
    # Page that edits posts
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    
    # Page to show the user this post does't belong to him/her
    path('prompt/', views.edit_post, name='prompt'),
    
    # Page that shows serach results
    path('search/', views.search, name='search'),
    
    # Deletes the post
    path('delete/<int:post_id>/', views.delete, name='delete'),
    
    # Page that shows full post with its comments
    path('post/<int:post_id>', views.full_post, name='full_post'),
    
    # Adds a comment
    path('add_comment/<int:post_id>', views.add_comment, name='add_comment'),
    
    # Like or dislike a post
    path('like/<int:post_id>', views.like, name='like'),
    
    # Discover page
    path('discover/', views.discover, name='discover'),
    
    # Discover page by hearts
    path('discover/<str:sort_type>', views.discover, name='discover'),
    
    # Share via email form page
    path('post/<int:post_id>/share', views.share, name='share')
]