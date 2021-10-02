from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from blogs.models import BlogPost

def register(request):
    """Registers new user"""
    if request.method != 'POST':
        # Sets form to a blank page
        form = UserCreationForm()
    else:
        # Processes user data and login
            form = UserCreationForm(data=request.POST)

            if form.is_valid():
                new_user = form.save()
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
    return render(request, 'registration/dashboard.html', context)