from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('post/', views.post_view, name='post')
]