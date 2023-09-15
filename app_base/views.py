from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from . import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import AddUserToGroupForm, RemoveUserFromGroupForm, MuUserForm


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


# //-------------------------------------------------~~-------------------------------------------------


def usergroups_view(request):
    groups = Group.objects.all()
    return render(request, "app_base/grouppage.html", {"groups": groups})


# def groupdetail_view(request, group_id):
#     group = Group.objects.get(pk=group_id)
#     users = group.user_set.all()
#     return render(request, "app_base/groupdetail.html", {"group": group, "users": users})


def groupdetail_view(request, group_id):
    group = Group.objects.get(pk=group_id)
    users = group.user_set.all()

    if request.method == "POST":
        add_user_form = AddUserToGroupForm(request.POST)
        remove_user_form = RemoveUserFromGroupForm(request.POST)

        if add_user_form.is_valid():
            user_to_add = add_user_form.cleaned_data["user"]
            group.user_set.add(user_to_add)

        if remove_user_form.is_valid():
            users_to_remove = remove_user_form.cleaned_data["users"]
            group.user_set.remove(*users_to_remove)

        return redirect("groupdetail_view_name", group_id=group_id)

    else:
        add_user_form = AddUserToGroupForm()
        remove_user_form = RemoveUserFromGroupForm()

    return render(
        request,
        "app_base/groupdetail.html",
        {
            "group": group,
            "users": users,
            "add_user_form": add_user_form,
            "remove_user_form": remove_user_form,
        },
    )


def groupcreate_view(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                # Group created successfully
                # You can perform any additional actions here
                return redirect("usergroups_view_name")  # Redirect to a group list view

    return render(request, "app_base/groupcreate.html")


# //-------------------------------------------------~~-------------------------------------------------


def muuserlist_view(request):
    users = models.MuUser.objects.all()
    return render(request, "app_base/userlist.html", {"users": users})


def muusercreate_view(request):
    if request.method == "POST":
        form = MuUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("muuserlist_view_name")
    else:
        form = MuUserForm()
    return render(request, "app_base/usercreate.html", {"form": form})


def muuserupdate_view(request, pk):
    user = get_object_or_404(models.MuUser, pk=pk)
    if request.method == "POST":
        form = MuUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("muuserlist_view_name")
    else:
        form = MuUserForm(instance=user)
    return render(request, "app_base/userupdate.html", {"form": form, "user": user})


def muuserdelete_view(request, pk):
    user = get_object_or_404(models.MuUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('muuserlist_view_name')
    return render(request, 'app_base/userdelete.html', {'user': user})
