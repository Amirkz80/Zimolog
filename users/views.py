from datetime import datetime
from time import strftime
import cloudinary
from django.shortcuts import render, redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from users.models import UserInfo
from blogs.models import BlogPost
from .forms import UserInfoForm
# Using pagianator featrue to break pages into pieces
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  


def pagination_func(request, list_objects, objects_per_page):
    """Paginates the the lists and return posts and page"""
    page = request.GET.get('page')
    
    paginator = Paginator(list_objects, objects_per_page)
    try:
        posts = paginator.page(page)
    # Retrun first page if page number is not an integer
    except PageNotAnInteger:
        posts= paginator.page(1)
    # Retrun last pages if page number is out of index
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    output = {'posts' : posts, 'page' : page}
    return output


def delete_username_and_save(object_list):
    """Check and upgrade if a user is deleted from database"""
    change = False
    for user in object_list :
        try :
            User.objects.get(username = user)
        except User.DoesNotExist :    
            object_list.remove(user)
            change = True
    
    return(change) 


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


def has_pro_pic(user):
    """Checks if the user has profile photo or not"""
    pic_flag = True 

    if user.userinfo.picture.name == 'False':
        pic_flag = False
    else:
        pass
    
    return pic_flag


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
            # now we log in and then go to the get_bio page
            login(request, new_user)
            context = {'form' : UserInfoForm() }
            return render(request, 'registration/bio.html', context)
    
    context = {'form' : form}
    return render(request, 'registration/register.html', context)

 
@login_required
def get_bio(request):
    """Takes profile pic from user in register page, optional"""
    
    if request.method != 'POST':
        form = UserInfoForm(instance=request.user.userinfo)
    else:
        form = UserInfoForm(request.POST, request.FILES, instance=request.user.userinfo)
    
        if form.is_valid():
            new_bio = form.save(commit=False)
            new_bio.user = request.user
            new_bio = form.save()
            return redirect('users:dashboard')


    # Shows a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/bio.html', context)


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
    
    # deleting person from followers and updating followers num if he's been deleted by admin or h/h self
    if delete_username_and_save(request.user.userinfo.followers) :
        request.user.userinfo.followers_number = len(request.user.userinfo.followers)
        request.user.userinfo.save()

    # deleting person from following and updating following num if he's been deleted by admin or h/h self
    if delete_username_and_save(request.user.userinfo.following) :
        request.user.userinfo.following_number = len(request.user.userinfo.following)
        request.user.userinfo.save()

    first_post_id = ''
    for post in user_posts:
        # deleting person from liked people and updating hearts if he's been deleted by admin or h/h self
        if delete_username_and_save(post.people_who_liked) :
            post.heart = len(post.people_who_liked)
            post.save()

        post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted") 
        first_post_id = post.id

    # Pagintaing anonymos user page
    posts_and_page = pagination_func(request, user_posts, 5)
    user_posts = posts_and_page['posts']
    page  =  posts_and_page['page']

    context = {'user_posts' : user_posts, 'page' : page, 'join_message' : join_message, 'first_post_id' : first_post_id}
    return render(request, 'user/dashboard.html', context)


@login_required
def followers(request,user_name):
    """Shows user's followers"""
    current_user = get_user(user_name)
    all_users = User.objects.all()
    followers_list = []

    for user in all_users:
        if user.username in current_user.userinfo.followers:
            followers_list.append(user)

    context ={'user' : current_user, 'followers' : followers_list}
    return render(request, 'user/followers.html', context)


@login_required
def following(request,user_name):
    """Shows user's following"""
    current_user = get_user(user_name)
    all_users = User.objects.all()
    following_list = []

    for user in all_users:
        if user.username in current_user.userinfo.following:
            following_list.append(user)
    
    context = {'user' : current_user, 'followings' : following_list}
    return render(request, 'user/following.html', context)


@login_required
def user_info(request, user_name): 
    """Returns user's(not authenticated user) posts and info"""

    # If currnet authenticated user is trying to see h/h page, redirect to h/h dashboard
    if request.user.username == user_name:
        return redirect('users:dashboard')
    
    # calculating the time that user has joined the blog
    user = get_user(user_name)
    posts = user.blogpost_set.order_by("-date_added")
    join_message = calculate_time(user.date_joined, datetime.utcnow(), keyword="joined")

    # deleting person from followers and updating followers num if he's been deleted by admin or h/h self
    if delete_username_and_save(user.userinfo.followers) :
        user.userinfo.followers_number = len(user.userinfo.followers)
        user.userinfo.save()

    # deleting person from following and updating following num if he's been deleted by admin or h/h self
    if delete_username_and_save(user.userinfo.following) :
        user.userinfo.following_number = len(user.userinfo.following)
        user.userinfo.save()

    # Calculating the time that user's posts has been posted by user
    first_post_id = ''
    for post in posts:
        # deleting person from liked people and updating hearts if he's been deleted by admin or h/h self
        if delete_username_and_save(post.people_who_liked) :
            post.heart = len(post.people_who_liked)
            post.save()
        
        post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword='posted')
        first_post_id = post.id


    # Pagintaing anonymos user page
    posts_and_page = pagination_func(request, posts, 5)
    posts = posts_and_page['posts']
    page  =  posts_and_page['page']

    context = {'requested_user' : user, 'posts' : posts, 'page' : page, 'join_message' : join_message, 'first_post_id' : first_post_id}
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
        selected_user_info.followers_number = len(selected_user_info.followers)
        selected_user_info.save(update_fields=['followers', 'followers_number'])
        
        currnet_user_info.following.remove(selected_username)
        currnet_user_info.following_number = len(currnet_user_info.following)
        currnet_user_info.save(update_fields=['following', 'following_number'])

        flag = 0 
        context = {'flag' : flag, 'user_name' : selected_username}
        return redirect('users:user_info', user_name)

    #If user is not in selected user's followers, does unfollow
    else:
        # Making empty lists if these to lists have no member
        if bool(selected_user_info.followers) is False:
            selected_user_info.followers = []
        if bool(currnet_user_info.following) is False:
            currnet_user_info.followers = []    
        
        selected_user_info.followers.append(current_usernname)
        selected_user_info.followers_number = len(selected_user_info.followers)
        selected_user_info.save(update_fields=['followers', 'followers_number'])
        
        currnet_user_info.following.append(selected_username)
        currnet_user_info.following_number = len(currnet_user_info.following)
        currnet_user_info.save(update_fields=['following', 'following_number'])

        flag = 1
        context = {'flag' : flag, 'user_name' : selected_username}
        return redirect('users:user_info', user_name)