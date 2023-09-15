from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view_name"),
    path("passchange", views.passchange_view, name="passchange_view_name"),
    path("login", views.login_view, name="login_view_name"),
    path("logout", views.logout_view, name="logout_view_name"),
    path("profile/", views.profile_view, name="profile_view_name"),
    path("bakiye", views.bakiye_view, name="bakiye_view_name"),
]
