from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from . import models
from django.contrib.auth.decorators import login_required


# Create your views here.
def bakiye_view(request):
    users = models.MuUser.objects.all()  # Retrieve all MuUser objects from the database
    context = {"users": users}
    return render(request, "app_base/bakiye.html", context)


def home_view(request):
    return render(request, template_name="app_base/home.html")


def passchange_view(request):
    if request.method == "POST":
        hashed_pass = request.user.password
        if request.POST.get("password1") == request.POST.get("password2") and check_password(request.POST.get("password_old"), hashed_pass):
            u = models.MuUser.objects.get(username=request.user.username)
            u.set_password(request.POST.get("password1"))
            u.save()
            logout(request)
            return redirect("home_view_name")
        else:
            return render(request, template_name="app_base/change_password.html")

    if request.method == "GET":
        return render(request, template_name="app_base/change_password.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect("home_view_name")
        else:
            # Return an 'invalid login' error message.
            return render(request, template_name="app_base/login.html")
    if request.method == "GET":
        return render(request, template_name="app_base/login.html")


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("home_view_name")


@login_required
def profile_view(request):
    # user_profile = UserProfile.objects.get(user=request.user)
    user_profile = "deneme"
    return render(request, "app_base/profile.html", {"user_profile": user_profile})
