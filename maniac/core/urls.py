from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('post/', views.post_view, name='post'),
    path('post/<int:post_id>/edit/', views.edit_post, name="edit_post"),
    path('post/<int:post_id>delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/view/', views.view_post, name='view_post'),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("users/", views.view_users, name="view_users"),
    path("leaderboard/", views.leaderboard, name="leaderboard")
]