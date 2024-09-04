from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.show_page, name="show_page"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("random_page/", views.random_page, name="random_page"),
    path("edit/", views.edit, name="edit")
]
