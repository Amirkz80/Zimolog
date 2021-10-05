from django.shortcuts import render, redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserInfo
from blogs.models import BlogPost


def get_user_info(req, user_name_string):
    """"Gets UserInfo that is conected to the the user"""
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
    user_posts = BlogPost.objects.filter(owner=request.user).order_by("-date_added")

    context = {'user_posts' : user_posts, 'date_joined' : date_joined}
    return render(request, 'user/dashboard.html', context)


@login_required
def followers(request,user_name):
    """Shows user's followers"""
    user = get_user_info(request, user_name)
    context ={'user' : user}
    return render(request, 'user/followers.html', context)


@login_required
def following(request,user_name):
    """Shows user's following"""
    user = get_user_info(request, user_name)
    context = {'user' : user}
    return render(request, 'user/following.html', context)


@login_required
def user_info(request, user_name): 
    """Returns user's(not authenticated user) posts and info"""

    # If currnet authenticated user is trying to see h/h page, redirect to h/h dashboard
    if request.user.username == user_name:
        return redirect('users:dashboard')
    
    user = get_user_info(request, user_name)
    posts = user.blogpost_set.order_by("-date_added")
    context = {'user' : user, 'posts' : posts}
    return render(request, 'user/user_info.html', context)       