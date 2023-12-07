from ..forms import MuUserForm
from ..models import MuUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator


# //------------------------~ USER ~--------------------------------------------------------------------------
def is_staff(user):
    return user.is_staff


@login_required
def userlist_view(request):
    users = MuUser.objects.all()

    # Number of users to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(users, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/users/userlist.html", {"page": page})


def userlistmasked_view(request):
    users = MuUser.all_objects.get_deleted()

    # Number of users to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(users, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/users/userlistmasked.html", {"page": page})


@login_required
@user_passes_test(is_staff)
def usercreate_view(request):
    if request.method == "POST":
        form = MuUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("userlist_view_name")
    else:
        form = MuUserForm()

    return render(request, "app_base/users/usercreate.html", {"form": form})


@login_required
@user_passes_test(is_staff)
def userupdate_view(request, pk):
    user = get_object_or_404(MuUser.all_objects, pk=pk)
    if request.method == "POST":
        form = MuUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("userlist_view_name")
    else:
        form = MuUserForm(instance=user)
    return render(request, "app_base/users/userupdate.html", {"form": form, "user": user})


@login_required
@user_passes_test(is_staff)
def userdelete_view(request, pk):
    user = get_object_or_404(MuUser, pk=pk)
    # user = MuUser.all_objects.get(pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("userlist_view_name")
    return render(request, "app_base/users/userdelete.html", {"user": user})
