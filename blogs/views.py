import time
from datetime import datetime
from django.core import paginator
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from users.models import UserInfo
from .models import BlogPost, Comments
from .forms import BlogPostForm, CommentsForm
from users.views import calculate_time, delete_username_and_save
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


def about(request):
    """Shows about page"""
    return render(request, 'blogs/about.html')


def index(request):
    """Shows the posts in the main page"""
    comments_number = {}
    first_post_id = ''
    # a dictioanry to save the number of comments
    if request.user.is_authenticated == False :
        posts = BlogPost.objects.order_by('-date_added')
        for post in posts:
            # deleting person from liked people and updating hearts if he's been deleted by admin or h/h self
            if delete_username_and_save(post.people_who_liked) :
                post.heart = len(post.people_who_liked)
                post.save()
            
            if len(post.text) > 140 :
                post.text = f"{post.text[:140]}..." 
            post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted")
            comments_number[post.id] = len(post.comments_set.all())
            first_post_id = post.id


        # Pagintaing anonymos user page
        posts_and_page = pagination_func(request, posts, 5)
        posts = posts_and_page['posts']
        page  =  posts_and_page['page']

        context = {'posts' : posts, 'page' : page, 'comments_number' : comments_number, 'first_post_id' : first_post_id }

    
    else:
        user_timeline_posts = []
        posts = BlogPost.objects.all().order_by("-date_added")
        for post in posts:
            # Check to only show posts from whome user follows and shwo h/h posts
            if post.owner.username in request.user.userinfo.following or post.owner.username == request.user.username:
                if len(post.text) > 140 :
                    post.text = f"{post.text[:140]}..." 
                post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted")
                user_timeline_posts.append(post)
                comments_number[post.id] = len(post.comments_set.all())
                first_post_id = post.id


        # Pagintaing sigend in user page
        posts_and_page = pagination_func(request, user_timeline_posts, 5)
        posts = posts_and_page['posts']
        page  =  posts_and_page['page']

        context = {'posts' : posts, 'page' : page, 'comments_number' : comments_number, 'first_post_id' : first_post_id}

    return render(request, 'blogs/index.html', context)


@login_required
def add_post(request):
    """Adds a new post"""
    if request.method != 'POST':
        # There is no submitted data , creates a blank form
        form = BlogPostForm()
    else:
        # Processing data
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post = form.save()
            return redirect('blogs:index')

    context = {'form': form}
    return render(request, 'blogs/add_post.html', context)     


@login_required
def edit_post(request, post_id):
    """Edits a post"""
    post = BlogPost.objects.get(id=post_id)
    """Checks if the current logged in user is post's owner"""
    if request.user != post.owner:
        return render(request, 'blogs/prompt.html')

    if request.method != 'POST':
        # initial request, pre-fills the form with currnet post
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted, porcessing data
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    context = {'form' : form, 'post' : post}
    return render(request, 'blogs/edit_post.html', context)


@login_required
def search(request):
    """searches the user's keyword and shows results"""

    #getting user's search keyword
    key = request.GET.get('search')

    post_results = []
    user_results = []
    flag = True

    # search key in the users and posts in database
    posts = BlogPost.objects.order_by('-date_added')
    first_post_id = ''
    for post in posts:
        if (key.lower() in post.text.lower()) or (key.lower() in post.title.lower()):
            # deleting person from liked people and updating hearts if he's been deleted by admin or h/h self
            if delete_username_and_save(post.people_who_liked) :
                post.heart = len(post.people_who_liked)
                post.save()

            post_results.append(post)
            # Calculating postst's time 
            post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword=('posted'))
            first_post_id = post.id
        
    users = User.objects.all()
    for user in users:
        if (key.lower() in user.username.lower()):
            user_results.append(user)

    # Check if both user and post results are empty   
    if post_results == [] and user_results == []:
        flag = False


    context = {'posts' : post_results, 'users' : user_results, 'key' : key, 'flag' : flag, 'first_post_id' : first_post_id}
    return render(request, 'blogs/results.html', context)


@login_required
def delete(request, post_id):
    """Deletes the post"""
    BlogPost.objects.get(id=post_id).delete()
    
    time.sleep(0.2)

    return redirect('users:dashboard')


def full_post(request, post_id):
    """Renders the post in its full shape and show its comments"""

    post = BlogPost.objects.get(id=post_id)
    comments = Comments.objects.filter(post=post).order_by("-date_added")

    # deleting person from liked people and updating hearts if he's been deleted by admin or h/h self
    if delete_username_and_save(post.people_who_liked) :
        post.heart = len(post.people_who_liked)
        post.save()

    post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted")
    
    comments_number = len(post.comments_set.all())
    
    context = {'post' : post, 'comments' : comments, 'comments_number' : comments_number }
    return render(request, 'blogs/full_post.html', context)


@login_required
def add_comment(request, post_id):
    """Adds a comment to the post"""
    post = BlogPost.objects.get(id=post_id)

    if request.method != 'POST':
        # there is no submitted data so the form is blank
        form = CommentsForm()
    else:
        # proccessing data
        form = CommentsForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post = post
            new_comment = form.save()
            return redirect('blogs:full_post', post_id)

    context = {'form' : form, 'post' : post}
    return render(request, 'blogs/add_comment.html', context)


@login_required
def like(request, post_id):
    """Increase post's hearts by one,if user's voted already decrease by one"""
    post = BlogPost.objects.get(id=post_id)
    user_name = str(request.user.username)
    next = request.POST.get('next', '/')

    #If user has liked before, decreases hearts by one
    if user_name in post.people_who_liked:
        post.people_who_liked.remove(user_name)
        post.heart = len(post.people_who_liked)
        post.save()
        flag = 0 
        context = {'flag' : flag}
        return HttpResponseRedirect(next)

    #If user hasn't liked before,increases hearts by one
    else:
        if bool(post.people_who_liked) is False:
            post.people_who_liked = []
        post.people_who_liked.append(user_name)
        post.heart = len(post.people_who_liked)
        post.save()
        flag = 1
        context = {'flag' : flag}
        return HttpResponseRedirect(next)

@login_required
def discover(request, sort_type=''):
    """Sorts posts by their time or their hearts"""
    comments_number = {}
    first_post_id = ''
    

    if sort_type == 'time' :    
        posts = BlogPost.objects.order_by("-date_added")
        for post in posts:
            # deleting person from liked people and updating hearts if he's been deleted by admin or h/h self
            if delete_username_and_save(post.people_who_liked) :
                post.heart = len(post.people_who_liked)
                post.save()

            if len(post.text) > 140 :
                post.text = f"{post.text[:140]}..." 
            post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted")
            comments_number[post.id] = len(post.comments_set.all())
            first_post_id = post.id

        # a flag for html page
        flag = 'time'


    if sort_type == 'heart' or sort_type == '':
        posts = BlogPost.objects.order_by("-heart")
        for post in posts:
            if delete_username_and_save(post.people_who_liked) :
                post.heart = len(post.people_who_liked)
                post.save()

            if len(post.text) > 140 :
                post.text = f"{post.text[:140]}..." 
            post.date_added = calculate_time(post.date_added, datetime.utcnow(), keyword="posted")
            comments_number[post.id] = len(post.comments_set.all())
            first_post_id = post.id

        flag = 'heart'

    context = {'posts' : posts, 'flag' : flag, 'comments_number' : comments_number, 'first_post_id' : first_post_id}
    return render(request, 'blogs/discover.html', context)    
