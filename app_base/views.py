import json
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from . import models
from .forms import CurrencyForm, MuUserForm, TagForm, TransactionFilterForm, TransactionForm
from .models import Currency, Islemler, MuGroup, MuUser, Tag
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import TransactionForm
from .models import Islemler
from django.core.paginator import Paginator


def is_staff(user):
    return user.is_staff


# //------------------------~ ANASAYFA ~--------------------------------------------------------------------------
def home_view(request):
    return render(request, template_name="app_base/home.html")


# //------------------------~ BAKIYE ~--------------------------------------------------------------------------


@login_required
def bakiye_view(request):
    # Fetch all users
    users = MuUser.objects.all()

    # Fetch all unique currencies
    currencies = Currency.objects.all()

    # Create a list to store user balances for each currency
    user_balances = []

    for user in users:
        user_balance = {}
        for currency in currencies:
            user_balance[currency.name] = user.calculate_currency_balance(currency)
        user_balances.append((user, user_balance))

    # Number of users to display per page
    per_page = 1  # You can adjust this as needed

    paginator = Paginator(user_balances, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "currencies": currencies,
    }
    return render(request, "app_base/bakiye.html", context)


# @login_required
# def bakiye_view(request):
#     # Fetch all users
#     users = MuUser.objects.all()

#     # Fetch all unique currencies
#     currencies = Currency.objects.all()

#     # Create a dictionary to store user balances for each currency
#     user_balances = {}

#     for user in users:
#         user_balance = {}
#         for currency in currencies:
#             user_balance[currency.name] = user.calculate_currency_balance(currency)
#         user_balances[user] = user_balance

#     context = {
#         "user_balances": user_balances,
#         "currencies": currencies,
#     }
#     return render(request, "app_base/bakiye.html", context)


# //------------------------~ AUTHENTICATIONS ~--------------------------------------------------------------------------
@login_required
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
            return render(request, template_name="app_base/authentications/change_password.html")

    if request.method == "GET":
        return render(request, template_name="app_base/authentications/change_password.html")


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


# //------------------------~ USER GROUPS ~--------------------------------------------------------------------------
# @login_required
# def usergroups_view(request):
#     groups = models.MuGroup.objects.all()
#     return render(request, "app_base/groups/grouppage.html", {"groups": groups})
@login_required
def usergroups_view(request):
    groups = models.MuGroup.objects.all()

    # Number of groups to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(groups, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/groups/grouppage.html", {"page": page})


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
@user_passes_test(is_staff)
def groupcreate_view(request):
    if request.method == "POST":
        group_name = request.POST.get("group_name")
        if group_name:
            group, created = models.MuGroup.objects.get_or_create(name=group_name)
            if created:
                # Group created successfully
                # You can perform any additional actions here
                return redirect("usergroups_view_name")  # Redirect to a group list view

    return render(request, "app_base/groups/groupcreate.html")


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
            return redirect("usergroups_view_name")  # Redirect to a group list view

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


# //------------------------~ ACCOUNTS ~--------------------------------------------------------------------------
# @login_required
# def muuserlist_view(request):
#     users = models.MuUser.objects.all()
#     return render(request, "app_base/accounts/userlist.html", {"users": users})


@login_required
def muuserlist_view(request):
    users = models.MuUser.objects.all()

    # Number of users to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(users, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/accounts/userlist.html", {"page": page})


@login_required
@user_passes_test(is_staff)
def muusercreate_view(request):
    if request.method == "POST":
        form = MuUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("muuserlist_view_name")
    else:
        form = MuUserForm()

    return render(request, "app_base/accounts/usercreate.html", {"form": form})


@login_required
@user_passes_test(is_staff)
def muuserupdate_view(request, pk):
    user = get_object_or_404(models.MuUser, pk=pk)
    if request.method == "POST":
        form = MuUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("muuserlist_view_name")
    else:
        form = MuUserForm(instance=user)
    return render(request, "app_base/accounts/userupdate.html", {"form": form, "user": user})


