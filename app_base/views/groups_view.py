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


@login_required
def groupdetail_view(request, group_id):
    group = get_object_or_404(MuGroup, pk=group_id)
    all_users = MuUser.objects.all()

    # Handle adding users
    if request.method == "POST" and "add_users" in request.POST:
        selected_users_ids = request.POST.getlist("add_user")
        group.user_set.add(*selected_users_ids)

    # Handle removing users
    if request.method == "POST" and "remove_users" in request.POST:
        selected_users_ids = request.POST.getlist("remove_user")
        group.user_set.remove(*selected_users_ids)

    context = {
        "group": group,
        "all_users": all_users,
    }
    return render(request, "app_base/groups/groupdetail.html", context)


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
        return redirect("usergroups_view_name")  # Redirect to a group list view

    context = {
        "group": group,
    }
    return render(request, "app_base/groups/groupdelete.html", context)
