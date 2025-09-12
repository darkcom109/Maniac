from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def feed(request):
    return render(request, 'core/feed.html')

def profile(request, username):
    return render(request, 'core/profile.html', {'username': username})

def login_view(request):
    return render(request, 'core/login.html')

def signup_view(request):
    return render(request, 'core/signup.html')

def post_view(request):
    return render(request, 'core/post.html')