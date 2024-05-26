from ..forms import MuUserForm
from ..models import MuUser, MuGroup
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from ..tables import MuUserTable, DeletedMuUserTable

from ..filters import MuUserFilter, MuUserFilterMasked


# //------------------------~ USER ~--------------------------------------------------------------------------
def is_staff(user):
    return user.is_staff


# @login_required
# def userlist_view(request):
#     users = MuUser.objects.all()

#     # Number of users to display per page
#     per_page = 10  # You can adjust this as needed

#     paginator = Paginator(users, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)

#     return render(request, "app_base/users/userlist.html", {"page": page})


# def userlistmasked_view(request):
#     users = MuUser.all_objects.get_deleted()

#     # Number of users to display per page
#     per_page = 10  # You can adjust this as needed

#     paginator = Paginator(users, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)


#     return render(request, "app_base/users/userlistmasked.html", {"page": page})
class UserListView(SingleTableMixin, FilterView):
    table_class = MuUserTable
    model = MuUser
    template_name = "app_base/users/userlist.html"
    # context_table_name = "etkinlik_table"
    filterset_class = MuUserFilter


class UserListMaskedView(SingleTableMixin, FilterView):
    table_class = DeletedMuUserTable
    model = MuUser
    template_name = "app_base/users/userlistmasked.html"
    # context_table_name = "etkinlik_table"
    filterset_class = MuUserFilterMasked

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ..models import MuUser  # Import your User model here


# @require_POST
# def reactivate_user(request):
#     if request.method == "POST":
#         user_id = request.POST.get("user_id")
#         print(user_id)
#         try:
#             user = MuUser.objects.get(pk=user_id)
#             print(user)
#             user.is_active = True
#             user.save()
#             return JsonResponse({"success": True})
#         except MuUser.DoesNotExist:
#             return JsonResponse({"success": False, "error": "User not found"})
#     else:
#         return JsonResponse({"success": False, "error": "Invalid request method"})

import logging
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ..models import MuUser

logger = logging.getLogger(__name__)


@require_POST
def reactivate_user(request):
    try:
        user_id = request.POST.get("user_id")
        logger.info("Received request to reactivate user with ID: %s", user_id)
        user = MuUser.all_objects.get(pk=user_id)
        user.is_active = True
        user.save()
        logger.info("User reactivated successfully")
        return redirect("userlist_view_name")
    except MuUser.DoesNotExist:
        logger.error("User not found with ID: %s", user_id)
        return JsonResponse({"success": False, "error": "User not found"})
    except Exception as e:
        logger.exception("Error occurred while reactivating user")
        return JsonResponse({"success": False, "error": str(e)})


# @login_required
# @user_passes_test(is_staff)
# def usercreate_view(request):
#     if request.method == "POST":
#         form = MuUserForm(request.POST)
#         if form.is_valid():
#             # print("Form data:")
#             # for field in form:
#             #     print(f"{field.name}: {field.value()}")
#             # form.instance.is_active = True
#             form.save()
#             # Get or create the default group
#             default_group, created = MuGroup.objects.get_or_create(name="Default Group")

#             # If the group is newly created, set its permissions to default
#             if created:
#                 default_permissions = Yetkiler.objects.create()
#                 default_group.yetkiler = default_permissions
#                 default_group.save()

#             # Add the user to the default group
#             MuUser.groups.add(default_group)

#             return redirect("userlist_view_name")
#     else:
#         form = MuUserForm()

#     return render(request, "app_base/users/usercreate.html", {"form": form})


@login_required
@user_passes_test(is_staff)
def usercreate_view(request):
    if request.method == "POST":
        form = MuUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Get or create a Yetkiler instance (if necessary)
            yetkiler_instance, created = Yetkiler.objects.get_or_create(
                # You can provide default values for the Yetkiler fields here if needed
            )

            # Get or create the MuGroup instance
            mu_group_instance, created = MuGroup.objects.get_or_create(name="DefaultGroup", yetkiler=yetkiler_instance)  # Assign the Yetkiler instance to the yetkiler field

            # Add the MuGroup instance to the created user
            user.gruplar.add(mu_group_instance)

            return redirect("userlist_view_name")
    else:
        form = MuUserForm()

    return render(request, "app_base/users/usercreate.html", {"form": form})


@login_required
@user_passes_test(is_staff)
def userupdate_view(request, pk):
    muser = get_object_or_404(MuUser.all_objects, pk=pk)
    if request.method == "POST":
        form = MuUserForm(request.POST, instance=muser)
        if form.is_valid():
            form.save()
            return redirect("userlist_view_name")
    else:
        form = MuUserForm(instance=muser)
    return render(request, "app_base/users/userupdate.html", {"form": form, "muser": muser})


@login_required
@user_passes_test(is_staff)
def userdelete_view(request, pk):
    user = get_object_or_404(MuUser.all_objects, pk=pk)
    # user = MuUser.all_objects.get(pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("userlist_view_name")
    return render(request, "app_base/users/userdelete.html", {"user": user})
