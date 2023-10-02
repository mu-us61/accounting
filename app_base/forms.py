from django import forms
from .models import MuUser  # Import your custom user model
from .models import Islemler
from .models import Tag


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


# //-------------------------------------------------~~-------------------------------------------------


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
