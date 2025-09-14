from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post

# Page Views
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts})

@login_required(login_url='login')
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'core/profile.html', {'profile_user': user})

def login_view(request):
    return render(request, 'core/login.html')

# Post Views
@login_required(login_url='login')
def post_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'core/post.html', {'form': form})

@login_required(login_url='login')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = PostForm(instance=post)

    return render(request, 'core/edit_post.html', {'form': form, 'post': post})

@login_required(login_url='login')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('feed')
    
    return render(request, 'core/delete_post.html', {'post': post})

@login_required(login_url='login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('feed')

def total_likes(self):
    return self.likes.count()

# Signup, Login and Logout Views
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup Successful!")
            return redirect('login')
        else:
            messages.error(request, f"Signup Failed. {form.errors}")
            return redirect('signup')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form' : form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login Successful! Welcome to Maniac")
            return redirect('feed')
        else: 
            return messages.error(request, f"Login failed. Errors: {form.errors}")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form' : form})

def logout_view(request):
    try:
        logout(request)
        messages.success(request, "Logout Successful!")
        return redirect('feed')
    except:
        return messages.error(request, "Failed to Logout. Try Again")