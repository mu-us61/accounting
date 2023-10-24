# filters.py
import django_filters
from .models import Islemler, MuUser, Tag, Currency
from django import forms

# from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from django_filters.widgets import DateRangeWidget


class IslemlerFilter(django_filters.FilterSet):
    miktar = django_filters.NumberFilter(
        label="Miktar",
        # method="custom_miktar_filter",
        # widget=django_filters.widgets.RangeWidget(attrs={"class": "custom-class"}),
        # widget=forms.IntegerField(),
    )
    islem_tarihi = django_filters.DateFromToRangeFilter(
        label="Islem Tarihi",
        # widget=django_filters.widgets.RangeWidget(attrs={"class": "custom-class"}),
        widget=DateRangeWidget(
            attrs={
                "placeholder": "Select date range",
                "class": "aaa",
            },
        ),
    )
    kimden_geldi = django_filters.ModelChoiceFilter(
        label="Kimden Geldi",
        queryset=MuUser.objects.all(),
        empty_label="Select an option",
        # widget=django_filters.widgets.LinkWidget(attrs={"class": "custom-class"}),
        widget=forms.Select(attrs={"class": "select22"}),
    )
    kime_gitti = django_filters.ModelChoiceFilter(
        label="Kime Gitti",
        queryset=MuUser.objects.all(),
        empty_label="Select an option",
        widget=forms.Select(attrs={"class": "select22"}),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tags",
        queryset=Tag.objects.all(),
        # widget=django_filters.widgets.FilteredSelectMultiple(attrs={"class": "custom-class"}),
        widget=forms.SelectMultiple(attrs={"class": "select22", "multiple": "multiple"}),
    )
    islem_ismi = django_filters.CharFilter(
        label="Islem Ismi",
        lookup_expr="icontains",
        # widget=django_filters.widgets.TextInput(attrs={"class": "custom-class"}),
        widget=forms.TextInput(attrs={"class": "custom-class"}),
    )
    islemsahibi = django_filters.ModelChoiceFilter(
        label="Islem Sahibi",
        queryset=MuUser.objects.all(),
        empty_label="Select an option",
        widget=forms.Select(attrs={"class": "select22"}),
    )
    currency = django_filters.ModelChoiceFilter(
        label="Currency",
        queryset=Currency.objects.all(),
        empty_label="Select an option",
        widget=forms.Select(attrs={"class": "select22"}),
    )

    class Meta:
        model = Islemler
        fields = ["miktar", "islem_tarihi", "kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islemsahibi", "currency"]


# //------------------------~~--------------------------------------------------------------------------


# class FilterProvenTags(django_filters.FilterSet):
#     year = django_filters.ChoiceFilter(
#         label="Yıl",
#         choices=[
#             (2023, "2023"),
#             (2024, "2024"),
#             (2025, "2025"),
#             (2026, "2026"),
#             (2027, "2027"),
#             (2028, "2028"),
#             (2029, "2029"),
#             (2030, "2030"),
#             (2031, "2031"),
#             (2032, "2032"),
#             (2033, "2033"),
#         ],
#         empty_label="Seçiniz",
#         widget=forms.Select(attrs={"class": "select22"}),
#     )
#     tags = django_filters.ModelMultipleChoiceFilter(
#         label="Tags",
#         queryset=Tag.objects.all(),
#         # widget=django_filters.widgets.FilteredSelectMultiple(attrs={"class": "custom-class"}),
#         widget=forms.SelectMultiple(attrs={"class": "select22", "multiple": "multiple"}),
#     )

import django_filters
from django import forms
from django.db.models import F, DateField
from django.db.models.functions import ExtractYear


class FilterProvenTags(django_filters.FilterSet):
    year = django_filters.NumberFilter(
        label="Yıl",
        field_name="your_date_field_name",  # Replace with the actual name of your date field
        lookup_expr="year",  # Use the 'year' lookup to extract the year from the date field
        empty_label="Seçiniz",
        widget=forms.Select(attrs={"class": "select22"}),
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        label="Tags",
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "select22", "multiple": "multiple"}),
    )
