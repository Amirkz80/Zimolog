from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import BlogPost, Comments
from .forms import BlogPostForm, CommentsForm


def index(request):
    """Shows the posts in the main page"""
    posts = BlogPost.objects.order_by('-date_added')
    for post in posts:
        if len(post.text) > 140 :
            post.text = f"{post.text[:140]}..."
    context = {'posts' : posts}

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

    results = []
    posts = BlogPost.objects.order_by('-date_added')
    for post in posts:
        if (key.lower() in post.text.lower()) or (key.lower() in post.title.lower()):
            results.append(post)

    context = {'results' : results, 'key' : key}
    return render(request, 'blogs/results.html', context)


@login_required
def dashboard(request):
    """Shows user's informations and posts"""
    date_joined = request.user.date_joined
    user_posts = BlogPost.objects.filter(owner=request.user).order_by("-date_added")
    context = {'user_posts' : user_posts, 'date_joined' : date_joined}

    return render(request, 'blogs/dashboard.html', context)


@login_required
def delete(request, post_id):
    """deletes the post"""
    BlogPost.objects.get(id=post_id).delete()

    return redirect("blogs:dashboard")


def full_post(request, post_id):
    """Renders the post in its full shape and show its comments"""
    post = BlogPost.objects.get(id=post_id)
    comments = Comments.objects.filter(post=post).order_by("-date_added")
    context = {'post' : post, 'comments' : comments }
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
            return redirect('blogs:index')

    context = {'form' : form, 'post' : post}
    return render(request, 'blogs/add_comment.html', context)

