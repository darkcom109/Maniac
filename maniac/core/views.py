from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

# Create your views here.

def feed(request):
    return render(request, 'core/feed.html')

def profile(request, username):
    return render(request, 'core/profile.html', {'username': username})

def login_view(request):
    return render(request, 'core/login.html')

def post_view(request):
    return render(request, 'core/post.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("USER ADDED TO DB")
            return HttpResponse("Signup Successful!")
        else:
            print("USER WAS NOT ADDED TO DB")
            return HttpResponse(f"Form errors: {form.errors}")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form' : form})
