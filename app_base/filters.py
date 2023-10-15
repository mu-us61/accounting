# filters.py
import django_filters
from .models import Islemler, MuUser, Tag, Currency
from django import forms
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
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

    # # Custom filter method for miktar
    # def custom_miktar_filter(self, queryset, name, value):
    #     # Implement your custom filtering logic for the 'miktar' field here
    #     if value:
    #         # Process the filter value and update the queryset as needed
    #         pass
    #     return queryset


# class IslemlerFilter(django_filters.FilterSet):
#     miktar = django_filters.NumberFilter()
#     islem_tarihi = django_filters.DateFromToRangeFilter(field_name="islem_tarihi")
#     kimden_geldi = django_filters.ModelChoiceFilter(queryset=MuUser.objects.all())
#     kime_gitti = django_filters.ModelChoiceFilter(queryset=MuUser.objects.all())
#     tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
#     islem_ismi = django_filters.CharFilter(lookup_expr="icontains")
#     islemsahibi = django_filters.ModelChoiceFilter(queryset=MuUser.objects.all())
#     currency = django_filters.ModelChoiceFilter(queryset=Currency.objects.all())

#     class Meta:
#         model = Islemler
#         fields = ["miktar", "islem_tarihi", "kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islemsahibi", "currency"]


# class IslemlerFilter(django_filters.FilterSet):
#     miktar = django_filters.NumberFilter()


#     class Meta:
#         model = Islemler
#         fields = ["miktar"]

# islem_tarihi = models.DateTimeField(auto_now_add=True)
# # belge =
# islemsahibi = models.ForeignKey(MuUser, on_delete=models.PROTECT)
# kimden_geldi = models.ForeignKey(MuUser, related_name="gelen_paralar", on_delete=models.PROTECT, null=True, blank=True)
# kime_gitti = models.ForeignKey(MuUser, related_name="giden_paralar", on_delete=models.PROTECT, null=True, blank=True)
# tags = models.ManyToManyField(Tag, blank=True)
# islem_ismi = models.CharField(max_length=250)
# islem_aciklamasi = models.TextField()
# currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
# miktar = models.IntegerField(default=0)

# username = django_filters.CharFilter(lookup_expr="icontains")
