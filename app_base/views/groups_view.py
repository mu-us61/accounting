from django.contrib.auth.decorators import login_required, user_passes_test
from ..models import MuGroup, MuUser
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from ..tables import GroupTable
from ..filters import MuGroupFilter, MuGroupFilterMasked
from ..izinler import WritePermissionRequiredMixin, DeletePermissionRequiredMixin, func_delete_permission_required, func_write_permission_required

# from ..filters import

# //------------------------~ GROUP ~--------------------------------------------------------------------------


def is_staff(user):
    return user.is_staff


# @login_required
# def grouplist_view(request):
#     groups = MuGroup.objects.all()
#     per_page = 10  # You can adjust this as needed
#     paginator = Paginator(groups, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)

#     return render(request, "app_base/groups/grouplist.html", {"page": page})


# @login_required
# def grouplistmasked_view(request):
#     groups = MuGroup.all_objects.get_deleted()  # silinenler
#     per_page = 10  # You can adjust this as needed
#     paginator = Paginator(groups, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)


#     return render(request, "app_base/groups/grouplistmasked.html", {"page": page})
class GroupListView(SingleTableMixin, FilterView):
    table_class = GroupTable
    model = MuGroup
    template_name = "app_base/groups/grouplist.html"
    # context_table_name = "etkinlik_table"
    filterset_class = MuGroupFilter


class GroupListMaskedView(SingleTableMixin, FilterView):
    table_class = GroupTable
    model = MuGroup
    template_name = "app_base/groups/grouplistmasked.html"
    # context_table_name = "etkinlik_table"
    filterset_class = MuGroupFilterMasked

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


# @login_required
# @user_passes_test(is_staff)
# @func_write_permission_required
# def groupcreate_view(request):
#     if request.method == "POST":
#         group_name = request.POST.get("group_name")
#         can_write = request.POST.get("can_write") == "on"
#         can_delete = request.POST.get("can_delete") == "on"
#         if group_name:
#             group, created = MuGroup.objects.get_or_create(name=group_name)
#             if created:
#                 group.can_write = can_write
#                 group.can_delete = can_delete
#                 group.save()
#                 # Group created successfully
#                 # You can perform any additional actions here
#                 return redirect("grouplist_view_name")  # Redirect to a group list view


#     return render(request, "app_base/groups/groupcreate.html")
@login_required
@user_passes_test(is_staff)
@func_write_permission_required
def groupcreate_view(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        can_write = request.POST.get("can_write") == "on"
        can_delete = request.POST.get("can_delete") == "on"

        # Check if the MuGroup with the given name already exists
        existing_mu_group = MuGroup.objects.filter(name=group_name).first()

        if existing_mu_group is None:
            # MuGroup with this name doesn't exist, create a new one
            new_mu_group = MuGroup(name=group_name, can_write=can_write, can_delete=can_delete)
            new_mu_group.save()

            # Assign the MuGroup to the user or perform any other necessary actions
            # For example, if you have a user object, you can do:
            # user.gruplar.add(new_mu_group)
            # user.save()

            return redirect("grouplist_view_name")  # Redirect to a group list view

        # If MuGroup with this name already exists, handle accordingly
        # You might want to display an error message or take other actions

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


# def groupdetail_view(request, group_id):
#     group = get_object_or_404(MuGroup.all_objects, pk=group_id)
#     all_users = MuUser.objects.all()  # Use the appropriate User model here

#     if request.method == "POST":
#         if "add_users" in request.POST:
#             selected_usernames = request.POST.getlist("add_user")
#             selected_users = MuUser.objects.filter(username__in=selected_usernames)
#             group.user_set.add(*selected_users)
#         elif "remove_users" in request.POST:
#             selected_usernames = request.POST.getlist("remove_user")
#             selected_users = MuUser.objects.filter(username__in=selected_usernames)
#             group.user_set.remove(*selected_users)

#     context = {
#         "group": group,
#         "all_users": all_users,
#     }
#     return render(request, "app_base/groups/groupdetail.html", context)
from django.shortcuts import render, get_object_or_404
from ..models import MuGroup, MuUser


def groupdetail_view(request, group_id):
    group = get_object_or_404(MuGroup.all_objects, pk=group_id)
    all_users = MuUser.objects.all()

    if request.method == "POST":
        if "add_users" in request.POST:
            selected_usernames = request.POST.getlist("add_user")
            selected_users = MuUser.objects.filter(username__in=selected_usernames)
            for user in selected_users:
                user.gruplar.add(group)
        elif "remove_users" in request.POST:
            selected_usernames = request.POST.getlist("remove_user")
            selected_users = MuUser.objects.filter(username__in=selected_usernames)
            for user in selected_users:
                user.gruplar.remove(group)

    context = {
        "group": group,
        "all_users": all_users,
        "muuser": MuUser.objects.all(),  # eklendi
    }
    return render(request, "app_base/groups/groupdetail.html", context)


from django.http import JsonResponse
from ..models import MuUser


def user_autocomplete(request):
    query = request.GET.get("query", "")
    users = MuUser.objects.filter(username__icontains=query).values("id", "username")
    return JsonResponse(list(users), safe=False)


# @login_required
# def groupupdate_view(request, group_id):
#     group = get_object_or_404(MuGroup.all_objects, pk=group_id)

#     if request.method == "POST":
#         group_name = request.POST.get("group_name")
#         if group_name:
#             group.name = group_name
#             group.save()
#             # Group updated successfully
#             # You can perform any additional actions here
#             return redirect("grouplist_view_name")  # Redirect to a group list view

#     context = {
#         "group": group,
#     }
#     return render(request, "app_base/groups/groupupdate.html", context)
from django.shortcuts import render, get_object_or_404, redirect
from ..models import MuGroup


# @login_required
# @func_write_permission_required
# def groupupdate_view(request, group_id):
#     group = get_object_or_404(MuGroup.all_objects, pk=group_id)

#     if request.method == "POST":
#         group_name = request.POST.get("group_name")
#         is_active = request.POST.get("is_active") == "on"  # Checkbox value handling
#         if group_name:
#             group.name = group_name
#             group.is_active = is_active  # Assign the is_active value
#             group.save()
#             # Group updated successfully
#             # You can perform any additional actions here
#             return redirect("grouplist_view_name")  # Redirect to a group list view


#     context = {
#         "group": group,
#     }
#     return render(request, "app_base/groups/groupupdate.html", context)
@login_required
@func_write_permission_required
def groupupdate_view(request, group_id):
    group = get_object_or_404(MuGroup.all_objects, pk=group_id)

    if request.method == "POST":
        group_name = request.POST.get("group_name")
        is_active = request.POST.get("is_active") == "on"  # Checkbox value handling
        can_write = request.POST.get("can_write") == "on"  # Checkbox value handling
        can_delete = request.POST.get("can_delete") == "on"  # Checkbox value handling

        if group_name:
            group.name = group_name
            group.is_active = is_active  # Assign the is_active value
            group.can_write = can_write  # Assign the can_write value
            group.can_delete = can_delete  # Assign the can_delete value
            group.save()
            # Group updated successfully
            # You can perform any additional actions here
            return redirect("grouplist_view_name")  # Redirect to a group list view

    context = {
        "group": group,
    }
    return render(request, "app_base/groups/groupupdate.html", context)


@login_required
@func_delete_permission_required
def groupdelete_view(request, group_id):
    group = get_object_or_404(MuGroup.all_objects, pk=group_id)

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
