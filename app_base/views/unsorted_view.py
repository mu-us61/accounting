from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import F, IntegerField, Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from ..models import Currency, Islemler, MuUser, Tag
from django.shortcuts import render
from django_tables2 import RequestConfig
from ..models import MuUser, Currency, DummyModel
from ..tables import UserBalanceTable, TableProvenTags
from ..filters import FilterProvenTags, BalanceFilter
from ..izinler import WritePermissionRequiredMixin, DeletePermissionRequiredMixin
from django.db.models.functions import ExtractMonth


def home_view(request):
    # user = MuUser.objects.get(username="denemeadmin")
    # print(user.MuGroup)  # Check the value of mu_group attribute
    return render(request, template_name="app_base/unsorted/home.html")


# //------------------------~ BALANCE ~--------------------------------------------------------------------------
# @login_required
# def balance_view(request):
#     # Fetch all users
#     users = MuUser.objects.all()

#     # Fetch all unique currencies
#     currencies = Currency.objects.all()

#     # Create a list to store user balances for each currency
#     user_balances = []

#     for user in users:
#         user_balance = {}
#         for currency in currencies:
#             user_balance[currency.name] = user.calculate_currency_balance(currency)
#         user_balances.append((user, user_balance))

#     # Number of users to display per page
#     per_page = 10  # You can adjust this as needed

#     paginator = Paginator(user_balances, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)

#     context = {
#         "page": page,
#         "currencies": currencies,
#     }
#     return render(request, "app_base/unsorted/balance.html", context)


# def balance_view(request):
#     users = MuUser.objects.all()
#     currencies = Currency.objects.all()

#     # Create a list to store user balances for each currency
#     user_balances = []

#     for user in users:
#         user_balance = {"username": user.username}
#         for currency in currencies:
#             user_balance[currency.name] = user.calculate_currency_balance(currency)
#         user_balances.append(user_balance)

#     per_page = 10
#     paginator = Paginator(user_balances, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)

#     # Use the UserBalanceTable to render the table
#     table = UserBalanceTable(user_balances, currencies=currencies)
#     RequestConfig(request, paginate={"per_page": per_page}).configure(table)

#     context = {
#         "table": table,
#         "page": page,
#     }
#     return render(request, "app_base/unsorted/balance.html", context)
from decimal import Decimal


# def balance_view(request):
#     users = MuUser.objects.all()
#     currencies = Currency.objects.all()

#     # Create a list to store user balances for each currency
#     user_balances = []

#     for user in users:
#         user_balance = {"username": user.username}
#         for currency in currencies:
#             balance = user.calculate_currency_balance(currency)
#             # Convert Decimal balance to a string without trailing zeroes
#             trimmed_balance = str(balance).rstrip("0").rstrip(".") if isinstance(balance, Decimal) else balance
#             user_balance[currency.name] = trimmed_balance
#         user_balances.append(user_balance)

#     per_page = 10
#     paginator = Paginator(user_balances, per_page)
#     page_number = request.GET.get("page")
#     page = paginator.get_page(page_number)

#     # Use the UserBalanceTable to render the table
#     table = UserBalanceTable(user_balances, currencies=currencies)
#     RequestConfig(request, paginate={"per_page": per_page}).configure(table)

#     context = {
#         "table": table,
#         "page": page,
#     }
#     return render(request, "app_base/unsorted/balance.html", context)
from django.shortcuts import render
from ..models import MuUser, Islemler, Currency
import django_tables2 as tables


# def balance_view(request):
#     users = MuUser.objects.all()  # Fetch all users
#     currencies = Currency.objects.all()  # Fetch all currencies

#     table_data = []
#     for user in users:
#         user_data = {"username": user.username}
#         for currency in currencies:
#             balance = user.calculate_currency_balance(currency)  # Use the method in MuUser model
#             user_data[currency.abbreviation] = balance  # Include currency abbreviation
#         table_data.append(user_data)

#     table = UserBalanceTable(table_data, currencies=currencies)
#     tables.RequestConfig(request).configure(table)

#     return render(request, "app_base/unsorted/balance.html", {"table": table})


