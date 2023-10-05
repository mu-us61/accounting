from django import forms
from .models import MuUser  # Import your custom user model
from .models import Islemler
from .models import Tag
from django.contrib.auth.forms import AuthenticationForm


class MuUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MuUser
        # fields = "__all__"
        # exclude = ["pk"]
        fields = ["username", "password", "first_name", "last_name", "bakiye_TL", "bakiye_Dolar", "bakiye_Euro", "bakiye_GBP", "bakiye_Sek"]  # Adjust fields as needed # TODO gerekli alanlar eklencek

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
        fields = ["kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islem_aciklamasi", "bakiye_ilk_TL", "girdiler_TL", "ciktilar_TL", "bakiye_ilk_Euro", "girdiler_Euro", "ciktilar_Euro", "bakiye_ilk_Dolar", "girdiler_Dolar", "ciktilar_Dolar", "bakiye_ilk_GBP", "girdiler_GBP", "ciktilar_GBP", "bakiye_ilk_Sek", "girdiler_Sek", "ciktilar_Sek"]


# //-------------------------------------------------~~-------------------------------------------------


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
