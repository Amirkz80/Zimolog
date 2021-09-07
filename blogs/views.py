from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import BlogPost
from .forms import BlogPostForm

    
def index(request):
    """Shows the posts in the main page"""
    posts = BlogPost.objects.order_by('-date_added')
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