def balance_view(request):
    users = MuUser.objects.all()  # Fetch all users
    currencies = Currency.objects.all()  # Fetch all currencies
    # Apply filtering if request contains filter data
    balance_filter = BalanceFilter(request.GET, queryset=users)

    # Fetch filtered users based on filter criteria
    filtered_users = balance_filter.qs

    table_data = []
    for user in filtered_users:
        user_data = {"username": user.username}
        for currency in currencies:
            balancemoney = user.calculate_currency_balance(currency)
            balance_without_zeros = Decimal(str(balancemoney).rstrip("0").rstrip(".") if "." in str(balancemoney) else str(balancemoney))
            balance = f"{balance_without_zeros} {currency.abbreviation}"
            user_data[currency.abbreviation] = balance  # Include concatenated balance and abbreviation
        table_data.append(user_data)

    table = UserBalanceTable(table_data, currencies=currencies)
    tables.RequestConfig(request).configure(table)

    return render(request, "app_base/unsorted/balance.html", {"table": table, "balance_filter": balance_filter})


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
        islemler_type="giden",
    )

    # Calculate the sum of the selected currency field
    currency_sum = islemler.aggregate(Sum("miktar"))["miktar__sum"] or 0

    # Get tag data for the selected month and currency
    tag_data = islemler.values("tags__name").annotate(miktar=Coalesce(Sum("miktar"), Value(0), output_field=IntegerField())).order_by("-miktar")

    # Serialize tag_data to JSON
    tag_data_json = json.dumps(list(tag_data))

    context = {
        "tag_data": tag_data,
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


# //------------------------~ Proven-Tags ~--------------------------------------------------------------------------
from collections import defaultdict

from decimal import Decimal


# def proventags_view(request):
#     if request.method == "GET":
#         data_ay = [
#             {"aylar": "Ocak"},
#             {"aylar": "Şubat"},
#             {"aylar": "Mart"},
#             {"aylar": "Nisan"},
#             {"aylar": "Mayıs"},
#             {"aylar": "Haziran"},
#             {"aylar": "Temmuz"},
#             {"aylar": "Ağustos"},
#             {"aylar": "Eylül"},
#             {"aylar": "Ekim"},
#             {"aylar": "Kasım"},
#             {"aylar": "Aralik"},
#         ]
#         table = TableProvenTags(data_ay)
#         all_tags = Islemler.objects.values_list("tags__name", flat=True).distinct()
#         # all_tags = Islemler.objects.unique_values('tags')
#         year = request.GET.get("year")
#         tags = request.GET.getlist("tags")
#         # filtered_data = Islemler.objects.filter(Q(year=year) & Q(tags__name__in=tags))
#         filtered_data = Islemler.objects.filter(Q(islem_tarihi__year=year) & Q(tags__name__in=tags))

#         monthly_data = defaultdict(lambda: {"total": 0, "with_documents": 0})

#         for data in filtered_data:
#             month = data.islem_tarihi.month
#             monthly_data[month]["total"] += 1
#             if data.islemler_picture or data.islemler_pdf:
#                 monthly_data[month]["with_documents"] += 1

#         table_data = []

#         for month_num in range(1, 13):
#             month_name = {
#                 1: "Ocak",
#                 2: "Şubat",
#                 3: "Mart",
#                 4: "Nisan",
#                 5: "Mayıs",
#                 6: "Haziran",
#                 7: "Temmuz",
#                 8: "Ağustos",
#                 9: "Eylül",
#                 10: "Ekim",
#                 11: "Kasım",
#                 12: "Aralık",
#             }[month_num]
#             total = monthly_data[month_num]["total"]
#             with_documents = monthly_data[month_num]["with_documents"]
#             percentage = (decimal.Decimal(with_documents) / decimal.Decimal(total)) * 100 if total > 0 else 0

#             table_data.append(
#                 {
#                     "aylar": month_name,
#                     "toplam": total,
#                     "belgeli": with_documents,
#                     "yuzdesi": percentage,
#                 }
#             )

#         # print("year", year, "  " "tags", tags)
#     else:
#         pass

#     context = {
#         "all_tags": all_tags,
#         "year": year,
#         "tags": tags,
#         "filtered_data": filtered_data,
#         "table": table,
#     }

#     print(all_tags)

#     return render(request, template_name="app_base/unsorted/proven_tags.html", context=context)


# def proventags_view(request):
#     table_data = []  # Create an empty list to store table data
#     currency_id = request.GET.get("currency")  # Get currency ID from request

#     if request.method == "GET":
#         all_tags = Islemler.objects.values_list("tags__name", flat=True).distinct()
#         # all_tags = Islemler.objects.unique_values('tags')
#         year = request.GET.get("year")
#         tags = request.GET.getlist("tags")
#         currency = Currency.objects.get(id=currency_id) if currency_id else None  # Get Currency object
#         # filtered_data = Islemler.objects.filter(Q(year=year) & Q(tags__name__in=tags))
#         filtered_data = Islemler.objects.filter(Q(islem_tarihi__year=year) & Q(tags__name__in=tags) & Q(islemler_type="giden") & Q(currency=currency) if currency else Q())
#         # Your existing code to get year and tags...
#         # ... your existing code ...

#         # Calculate the data
#         monthly_data = defaultdict(lambda: {"total": 0, "with_documents": 0, "toplamgelen": 0, "toplamgiden": 0, "ispatlilar": 0})

#         for data in filtered_data:
#             month = data.islem_tarihi.month
#             monthly_data[month]["total"] += 1
#             if data.islemler_picture or data.islemler_pdf:
#                 monthly_data[month]["with_documents"] += 1

#         for month_num in range(1, 13):
#             month_name = {
#                 1: "Ocak",
#                 2: "Şubat",
#                 3: "Mart",
#                 4: "Nisan",
#                 5: "Mayıs",
#                 6: "Haziran",
#                 7: "Temmuz",
#                 8: "Ağustos",
#                 9: "Eylül",
#                 10: "Ekim",
#                 11: "Kasım",
#                 12: "Aralık",
#             }[month_num]
#             total = monthly_data[month_num]["total"]
#             with_documents = monthly_data[month_num]["with_documents"]
#             percentage = int((Decimal(with_documents) / Decimal(total)) * 100 if total > 0 else 0)
#             # toplamgelen =
#             # toplamgiden
#             # ispatlilar

#             table_data.append(
#                 {
#                     "aylar": month_name,
#                     "toplam": total,
#                     "belgeli": with_documents,
#                     "yuzdesi": percentage,
#                     # "toplamgelen": toplamgelen,
#                     # "toplamgiden": toplamgiden,
#                     # "ispatlilar": ispatlilar,
#                 }
#             )

#     table = TableProvenTags(table_data)  # Create a table instance and pass data

#     context = {
#         "all_tags": all_tags,
#         "year": year,
#         "tags": tags,
#         "filtered_data": filtered_data,
#         "table": table,
#     }

#     return render(request, template_name="app_base/unsorted/proven_tags.html", context=context)


# from collections import defaultdict
# from decimal import Decimal
# from django.db.models import Sum, F

# def proventags_view(request):
#     table_data = []  # Create an empty list to store table data
#     currency_id = request.GET.get("currency")  # Get currency ID from request

#     if request.method == "GET":
#         all_tags = Islemler.objects.values_list("tags__name", flat=True).distinct()
#         year = request.GET.get("year")
#         tags = request.GET.getlist("tags")
#         currency = Currency.objects.get(id=currency_id) if currency_id else None  # Get Currency object

#         filtered_data = Islemler.objects.filter(
#             Q(islem_tarihi__year=year) &
#             Q(tags__name__in=tags) &
#             Q(islemler_type="giden" if currency else "gelen") &
#             Q(currency=currency) if currency else Q()
#         )

#         monthly_data = defaultdict(lambda: {"total": 0, "with_documents": 0, "toplamgelen": Decimal(0), "toplamgiden": Decimal(0)})

#         for data in filtered_data:
#             month = data.islem_tarihi.month
#             monthly_data[month]["total"] += 1
#             if data.islemler_type == "gelen":
#                 monthly_data[month]["toplamgelen"] += data.miktar
#             elif data.islemler_type == "giden":
#                 monthly_data[month]["toplamgiden"] += data.miktar
#                 if data.islemler_picture or data.islemler_pdf:
#                     monthly_data[month]["with_documents"] += 1

#         for month_num in range(1, 13):
#             total = monthly_data[month_num]["total"]
#             with_documents = monthly_data[month_num]["with_documents"]
#             toplamgelen = monthly_data[month_num]["toplamgelen"]
#             toplamgiden = monthly_data[month_num]["toplamgiden"]

#             # Calculate ispatlilar percentage
#             ispatlilar = 0 if toplamgiden == 0 else (with_documents / total) * 100 if total > 0 else 0

#             table_data.append(
#                 {
#                     "aylar": {
#                         1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
#                         7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık",
#                     }[month_num],
#                     "toplam": total,
#                     "belgeli": with_documents,
#                     "yuzdesi": int((Decimal(with_documents) / Decimal(total)) * 100) if total > 0 else 0,
#                     "toplamgelen": toplamgelen,
#                     "toplamgiden": toplamgiden,
#                     "ispatlilar": ispatlilar,
#                 }
#             )

#     table = TableProvenTags(table_data)  # Create a table instance and pass data

#     context = {
#         "all_tags": all_tags,
#         "year": year,
#         "tags": tags,
#         "currency_id": currency_id,
#         "filtered_data": filtered_data,
#         "table": table,
#     }

#     return render(request, template_name="app_base/unsorted/proven_tags.html", context=context)


# //------------------------~ EXEL USERS ~--------------------------------------------------------------------------

# # myapp/views.py
# from django.shortcuts import render
# from import_export.formats import base_formats
# from ..resources import ExelUsersResource


# def upload_excel_view(request):
#     if request.method == "POST" and request.FILES["file"]:
#         excel_file = request.FILES["file"]

#         # Determine the file format (Excel, CSV, etc.)
#         file_format = base_formats.XLS()

#         dataset = ExelUsersResource().import_data(dataset=excel_file.read(), format=file_format)

#         if dataset.has_errors():
#             # Handle errors here if needed
#             pass
#         else:
#             dataset.save()

#     return render(request, "app_base/unsorted/uploadexel.html")

# from django.shortcuts import render, redirect
# from import_export.formats import base_formats
# from ..resources import ExelUsersResource


# def upload_excel_view(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         excel_file = request.FILES["file"]

#         # Determine the file format (Excel, CSV, etc.)
#         file_format = base_formats.XLS()

#         dataset = ExelUsersResource().import_data(excel_file, format=file_format)

#         if dataset.has_errors():
#             # Handle errors here if needed
#             pass
#         else:
#             dataset.import_data()
#             return redirect("home_view_name")  # Redirect to a success page or another URL

#     return render(request, "app_base/unsorted/uploadexel.html")


from tablib import Dataset
from ..resources import ExelUsersResource


@WritePermissionRequiredMixin()
def upload_excel_view(request):
    if request.method == "POST":
        person_resource = ExelUsersResource()
        dataset = Dataset()
        new_persons = request.FILES["myfile"]

        imported_data = dataset.load(new_persons.read())
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, "app_base/unsorted/uploadexel.html")


