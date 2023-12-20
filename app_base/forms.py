from django import forms

from .models import Currency, Islemler, MuUser, Tag
from datetime import datetime


# class CurrencyForm(forms.ModelForm):
#     class Meta:
#         model = Currency
#         fields = ["name", "abbreviation"]
from django import forms
from .models import Currency


class CurrencyForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Is Active", required=False)

    class Meta:
        model = Currency
        fields = ["name", "abbreviation", "is_active"]


class MuUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # is_active = forms.CheckboxInput()
    is_active = forms.BooleanField(label="Aktif", required=False)  # Use BooleanField for is_active

    class Meta:
        model = MuUser
        # fields = "__all__"
        # exclude = ["pk"]
        fields = ["username", "password", "first_name", "is_active"]  # Adjust fields as needed

    def clean_username(self):
        return self.cleaned_data["username"].lower()

    def clean_first_name(self):
        return self.cleaned_data["first_name"].lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use set_password to hash the password
        user.set_password(self.cleaned_data["password"])
        user.is_active = self.cleaned_data["is_active"]  # Assign is_active value
        if commit:
            user.save()
        return user


# //-------------------------------------------------~~-------------------------------------------------


# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Islemler
#         fields = ["kimden_geldi", "kime_gitti", "exelusers", "tags", "islem_ismi", "islem_aciklamasi", "currency", "miktar", "islemler_picture", "islemler_pdf"]
class TransactionForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Is Active", required=False)

    class Meta:
        model = Islemler
        fields = ["kimden_geldi", "kime_gitti", "exelusers", "tags", "islem_ismi", "islem_aciklamasi", "currency", "miktar", "islemler_picture", "islemler_pdf", "is_active"]


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


# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ["name"]


#     def clean_name(self):
#         return self.cleaned_data["name"].lower()
class TagForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Is Active", required=False)

    class Meta:
        model = Tag
        fields = ["name", "is_active"]

    def clean_name(self):
        return self.cleaned_data["name"].lower()


# //------------------------~~--------------------------------------------------------------------------

from django import forms
from .models import EvrakModel


# class EvrakForm(forms.ModelForm):
#     class Meta:
#         model = EvrakModel
#         # fields = "__all__"
#         exclude = ["evrak_owner"]
from django import forms
from .models import EvrakModel


class EvrakForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Is Active", required=False)

    class Meta:
        model = EvrakModel
        exclude = ["evrak_owner"]  # You can exclude fields if needed

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


# class EtkinlikForm(forms.ModelForm):
#     class Meta:
#         model = EtkinlikModel
#         exclude = ["etkinlik_owner"]  # You can exclude fields if needed
from django import forms
from .models import EtkinlikModel


class EtkinlikForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Is Active", required=False)

    class Meta:
        model = EtkinlikModel
        exclude = ["etkinlik_owner"]  # You can exclude fields if needed


# class ExcelUploadForm(forms.Form):
#     excel_file = forms.FileField()

from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import ExelUsers


# class ExelUsersForm(forms.ModelForm):
#     class Meta:
#         model = ExelUsers
#         exclude = []
class ExelUsersForm(forms.ModelForm):
    is_active = forms.BooleanField(label="Is Active", required=False)

    class Meta:
        model = ExelUsers
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ExelUsersForm, self).__init__(*args, **kwargs)
        self.fields["is_active"].initial = self.instance.is_active if self.instance else False
