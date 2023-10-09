from django import forms

from .models import Currency, Islemler, MuUser, Tag
from datetime import datetime


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ["name", "abbreviation"]


class MuUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MuUser
        # fields = "__all__"
        # exclude = ["pk"]
        fields = ["username", "password", "first_name", "last_name"]  # Adjust fields as needed

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use set_password to hash the password
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# //-------------------------------------------------~~-------------------------------------------------


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Islemler
        fields = ["kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islem_aciklamasi", "currency", "miktar"]


class TransactionFilterForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=MuUser.objects.all(),
        label="User",
        required=False,
        widget=forms.Select(attrs={"class": "select2"}),
    )
    kimden_geldi = forms.ModelChoiceField(
        queryset=MuUser.objects.all(),
        label="Kimden Geldi",
        required=False,
        widget=forms.Select(attrs={"class": "select2"}),
    )
    kime_gitti = forms.ModelChoiceField(
        queryset=MuUser.objects.all(),
        label="Kime Gitti",
        required=False,
        widget=forms.Select(attrs={"class": "select2"}),
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        label="Currency",
        required=False,
        widget=forms.Select(attrs={"class": "select2"}),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        label="Tags",
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "select2"}),
    )
    # date_filter_year = forms.IntegerField(
    #     label="Year",
    #     required=False,
    #     widget=forms.Select(attrs={"class": "select2"}),
    # )
    # date_filter_month = forms.IntegerField(
    #     label="Month",
    #     required=False,
    #     widget=forms.Select(attrs={"class": "select2"}),
    # )
    # date_filter_day = forms.IntegerField(
    #     label="Day",
    #     required=False,
    #     widget=forms.Select(attrs={"class": "select2"}),
    # )
    # Year choices (Modify the range as needed)
    year_choices = [(str(year), str(year)) for year in range(datetime.now().year, 2000, -1)]
    date_filter_year = forms.ChoiceField(
        label="Year",
        required=False,
        choices=[("", "Any")] + year_choices,  # Include an "Any" option
        widget=forms.Select(attrs={"class": "select2"}),
    )

    # Month choices
    month_choices = [("01", "January"), ("02", "February"), ("03", "March"), ("04", "April"), ("05", "May"), ("06", "June"), ("07", "July"), ("08", "August"), ("09", "September"), ("10", "October"), ("11", "November"), ("12", "December")]
    date_filter_month = forms.ChoiceField(
        label="Month",
        required=False,
        choices=[("", "Any")] + month_choices,  # Include an "Any" option
        widget=forms.Select(attrs={"class": "select2"}),
    )

    # Day choices (Assuming 1-31 for all days of the month)
    day_choices = [(str(day).zfill(2), str(day).zfill(2)) for day in range(1, 32)]
    date_filter_day = forms.ChoiceField(
        label="Day",
        required=False,
        choices=[("", "Any")] + day_choices,  # Include an "Any" option
        widget=forms.Select(attrs={"class": "select2"}),
    )


# //-------------------------------------------------~~-------------------------------------------------


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
