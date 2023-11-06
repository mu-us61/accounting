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
        fields = ["kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islem_aciklamasi", "currency", "miktar", "islemler_picture", "islemler_pdf"]


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
    # start_date = forms.DateField(
    #     label="Başlangıç Tarihi",
    #     required=False,
    #     widget=forms.DateInput(
    #         attrs={"class": "input", "type": "date"},
    #         format="%Y-%m-%d",  # Format for date input
    #     ),
    #     input_formats=["%d/%m/%Y", "%Y-%m-%d"],  # Add Turkish date format
    # )
    # end_date = forms.DateField(
    #     label="Bitiş Tarihi",
    #     required=False,
    #     widget=forms.DateInput(
    #         attrs={"class": "input", "type": "date"},
    #         format="%Y-%m-%d",  # Format for date input
    #     ),
    #     input_formats=["%d/%m/%Y", "%Y-%m-%d"],  # Add Turkish date format
    # )
    start_date = forms.DateField(
        label="Başlangıç Tarihi",
        required=False,
        widget=forms.DateInput(attrs={"class": "input", "type": "date"}),
    )
    end_date = forms.DateField(
        label="Bitiş Tarihi",
        required=False,
        widget=forms.DateInput(attrs={"class": "input", "type": "date"}),
    )


# //-------------------------------------------------~~-------------------------------------------------


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


# //------------------------~~--------------------------------------------------------------------------

from django import forms
from .models import EvrakModel


class EvrakForm(forms.ModelForm):
    class Meta:
        model = EvrakModel
        # fields = "__all__"
        exclude = ["evrak_owner"]

    # widgets = {
    #     "evrak_name": forms.TextInput(attrs={"class": "input"}),
    #     "evrak_description": forms.Textarea(attrs={"class": "textarea"}),
    #     "evrak_type": forms.Select(attrs={"class": "select"}),
    #     "evrak_picture": forms.ClearableFileInput(attrs={"class": "file-input"}),
    #     "evrak_pdf": forms.ClearableFileInput(attrs={"class": "file-input"}),
    #     "evrak_tags": forms.SelectMultiple(attrs={"class": "select is-multiple"}),
    # }


# //------------------------~~--------------------------------------------------------------------------

from django import forms
from .models import EtkinlikModel


class EtkinlikForm(forms.ModelForm):
    class Meta:
        model = EtkinlikModel
        exclude = ["etkinlik_owner"]  # You can exclude fields if needed


# class ExcelUploadForm(forms.Form):
#     excel_file = forms.FileField()

from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import ExelUsers


class ExelUsersForm(forms.ModelForm):
    class Meta:
        model = ExelUsers
        exclude = []