# //------------------------~~--------------------------------------------------------------------------


def mobile_view(request):
    return render(request, template_name="app_base/unsorted/mobile.html")


from django.http import HttpResponse
from django.conf import settings
import os


def downloadmobile(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            response = HttpResponse(file.read(), content_type="application/vnd.android.package-archive")
            response["Content-Disposition"] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        return HttpResponse("File not found", status=404)


# def

from django.shortcuts import render
import django_filters
from ..models import Islemler
from ..filters import HarcamalarFilter  # Import your defined filter


def proventags_view(request):
    filter = HarcamalarFilter(request.GET, queryset=Islemler.objects.all())
    table_data = []
    if request.method == "GET":
        year = request.GET.get("year")
        tag_ids = request.GET.getlist("tags")
        currency_id = request.GET.get("currency")
        # print(year, tag_ids, currency_id)
        # filtered_data = Islemler.objects.filter(Q(islem_tarihi__year=year) & Q(tags__name__in=tags) & Q(islemler_type="giden") & Q(currency=currency))
        # filtered_data = Islemler.objects.all()
        filtered_data = Islemler.objects.filter(islemler_type="giden")

        if year:
            # Convert year to integer if not None
            year = int(year)
            # Filter by year
            filtered_data = filtered_data.filter(islem_tarihi__year=year)
            # print(f"Filtered by year {year}: {filtered_data}")

        if tag_ids:
            # Filter by tag_ids (assuming tag_ids are primary keys)
            filtered_data = filtered_data.filter(tags__id__in=tag_ids)
            # print(f"Filtered by tag_ids {tag_ids}: {filtered_data}")

        if currency_id:
            # Filter by currency_id (assuming currency_id is the primary key)
            filtered_data = filtered_data.filter(currency_id=currency_id)
        # print("aaaaaaaaaaaaa")
        # print(filtered_data)
        monthly_data = defaultdict(lambda: {"total": 0, "with_documents": 0})

        for data in filtered_data:
            month = data.islem_tarihi.month
            monthly_data[month]["total"] += 1
            if data.islemler_picture or data.islemler_pdf:
                monthly_data[month]["with_documents"] += 1

        for month_num in range(1, 13):
            month_name = {
                1: "Ocak",
                2: "Şubat",
                3: "Mart",
                4: "Nisan",
                5: "Mayıs",
                6: "Haziran",
                7: "Temmuz",
                8: "Ağustos",
                9: "Eylül",
                10: "Ekim",
                11: "Kasım",
                12: "Aralık",
            }[month_num]
            total = monthly_data[month_num]["total"]
            with_documents = monthly_data[month_num]["with_documents"]
            percentage = int((Decimal(with_documents) / Decimal(total)) * 100 if total > 0 else 0)
            # Calculate the total income (toplam_gelen) for "gelen" transactions in each month
            total_income_for_month = Islemler.objects.filter(islem_tarihi__month=month_num, islem_tarihi__year=year, islemler_type="gelen").aggregate(total_gelen=Sum("miktar"))["total_gelen"] or 0
            # Calculate the total outcome (toplam_giden) for "giden" transactions in each month
            total_outcome_for_month = Islemler.objects.filter(islem_tarihi__month=month_num, islem_tarihi__year=year, islemler_type="giden").aggregate(total_giden=Sum("miktar"))["total_giden"] or 0
            # total_ispatlilar = Islemler.objects.filter(islem_tarihi__month=month_num, islem_tarihi__year=year, islemler_type="giden", is has islemler_pdf or islemler_picture).aggregate(total_giden=Sum("miktar"))["total_giden"] or 0
            # Calculate the total for transactions with either islemler_pdf or islemler_picture
            total_ispatlilar = (
                Islemler.objects.filter(
                    islem_tarihi__month=month_num,
                    islem_tarihi__year=year,
                    islemler_type="giden",
                )
                # .filter(Q(islemler_picture__isnull=False) | Q(islemler_pdf__isnull=False))
                .filter((Q(islemler_picture__isnull=False) & ~Q(islemler_picture__exact="")) | (Q(islemler_pdf__isnull=False) & ~Q(islemler_pdf__exact=""))).aggregate(total_ispatlilar=Sum("miktar"))["total_ispatlilar"]
                or 0
            )
            # print(total_ispatlilar)
            # query_set = Islemler.objects.filter(
            #     islem_tarihi__month=month_num,
            #     islem_tarihi__year=year,
            #     islemler_type="giden",
            # ).filter(Q(islemler_picture__isnull=False) | Q(islemler_pdf__isnull=False))

            # print(query_set.query)
            percentage_of_ispatlilar = int((Decimal(total_ispatlilar) / Decimal(total_outcome_for_month)) * 100 if total_outcome_for_month > 0 else 0)

            table_data.append(
                {
                    "aylar": month_name,
                    "toplam": total,
                    "belgeli": with_documents,
                    "yuzdesi": percentage,
                    "toplam_gelen": total_income_for_month,  # Total income for "gelen" transactions
                    "toplam_giden": total_outcome_for_month,  # Total outcome for "giden" transactions
                    "ispatlilar": percentage_of_ispatlilar,  # Total for transactions with islemler_pdf or islemler_picture
                }
            )
    table = TableProvenTags(table_data)  # Create a table instance and pass data

    context = {
        "filter": filter,
        "filtered_data": filtered_data,
        "table": table,
    }

    return render(request, template_name="app_base/unsorted/proven_tags.html", context=context)