@login_required
@user_passes_test(is_staff)
def muuserdelete_view(request, pk):
    user = get_object_or_404(models.MuUser, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("muuserlist_view_name")
    return render(request, "app_base/accounts/userdelete.html", {"user": user})


# //------------------------~ TRANSACTIONS ~--------------------------------------------------------------------------
# @method_decorator(login_required, name="dispatch")
class TransactionList(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_list.html"

    def get(self, request):
        # transactions = Islemler.objects.order_by('-islem_tarihi')  # Order by date in descending order
        transactions = Islemler.objects.filter(islemsahibi=request.user).order_by("-islem_tarihi")
        return render(request, self.template_name, {"transactions": transactions})


#! TODO burda bir sorun var


# @method_decorator(login_required, name="dispatch")
class CreateTransaction(LoginRequiredMixin, View):
    template_name = "app_base/transactions/create_transaction.html"

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


# @method_decorator(login_required, name="dispatch")
class TransactionDetail(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_detail.html"

    def get(self, request, pk):
        transaction = Islemler.objects.get(pk=pk, islemsahibi=request.user)
        return render(request, self.template_name, {"transaction": transaction})


def is_owner_or_admin(user, transaction):
    return user == transaction.islemsahibi or user.is_staff


class UpdateTransaction(LoginRequiredMixin, View):
    template_name = "app_base/transactions/update_transaction.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.transaction = get_object_or_404(Islemler, pk=kwargs["pk"])
        # Apply the user_passes_test decorator here
        if not is_owner_or_admin(request.user, self.transaction):
            return redirect("permission_denied_page_name")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TransactionForm(instance=self.transaction)
        return render(request, self.template_name, {"form": form, "transaction": self.transaction})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST, instance=self.transaction)
        if form.is_valid():
            form.save()
            # Update balances here if needed
            return redirect("transaction_list_name")
        return render(request, self.template_name, {"form": form, "transaction": self.transaction})


# @method_decorator(login_required, name="dispatch")
class DeleteTransaction(LoginRequiredMixin, View):
    def get(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        return render(request, "app_base/transactions/delete_transaction.html", {"transaction": transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        transaction.delete()
        # Update balances here if needed
        return redirect("transaction_list_name")


# //------------------------~ TAGS ~--------------------------------------------------------------------------
# @login_required
# def tag_list(request):
#     tags = Tag.objects.all()
#     return render(request, "app_base/tags/tag_list.html", {"tags": tags})


@login_required
def tag_list(request):
    tags = Tag.objects.all()

    # Number of tags to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(tags, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }
    return render(request, "app_base/tags/tag_list.html", context)


@login_required
def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render(request, "app_base/tags/tag_detail.html", {"tag": tag})


@login_required
def tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect("tag_list_name")
    else:
        form = TagForm()
    return render(request, "app_base/tags/tag_form.html", {"form": form})


@login_required
def tag_update(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            return redirect("tag_detail_name", slug=tag.slug)
    else:
        form = TagForm(instance=tag)
    return render(request, "app_base/tags/tag_form.html", {"form": form, "tag": tag})


@login_required
def tag_delete(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        tag.delete()
        return redirect("tag_list_name")
    return render(request, "app_base/tags/tag_confirm_delete.html", {"tag": tag})


# //------------------------~ TRANSACTION TABLE ~--------------------------------------------------------------------------


class TransactionTable(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_table.html"

    def get(self, request):
        # Initialize default values
        default_start_date = datetime.now() - timedelta(days=30)
        default_end_date = datetime.now()

        # Format default values in Turkish date format
        default_start_date_str = default_start_date.strftime("%d/%m/%Y")
        default_end_date_str = default_end_date.strftime("%d/%m/%Y")

        filter_form = TransactionFilterForm(request.GET)
        transactions = Islemler.objects.all().order_by("-islem_tarihi").prefetch_related("tags")

        if filter_form.is_valid():
            user = filter_form.cleaned_data.get("user")
            currency = filter_form.cleaned_data.get("currency")
            tags = filter_form.cleaned_data.get("tags")
            kimden_geldi = filter_form.cleaned_data.get("kimden_geldi")
            kime_gitti = filter_form.cleaned_data.get("kime_gitti")
            start_date = filter_form.cleaned_data.get("start_date")
            end_date = filter_form.cleaned_data.get("end_date")
            today = filter_form.cleaned_data.get("today")

            if user:
                transactions = transactions.filter(islemsahibi=user)
            if currency:
                transactions = transactions.filter(currency=currency)
            if tags:
                transactions = transactions.filter(tags__in=tags)
            if kimden_geldi:
                transactions = transactions.filter(kimden_geldi=kimden_geldi)
            if kime_gitti:
                transactions = transactions.filter(kime_gitti=kime_gitti)

            if start_date and end_date:
                # Adjust the end date by one day to include transactions on the end date
                end_date += timedelta(days=1)
                query = Q(islem_tarihi__range=(start_date, end_date))
                if today:
                    now = datetime.now()
                    today_query = Q(islem_tarihi__date=now.date())
                    transactions = transactions.filter(query | today_query)
                else:
                    transactions = transactions.filter(query)
            elif today:
                now = datetime.now()
                transactions = transactions.filter(islem_tarihi__date=now.date())

        all_tags = Tag.objects.all()
        years = range(datetime.now().year, 2000, -1)
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        days = [str(day).zfill(2) for day in range(1, 32)]
        # today = date.today()  "today": today,
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        return render(
            request,
            self.template_name,
            {
                "start_date": request.GET.get("start_date", default_start_date_str),
                "end_date": request.GET.get("end_date", default_end_date_str),
                "transactions": transactions,
                "all_tags": all_tags,
                "filter_form": filter_form,
                "years": years,
                "months": months,
                "days": days,
            },
        )


# //------------------------~ SPENDINGS CHART ~--------------------------------------------------------------------------


@login_required
def monthly_spendings(request):
    # Generate a list of years up to 2035
    years = list(range(2023, 2036))

    # Create a dictionary to map month numbers to Turkish month names
    months = {
        1: _("Ocak"),
        2: _("Şubat"),
        3: _("Mart"),
        4: _("Nisan"),
        5: _("Mayıs"),
        6: _("Haziran"),
        7: _("Temmuz"),
        8: _("Ağustos"),
        9: _("Eylül"),
        10: _("Ekim"),
        11: _("Kasım"),
        12: _("Aralık"),
    }

    # Get the current year and month for default values
    # current_date = datetime.date.today()
    current_date = datetime.today().date()

    current_year = current_date.year
    current_month = current_date.month

    # Get the list of currencies for the currency select field
    currencies = Currency.objects.all()

    selected_year = int(request.POST.get("year", current_year)) if request.method == "POST" else current_year
    selected_month = int(request.POST.get("month", current_month)) if request.method == "POST" else current_month
    selected_currency = request.POST.get("currency", "TL") if request.method == "POST" else "TL"

    # Filter Islemler based on selected year, month, currency, and tag
    islemler = Islemler.objects.filter(
        islem_tarihi__year=selected_year,
        islem_tarihi__month=selected_month,
        currency__abbreviation=selected_currency,
    )

    # Calculate the sum of the selected currency field
    currency_sum = islemler.aggregate(Sum("miktar"))["miktar__sum"] or 0

    # Get tag data for the selected month and currency
    tag_data = islemler.values("tags__name").annotate(miktar=Coalesce(Sum("miktar"), Value(0), output_field=IntegerField())).order_by("-miktar")

    # Serialize tag_data to JSON
    tag_data_json = json.dumps(list(tag_data))

    context = {
        "years": years,
        "months": months,
        "currencies": currencies,
        "selected_year": selected_year,
        "selected_month": selected_month,
        "selected_currency": selected_currency,
        "currency_sum": currency_sum,
        "tag_data_json": tag_data_json,
    }
    return render(request, "app_base/monthly_spendings.html", context)


# //------------------------~~--------------------------------------------------------------------------


class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = "app_base/currency_list.html"
    context_object_name = "currencies"


class CurrencyCreateView(LoginRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currency_form.html"
    success_url = reverse_lazy("currency_list")


class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currency_form.html"
    success_url = reverse_lazy("currency_list")


class CurrencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Currency
    template_name = "app_base/currency_confirm_delete.html"
    success_url = reverse_lazy("currency_list")
