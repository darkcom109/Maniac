from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
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
            return HttpResponse("Signup Successful!")
        else:
            return HttpResponse(f"Form errors: {form.errors}")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form' : form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse(f"Welcome back, {user.username}!")
        else: 
            return HttpResponse(f"Login failed. Errors: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form' : form})