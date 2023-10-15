import json
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from . import models
from .filters import IslemlerFilter
from .forms import CurrencyForm, MuUserForm, TagForm, TransactionFilterForm, TransactionForm
from .models import Currency, Islemler, MuGroup, MuUser, Tag
from .tables import IslemlerTable


# //------------------------~~--------------------------------------------------------------------------
def is_staff(user):
    return user.is_staff


# //------------------------~ ANASAYFA ~--------------------------------------------------------------------------
def home_view(request):
    return render(request, template_name="app_base/unsorted/home.html")


# //------------------------~ AUTHENTICATIONS ~--------------------------------------------------------------------------
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
            u = models.MuUser.objects.get(username=request.user.username)
            u.set_password(request.POST.get("password1"))
            u.save()
            logout(request)
            return redirect("home_view_name")
        else:
            messages.error(request, "Tekrar deneyiniz")
            return render(request, template_name="app_base/authentications/passwordchange.html")

    if request.method == "GET":
        return render(request, template_name="app_base/authentications/passwordchange.html")


# //------------------------~ BALANCE ~--------------------------------------------------------------------------
@login_required
def balance_view(request):
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
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(user_balances, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "currencies": currencies,
    }
    return render(request, "app_base/unsorted/balance.html", context)


# //------------------------~ GROUP ~--------------------------------------------------------------------------
@login_required
def grouplist_view(request):
    groups = models.MuGroup.objects.all()
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
            group, created = models.MuGroup.objects.get_or_create(name=group_name)
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


# //------------------------~ USER ~--------------------------------------------------------------------------
@login_required
def userlist_view(request):
    users = models.MuUser.objects.all()

    # Number of users to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(users, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "app_base/users/userlist.html", {"page": page})


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
    user = get_object_or_404(models.MuUser, pk=pk)
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
    user = get_object_or_404(models.MuUser, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("userlist_view_name")
    return render(request, "app_base/users/userdelete.html", {"user": user})


# //------------------------~ TRANSACTIONS ~--------------------------------------------------------------------------
class TransactionListView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_list.html"
    items_per_page = 10  # You can change the number of items per page as needed

    def get(self, request):
        transactions = Islemler.objects.filter(islemsahibi=request.user).order_by("-islem_tarihi")

        # Create a Paginator instance
        paginator = Paginator(transactions, self.items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get("page")

        # Get the transactions for the current page
        transactions = paginator.get_page(page)

        return render(request, self.template_name, {"transactions": transactions})


# @method_decorator(login_required, name="dispatch")
class TransactionCreateView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_create.html"

    def get(self, request):
        form = TransactionForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # print(request.POST)
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
class TransactionDetailView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_detail.html"

    def get(self, request, pk):
        transaction = Islemler.objects.get(pk=pk, islemsahibi=request.user)
        return render(request, self.template_name, {"transaction": transaction})


def is_owner_or_admin(user, transaction):
    return user == transaction.islemsahibi or user.is_staff


class TransactionUpdateView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_update.html"

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
class TransactionDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        return render(request, "app_base/transactions/transaction_delete.html", {"transaction": transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Islemler, pk=pk, islemsahibi=request.user)
        transaction.delete()
        # Update balances here if needed
        return redirect("transaction_list_name")


# //------------------------~TRANSACTION BIG TABLE~--------------------------------------------------------------------------


class TransactionTableView(SingleTableMixin, FilterView):
    table_class = IslemlerTable
    model = Islemler
    template_name = "app_base/transactions/transaction_big_table.html"
    filterset_class = IslemlerFilter

    # def get(self, request, *args, **kwargs):
    #     # Log information to the console using print()
    #     print("Request:", dir(request.GET))
    #     # You can print other information as needed

    #     # Call the super class's get method to continue the view execution
    #     return super().get(request, *args, **kwargs)


# //------------------------~ TAGS ~--------------------------------------------------------------------------
@login_required
def taglist_view(request):
    tags = Tag.objects.all()

    # Number of tags to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(tags, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }
    return render(request, "app_base/tags/taglist.html", context)


@login_required
def tagdetail_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render(request, "app_base/tags/tagdetail.html", {"tag": tag})


@login_required
def tagcreate_view(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect("taglist_view_name")
    else:
        form = TagForm()
    return render(request, "app_base/tags/tagform.html", {"form": form})


@login_required
def tagupdate_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            return redirect("tagdetail_view_name", slug=tag.slug)
    else:
        form = TagForm(instance=tag)
    return render(request, "app_base/tags/tagform.html", {"form": form, "tag": tag})


@login_required
def tagdelete_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        tag.delete()
        return redirect("taglist_view_name")
    return render(request, "app_base/tags/tagconfirm_delete.html", {"tag": tag})


# //------------------------~ TRANSACTION TABLE ~--------------------------------------------------------------------------


class TransactionTableView(LoginRequiredMixin, View):
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

        # Apply pagination to your transactions
        page_number = request.GET.get("page")
        per_page = 10  # You can adjust this as needed
        paginator = Paginator(transactions, per_page)
        page = paginator.get_page(page_number)

        context = {
            "start_date": request.GET.get("start_date", default_start_date_str),
            "end_date": request.GET.get("end_date", default_end_date_str),
            "transactions": page,
            "all_tags": all_tags,
            "filter_form": filter_form,
            "years": years,
            "months": months,
            "days": days,
        }

        return render(request, self.template_name, context)


# //------------------------~ MONTHLY SPENDINGS CHART ~--------------------------------------------------------------------------


@login_required
def monthlyspendings_view(request):
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
    return render(request, "app_base/unsorted/monthly_spendings.html", context)


# //------------------------~ CURRENCY ~--------------------------------------------------------------------------


class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = "app_base/currencies/currencylist.html"
    context_object_name = "currencies"


class CurrencyCreateView(LoginRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currencies/currencyform.html"
    success_url = reverse_lazy("currencylist_view_name")


class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currencies/currencyform.html"
    success_url = reverse_lazy("currencylist_view_name")


class CurrencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Currency
    template_name = "app_base/currencies/currencyconfirm_delete.html"
    success_url = reverse_lazy("currencylist_view_name")
