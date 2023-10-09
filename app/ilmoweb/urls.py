"""Module for routing urls."""
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home_page_view, name="home"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("created_labs/", views.created_labs, name="created_labs"),
    path("create_lab/", views.create_lab, name="create_lab"),
    path("open_labs/", views.open_labs, name="open_labs"),
    path("open_labs/confirm/", views.confirm, name="confirm"),
    path("delete_lab/<int:course_id>", views.delete_lab, name="delete_lab"),
]
