from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed/", views.closed_listings, name="closed_listings"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("<str:title>", views.show_page, name="page"),
    path("add_watch/", views.add_watch, name="add_watch"),
    path("view_watch/", views.view_watch, name="view_watch"),
    path("remove_watch/", views.remove_watch, name="remove_watch"),
    path("bid/", views.bid, name="bid"),
    path("close_auction/", views.close_auction, name="close_auction"),
    path("add_comment/", views.add_comment, name="add_comment"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:title>", views.category, name="category")
]
