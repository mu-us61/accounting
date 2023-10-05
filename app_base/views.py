import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

from . import models

from .forms import MuUserForm, TagForm, TransactionForm
from .models import Islemler, MuUser, Tag, MuGroup


# //------------------------~ ANASAYFA ~--------------------------------------------------------------------------
def home_view(request):
    return render(request, template_name="app_base/home.html")


# //------------------------~ BAKIYE ~--------------------------------------------------------------------------
def bakiye_view(request):
    users = models.MuUser.objects.all()  # Retrieve all MuUser objects from the database
    context = {"users": users}
    return render(request, "app_base/bakiye.html", context)


# //------------------------~ AUTHENTICATION ~--------------------------------------------------------------------------
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
            messages.error(request, "Tekrar deneyiniz")
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
            messages.error(request, "Tekrar deneyiniz")
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


# //------------------------~ USER GROUPS ~--------------------------------------------------------------------------
def usergroups_view(request):
    groups = models.MuGroup.objects.all()
    return render(request, "app_base/grouppage.html", {"groups": groups})


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
    return render(request, "app_base/groupdetail.html", context)


def groupcreate_view(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        if group_name:
            group, created = models.MuGroup.objects.get_or_create(name=group_name)
            if created:
                # Group created successfully
                # You can perform any additional actions here
                return redirect("usergroups_view_name")  # Redirect to a group list view

    return render(request, "app_base/groupcreate.html")


# //------------------------~ USER LIST ~--------------------------------------------------------------------------
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
    if request.method == "POST":
        user.delete()
        return redirect("muuserlist_view_name")
    return render(request, "app_base/userdelete.html", {"user": user})


# //------------------------~ TRANSACTIONS ~--------------------------------------------------------------------------
@method_decorator(login_required, name="dispatch")
class TransactionList(View):
    template_name = "app_base/transaction_list.html"

    def get(self, request):
        # transactions = Islemler.objects.order_by('-islem_tarihi')  # Order by date in descending order
        transactions = Islemler.objects.filter(islemsahibi=request.user).order_by("-islem_tarihi")
        return render(request, self.template_name, {"transactions": transactions})


@method_decorator(login_required, name="dispatch")
class CreateTransaction(View):
    template_name = "app_base/create_transaction.html"

    def get(self, request):
        form = TransactionForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        print(request.POST)
        form = TransactionForm(request.POST)
        if form.is_valid():
            # print(form)
            transaction = form.save(commit=False)
            transaction.islemsahibi = request.user
            transaction.save()
            form.save_m2m()
            # Update balances here if needed
            return redirect("transaction_list_name")
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class TransactionDetail(View):
    template_name = "app_base/transaction_detail.html"

    def get(self, request, pk):
        transaction = Islemler.objects.get(pk=pk, islemsahibi=request.user)
        return render(request, self.template_name, {"transaction": transaction})


@method_decorator(login_required, name="dispatch")
class UpdateTransaction(View):
    template_name = "app_base/update_transaction.html"

    def get(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        form = TransactionForm(instance=transaction)
        return render(request, self.template_name, {"form": form, "transaction": transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            # Update balances here if needed
            return redirect("transaction_list_name")
        return render(request, self.template_name, {"form": form, "transaction": transaction})


@method_decorator(login_required, name="dispatch")
class DeleteTransaction(View):
    def get(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        return render(request, "app_base/delete_transaction.html", {"transaction": transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        transaction.delete()
        # Update balances here if needed
        return redirect("transaction_list_name")


# //------------------------~ TAGGING ~--------------------------------------------------------------------------
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "app_base/tag_list.html", {"tags": tags})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render(request, "app_base/tag_detail.html", {"tag": tag})


def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect("tag_list_name")
    else:
        form = TagForm()
    return render(request, "app_base/tag_form.html", {"form": form})


def tag_update(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            return redirect("tag_detail_name", slug=tag.slug)
    else:
        form = TagForm(instance=tag)
    return render(request, "app_base/tag_form.html", {"form": form, "tag": tag})


def tag_delete(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        tag.delete()
        return redirect("tag_list_name")
    return render(request, "app_base/tag_confirm_delete.html", {"tag": tag})


# //------------------------~ TRANSACTION TABLE ~--------------------------------------------------------------------------
@method_decorator(login_required, name="dispatch")
class TransactionTable(View):
    template_name = "app_base/transaction_table.html"

    def get(self, request):
        # transactions = Islemler.objects.order_by("-islem_tarihi")  # Order by date in descending order
        transactions = Islemler.objects.prefetch_related("tags").all()

        # transactions = Islemler.objects.prefetch_related("tags").order_by("-islem_tarihi")
        # Debug: Print transactions and their tags to the console

        # for transaction in transactions:
        #     print(f"Transaction: {transaction.islem_ismi}")
        #     for tag in transaction.tags.all():
        #         print(f"  Tag: {tag.name}")
        for obj in Islemler.objects.all():
            print(obj.tags)
        # for transaction in transactions:
        #     print(f"Transaction: {transaction.islem_ismi}")
        #     print(f"Tags: {transaction.tags.all()}")

        return render(request, self.template_name, {"transactions": transactions})


# @method_decorator(login_required, name="dispatch")
# class TransactionTable(View):
#     template_name = "app_base/transaction_table.html"

#     def get(self, request):
#         # Get all transactions
#         transactions = Islemler.objects.all()

#         # Filter by income or expense
#         param_filter = request.GET.get("filter", None)
#         if param_filter == "income":
#             transactions = transactions.filter(kime_gitti__isnull=False)
#         elif param_filter == "expense":
#             transactions = transactions.filter(kimden_geldi__isnull=False)

#         # Filter by tags
#         tag_filter = request.GET.getlist("tags")
#         if tag_filter:
#             # Create a Q object to filter transactions by tags
#             tag_query = Q()
#             for tag_id in tag_filter:
#                 tag_query |= Q(tags__id=tag_id)
#             transactions = transactions.filter(tag_query)

#         # Order by date or amount
#         param_order = request.GET.get("order", None)
#         if param_order == "date":
#             transactions = transactions.order_by("islem_tarihi")
#         elif param_order == "amount":
#             transactions = transactions.order_by("girdiler_TL", "ciktilar_TL")

#         # Get all tags
#         all_tags = Tag.objects.all()  # Replace 'Tag' with your actual tag model name

#         # Pass filtered transactions and all tags to the template
#         return render(request, self.template_name, {"transactions": transactions, "all_tags": all_tags})


# //------------------------~ SPENDINGS CHART ~--------------------------------------------------------------------------


def monthly_spendings(request):
    # Get the selected year and month from the request
    selected_year = int(request.GET.get("year", datetime.date.today().year))
    selected_month = int(request.GET.get("month", datetime.date.today().month))

    # Create a list of month names in Turkish
    month_names_tr = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

    # Generate the range of years from 2023 to 2035
    year_range = list(range(2023, 2036))

    # Create a list of tuples for months with their numbers and names
    months_with_numbers = [(i + 1, month_names_tr[i]) for i in range(len(month_names_tr))]

    # Calculate the first day of the selected month
    first_day_of_month = datetime.date(selected_year, selected_month, 1)

    # Calculate the last day of the selected month
    if selected_month == 12:
        last_day_of_month = datetime.date(selected_year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        last_day_of_month = datetime.date(selected_year, selected_month + 1, 1) - datetime.timedelta(days=1)

    # Retrieve the monthly spendings grouped by tags for the selected month and year
    monthly_spendings = Islemler.objects.filter(islem_tarihi__range=(first_day_of_month, last_day_of_month)).values("tags__name").annotate(total_ciktilar_TL=Sum("ciktilar_TL"), total_ciktilar_Euro=Sum("ciktilar_Euro"), total_ciktilar_Dolar=Sum("ciktilar_Dolar"), total_ciktilar_GBP=Sum("ciktilar_GBP"), total_ciktilar_Sek=Sum("ciktilar_Sek"))

    # Prepare the data for Chart.js
    labels = [entry["tags__name"] for entry in monthly_spendings]
    ciktilar_TL = [entry["total_ciktilar_TL"] for entry in monthly_spendings]
    ciktilar_Euro = [entry["total_ciktilar_Euro"] for entry in monthly_spendings]
    ciktilar_Dolar = [entry["total_ciktilar_Dolar"] for entry in monthly_spendings]
    ciktilar_GBP = [entry["total_ciktilar_GBP"] for entry in monthly_spendings]
    ciktilar_Sek = [entry["total_ciktilar_Sek"] for entry in monthly_spendings]

    context = {
        "labels": labels,
        "ciktilar_TL": ciktilar_TL,
        "ciktilar_Euro": ciktilar_Euro,
        "ciktilar_Dolar": ciktilar_Dolar,
        "ciktilar_GBP": ciktilar_GBP,
        "ciktilar_Sek": ciktilar_Sek,
        "selected_year": selected_year,
        "selected_month": selected_month,
        "month_names_tr": month_names_tr,
        "year_range": year_range,  # Pass the year range to the template
        "months_with_numbers": months_with_numbers,  # Pass the list of months with numbers and names
    }

    return render(request, "app_base/monthly_spendings.html", context)
