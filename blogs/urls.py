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
    # page to show the user this post does't belong to him/her
    path('prompt/', views.edit_post, name='prompt'),
    # page that shows serach results
    path('search/', views.search, name='search'),
    # deletes the post
    path('delete/<int:post_id>/', views.delete, name='delete'),
    # page that shows full post with its comments
    path('post/<int:post_id>', views.full_post, name='full_post'),
    # adds a comment
    path('add_comment/<int:post_id>', views.add_comment, name='add_comment'),
    # like or dislike a post
    path('like/<int:post_id>', views.like, name='like'),
    # discover page
    path('discover/', views.discover, name='discover'),
    # discover page by hearts
    path('discover/<str:sort_type>', views.discover, name='discover')
]