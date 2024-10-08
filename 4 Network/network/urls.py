
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("<str:name>", views.profile, name="profile"),
    path("follow/", views.follow, name="follow"),
    path("unfollow/", views.unfollow, name="unfollow"),
    path("following/", views.following, name="following"),

    #API route
    path("edit/<int:tweet_id>", views.edit, name="edit"),
    path("like/<int:tweet_id>", views.like, name="like")

]
