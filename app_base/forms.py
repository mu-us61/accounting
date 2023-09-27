from django import forms
from .models import MuUser  # Import your custom user model
from .models import Islemler


class AddUserToGroupForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=MuUser.objects.all(),
        label="Select User to Add",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class RemoveUserFromGroupForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=MuUser.objects.all(),
        label="Select Users to Remove",
        widget=forms.CheckboxSelectMultiple(),
    )


class MuUserForm(forms.ModelForm):
    class Meta:
        model = MuUser
        # fields = "__all__"
        # exclude = ["pk"]
        fields = ["username", "password", "first_name", "last_name", "bakiye_TL", "bakiye_Dolar", "bakiye_Euro", "bakiye_GBP", "bakiye_Sek"]  # Adjust fields as needed # TODO gerekli alanlar eklencek


# //-------------------------------------------------~~-------------------------------------------------


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Islemler
        fields = ["kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islem_aciklamasi", "bakiye_ilk_TL", "girdiler_TL", "ciktilar_TL", "bakiye_ilk_Euro", "girdiler_Euro", "ciktilar_Euro", "bakiye_ilk_Dolar", "girdiler_Dolar", "ciktilar_Dolar", "bakiye_ilk_GBP", "girdiler_GBP", "ciktilar_GBP", "bakiye_ilk_Sek", "girdiler_Sek", "ciktilar_Sek"]
