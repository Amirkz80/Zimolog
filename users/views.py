from datetime import datetime
from time import strftime
from django.shortcuts import render, redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserInfo
from blogs.models import BlogPost


def calculate_time(object_time, now_time, keyword=''):
    """Calculates how much time has been passed from object_time till now"""
    """keyword can be (posted) word or (joined) word depending on usage for posts or users"""
    
    final_string = ""

    diff = {
    'year' : now_time.year - object_time.year,
    'month' : now_time.month - object_time.month,
    'day' :  now_time.day - object_time.day,
    'hour' :  now_time.hour - object_time.hour,
    'minute' :  now_time.minute - object_time.minute,
    'second' : now_time.second - object_time.second
    }
    
    if diff['year'] > 0 :
        final_string = object_time.strftime(f"{keyword} at %b, %d %Y")

    if diff['year'] == 0 and diff['month'] != 0 :
        final_string = object_time.strftime(f"{keyword} at %b, %d")

    if diff['year'] == 0 and diff ['month'] == 0 :

        # For days
        if diff['day'] > 7 :
            final_string = object_time.strftime(f"{keyword} at %b, %d")
        if diff['day'] <= 7 and diff['day'] > 1 :
            final_string = f"{keyword} {diff['day']} days ago"
        if diff['day'] == 1 :
            final_string = f"{keyword} {diff['day']} day ago"
        
        # For hours
        if diff['day'] == 0 :
            if diff['hour'] > 1 :
                final_string = f"{keyword} {diff['hour']} hours ago"
            if diff['hour'] == 1 :
                final_string = f"{keyword} {diff['hour']} hour ago"

            # For minutes
            if diff['hour'] == 0 :
                if diff['minute'] > 1 :
                    final_string = f"{keyword} {diff['minute']} minutes ago"
                if diff['minute'] == 1 :
                    final_string = f"{keyword} {diff['minute']} minute ago"

                # For seconds
                if diff['minute'] == 0 :
                    if diff['second'] > 1 :
                        final_string = f"{keyword} {diff['second']} seconds ago"
                    if diff['second'] == 1 :
                        final_string = f"{keyword} {diff['second']} second ago"

                    if diff['second'] == 0 :
                        final_string = f"{keyword} just now"

    return final_string

def get_user(user_name_string):
    """"Gets User from data base through its username"""
    user = User.objects.get(username=user_name_string)
    return (user)

def register(request):
    """Registers new user"""
    
    # Check if user is authenticated
    if request.user.is_authenticated :
        return redirect('users:dashboard')

    if request.method != 'POST':
        # Sets form to a blank page
        form = UserCreationForm()
    else:
        # Processes user data and login
            form = UserCreationForm(data=request.POST)

            if form.is_valid():
                new_user = form.save()
                # creating a userinfo model for user
                UserInfo(user=new_user).save()
                # now we log in and then redirect to the index page
                login(request, new_user)
                return redirect('blogs:index')

    # Shows a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def logged_out(request):
    """logging out"""
    return redirect(request, 'registration/logged_out')


@login_required
def dashboard(request):
    """Returns authentiacted user's informations and posts"""
    date_joined = request.user.date_joined
    now = datetime.utcnow()
    user_posts = BlogPost.objects.filter(owner=request.user).order_by("-date_added")
    join_message = calculate_time(date_joined, now, keyword="Joined")
    
    for post in user_posts:
        post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted") 

    context = {'user_posts' : user_posts, 'join_message' : join_message}
    return render(request, 'user/dashboard.html', context)


@login_required
def followers(request,user_name):
    """Shows user's followers"""
    user = get_user(user_name)
    context ={'user' : user}
    return render(request, 'user/followers.html', context)


@login_required
def following(request,user_name):
    """Shows user's following"""
    user = get_user(user_name)
    context = {'user' : user}
    return render(request, 'user/following.html', context)


@login_required
def user_info(request, user_name): 
    """Returns user's(not authenticated user) posts and info"""

    # If currnet authenticated user is trying to see h/h page, redirect to h/h dashboard
    if request.user.username == user_name:
        return redirect('users:dashboard')
    
    user = get_user(user_name)
    posts = user.blogpost_set.order_by("-date_added")
    join_message = calculate_time(user.date_joined, datetime.utcnow(), keyword="posted")

    context = {'requested_user' : user, 'posts' : posts, 'join_message' : join_message}
    return render(request, 'user/user_info.html', context)


@login_required
def follow_unfollow(request, user_name):
    """"Adds current user to selected user's followers or remove it from that"""
    current_usernname = request.user.username
    selected_username = user_name
    currnet_user_info = request.user.userinfo
    selected_user_info = get_user(user_name).userinfo 
    
    #If user is already in selected user's followers, does unfollow
    if current_usernname in selected_user_info.followers:
        selected_user_info.followers.remove(current_usernname)
        selected_user_info.followers_number = selected_user_info.followers_number - 1
        selected_user_info.save(update_fields=['followers', 'followers_number'])
        
        currnet_user_info.following.remove(selected_username)
        currnet_user_info.following_number = currnet_user_info.following_number - 1
        currnet_user_info.save(update_fields=['following', 'following_number'])

        flag = 0 
        context = {'flag' : flag, 'user_name' : selected_username}
        return render(request, 'user/follow_unfollow.html', context)

    #If user is not in selected user's followers, does unfollow
    else:
        # Making empty lists if these to lists have no member
        if bool(selected_user_info.followers) is False:
            selected_user_info.followers = []
        if bool(currnet_user_info.following) is False:
            currnet_user_info.followers = []    
        
        selected_user_info.followers.append(current_usernname)
        selected_user_info.followers_number = selected_user_info.followers_number + 1
        selected_user_info.save(update_fields=['followers', 'followers_number'])
        
        currnet_user_info.following.append(selected_username)
        currnet_user_info.following_number = currnet_user_info.following_number + 1
        currnet_user_info.save(update_fields=['following', 'following_number'])

        flag = 1
        context = {'flag' : flag, 'user_name' : selected_username}
        return render(request, 'user/follow_unfollow.html', context)