from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from ..models import MuUser

# //------------------------~~--------------------------------------------------------------------------


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
            messages.error(request, "Tekrar deneyiniz")
            return render(request, template_name="app_base/authentications/login.html")
    if request.method == "GET":
        return render(request, template_name="app_base/authentications/login.html")


@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect("home_view_name")


@login_required
def passwordchange_view(request):
    if request.method == "POST":
        hashed_pass = request.user.password
        if request.POST.get("password1") == request.POST.get("password2") and check_password(request.POST.get("password_old"), hashed_pass):
            u = MuUser.objects.get(username=request.user.username)
            u.set_password(request.POST.get("password1"))
            u.save()
            logout(request)
            return redirect("home_view_name")
        else:
            messages.error(request, "Tekrar deneyiniz")
            return render(request, template_name="app_base/authentications/passwordchange.html")

    if request.method == "GET":
        return render(request, template_name="app_base/authentications/passwordchange.html")
