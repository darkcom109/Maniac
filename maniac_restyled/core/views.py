from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .forms import PostForm, CommentForm
from .models import Post, Comment

# Page Views
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/feed.html', {'posts': posts})

@login_required(login_url='login')
def profile(request, username):
    user = User.objects.get(username=username)
    total_likes = Post.objects.filter(author=user).aggregate(total=Count('likes'))['total']
    return render(request, 'core/profile.html', {'profile_user': user, 'total_likes': total_likes})

@login_required(login_url='login')
def view_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'core/view_users.html', {'users': users})

@login_required(login_url='login')
def leaderboard(request):
    users = User.objects.annotate(
        total_likes=Count('post__likes')
    ).order_by('-total_likes')
    return render(request, 'core/leaderboard.html', {'users': users})

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
        messages.success(request, "YOU DISLIKED THIS POST?")
    else:
        post.likes.add(request.user)
        messages.success(request, "YOU LIKED THIS POST!")

    return redirect('view_post', post.id)

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
        return redirect('login')
    except:
        return messages.error(request, "Failed to Logout. Try Again")

# Comment Section
@login_required(login_url='login')
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('view_post', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'core/view_post.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post.id  # so we can redirect back to the post after deleting

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect("view_post", post_id=post_id)

    return render(request, "core/delete_comment.html", {"comment": comment})

