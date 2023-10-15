from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import F, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render


from ..models import Currency, Islemler, MuUser


def home_view(request):
    return render(request, template_name="app_base/unsorted/home.html")


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
