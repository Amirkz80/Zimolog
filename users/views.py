from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

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