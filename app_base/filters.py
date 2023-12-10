# filters.py
import django_filters
from .models import Islemler, MuUser, Tag, Currency, ExelUsers, EvrakModel, EVRAK_TYPE_CHOICES, EtkinlikModel
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
    exelusers = django_filters.ModelMultipleChoiceFilter(
        label="Exel Kullanicilari",
        queryset=ExelUsers.objects.all(),
        # widget=django_filters.widgets.FilteredSelectMultiple(attrs={"class": "custom-class"}),
        widget=forms.SelectMultiple(attrs={"class": "select22", "multiple": "multiple"}),
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
        fields = ["miktar", "islem_tarihi", "kimden_geldi", "kime_gitti", "exelusers", "tags", "islem_ismi", "islemsahibi", "currency"]


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


# //------------------------~~--------------------------------------------------------------------------
class EvrakModelFilter(django_filters.FilterSet):
    evrak_last_updated = django_filters.DateFromToRangeFilter(
        label="Son Degistirilme Tarihi",
        # widget=django_filters.widgets.RangeWidget(attrs={"class": "custom-class"}),
        widget=DateRangeWidget(
            attrs={
                "placeholder": "Select date range",
                "class": "aaa",
            },
        ),
    )

    evrak_owner = django_filters.ModelChoiceFilter(
        label="Girdiyi Olusturan",
        queryset=MuUser.objects.all(),
        empty_label="Select an option",
        widget=forms.Select(attrs={"class": "select22"}),
    )

    evrak_name = django_filters.CharFilter(
        label="Evrak Ismi",
        lookup_expr="icontains",
        # widget=django_filters.widgets.TextInput(attrs={"class": "custom-class"}),
        widget=forms.TextInput(attrs={"class": "custom-class"}),
    )

    evrak_tags = django_filters.ModelMultipleChoiceFilter(
        label="Harcama Kalemleri",
        queryset=Tag.objects.all(),
        # widget=django_filters.widgets.FilteredSelectMultiple(attrs={"class": "custom-class"}),
        widget=forms.SelectMultiple(attrs={"class": "select22", "multiple": "multiple"}),
    )

    evrak_type = django_filters.ChoiceFilter(
        field_name="evrak_type",
        label="Evrak Type",
        choices=EVRAK_TYPE_CHOICES,
        empty_label="Select an option",
        widget=forms.Select(attrs={"class": "select22"}),
    )

    class Meta:
        model = EvrakModel
        fields = ["evrak_last_updated", "evrak_owner", "evrak_name", "evrak_tags", "evrak_type"]


# //------------------------~~--------------------------------------------------------------------------


class EtkinlikModelFilter(django_filters.FilterSet):
    etkinlik_last_updated = django_filters.DateFromToRangeFilter(
        label="Son Degistirilme Tarihi",
        # widget=django_filters.widgets.RangeWidget(attrs={"class": "custom-class"}),
        widget=DateRangeWidget(
            attrs={
                "placeholder": "Select date range",
                "class": "aaa",
            },
        ),
    )

    etkinlik_owner = django_filters.ModelChoiceFilter(
        label="Girdiyi Olusturan",
        queryset=MuUser.objects.all(),
        empty_label="Select an option",
        widget=forms.Select(attrs={"class": "select22"}),
    )

    etkinlik_name = django_filters.CharFilter(
        label="Etkinlik Ismi",
        lookup_expr="icontains",
        # widget=django_filters.widgets.TextInput(attrs={"class": "custom-class"}),
        widget=forms.TextInput(attrs={"class": "custom-class"}),
    )

    etkinlik_tags = django_filters.ModelMultipleChoiceFilter(
        label="Harcama Kalemleri",
        queryset=Tag.objects.all(),
        # widget=django_filters.widgets.FilteredSelectMultiple(attrs={"class": "custom-class"}),
        widget=forms.SelectMultiple(attrs={"class": "select22", "multiple": "multiple"}),
    )

    class Meta:
        model = EtkinlikModel
        fields = ["etkinlik_last_updated", "etkinlik_owner", "etkinlik_name", "etkinlik_tags"]


# class EtkinlikModel(BaseModelSoftDelete):
#     etkinlik_date = models.DateTimeField(auto_now_add=True)
#     etkinlik_last_updated = models.DateTimeField(auto_now=True)  # Auto-updated on every save
#     etkinlik_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
#     etkinlik_name = models.CharField(max_length=250)
#     etkinlik_description = models.TextField()
#     etkinlik_tags = models.ManyToManyField(Tag, blank=True)
#     etkinlik_youtubelink = EmbedVideoField(max_length=200, blank=True, null=True)
#     etkinlik_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
#     is_active = models.BooleanField(_("active"), default=True)
#     objects = ActiveObjectsManager()

#     def __str__(self):
#         return self.etkinlik_name

#     def save(self, *args, **kwargs):
#         if not self.pk:  # Check if it's a new object
#             self.is_active = True  # Set is_active to True for new objects
#         super().save(*args, **kwargs)
