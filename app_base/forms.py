from django import forms

from .models import Currency, Islemler, MuUser, Tag


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
        fields = ["username", "password", "first_name", "last_name"]  # Adjust fields as needed # TODO gerekli alanlar eklencek

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


# //-------------------------------------------------~~-------------------------------------------------


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
