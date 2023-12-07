from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import MuGroup, MuUser
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

# //------------------------~ GROUP ~--------------------------------------------------------------------------


def is_staff(user):
    return user.is_staff


@login_required
def grouplist_view(request):
    groups = MuGroup.objects.all()
    per_page = 10  # You can adjust this as needed
    paginator = Paginator(groups, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/groups/grouplist.html", {"page": page})


@login_required
def grouplistmasked_view(request):
    groups = MuGroup.all_objects.get_deleted()  # silinenler
    per_page = 10  # You can adjust this as needed
    paginator = Paginator(groups, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/groups/grouplistmasked.html", {"page": page})


@login_required
@user_passes_test(is_staff)
def groupcreate_view(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        if group_name:
            group, created = MuGroup.objects.get_or_create(name=group_name)
            if created:
                # Group created successfully
                # You can perform any additional actions here
                return redirect("grouplist_view_name")  # Redirect to a group list view

    return render(request, "app_base/groups/groupcreate.html")


# @login_required
# def groupdetail_view(request, group_id):
#     group = get_object_or_404(MuGroup, pk=group_id)
#     all_users = MuUser.objects.all()

#     # Handle adding users
#     if request.method == "POST" and "add_users" in request.POST:
#         selected_users_ids = request.POST.getlist("add_user")
#         group.user_set.add(*selected_users_ids)

#     # Handle removing users
#     if request.method == "POST" and "remove_users" in request.POST:
#         selected_users_ids = request.POST.getlist("remove_user")
#         group.user_set.remove(*selected_users_ids)

#     context = {
#         "group": group,
#         "all_users": all_users,
#     }
#     return render(request, "app_base/groups/groupdetail.html", context)
# from django.shortcuts import render, get_object_or_404
# from ..models import MuGroup, MuUser

# def groupdetail_view(request, group_id):
#     group = get_object_or_404(MuGroup, pk=group_id)
#     all_users = MuUser.objects.all()

#     if request.method == "POST":
#         if "add_users" in request.POST:
#             selected_users_ids = request.POST.getlist("add_user")
#             group.user_set.add(*selected_users_ids)
#         elif "remove_users" in request.POST:
#             selected_users_ids = request.POST.getlist("remove_user")
#             group.user_set.remove(*selected_users_ids)

#     context = {
#         "group": group,
#         "all_users": all_users,
#     }
#     return render(request, "app_base/groups/groupdetail.html", context)

from django.shortcuts import get_object_or_404

# from django.contrib.auth.models import User  # Assuming MuUser is a custom model that extends User


def groupdetail_view(request, group_id):
    group = get_object_or_404(MuGroup, pk=group_id)
    all_users = MuUser.objects.all()  # Use the appropriate User model here

    if request.method == "POST":
        if "add_users" in request.POST:
            selected_usernames = request.POST.getlist("add_user")
            selected_users = MuUser.objects.filter(username__in=selected_usernames)
            group.user_set.add(*selected_users)
        elif "remove_users" in request.POST:
            selected_usernames = request.POST.getlist("remove_user")
            selected_users = MuUser.objects.filter(username__in=selected_usernames)
            group.user_set.remove(*selected_users)

    context = {
        "group": group,
        "all_users": all_users,
    }
    return render(request, "app_base/groups/groupdetail.html", context)


from django.http import JsonResponse
from ..models import MuUser


def user_autocomplete(request):
    query = request.GET.get("query", "")
    users = MuUser.objects.filter(username__icontains=query).values("id", "username")
    return JsonResponse(list(users), safe=False)


@login_required
def groupupdate_view(request, group_id):
    group = get_object_or_404(MuGroup, pk=group_id)

    if request.method == "POST":
        group_name = request.POST.get("group_name")
        if group_name:
            group.name = group_name
            group.save()
            # Group updated successfully
            # You can perform any additional actions here
            return redirect("grouplist_view_name")  # Redirect to a group list view

    context = {
        "group": group,
    }
    return render(request, "app_base/groups/groupupdate.html", context)


@login_required
def groupdelete_view(request, group_id):
    group = get_object_or_404(MuGroup, pk=group_id)

    if request.method == "POST":
        # Confirm deletion
        group.delete()
        # Group deleted successfully
        # You can perform any additional actions here
        return redirect("grouplist_view_name")  # Redirect to a group list view

    context = {
        "group": group,
    }
    return render(request, "app_base/groups/groupdelete.html", context)
