from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('post/', views.post_view, name='post')
]