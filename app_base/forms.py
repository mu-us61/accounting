from django import forms
from .models import MuUser  # Import your custom user model


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
        fields = ["username", "password", "first_name", "last_name","bakiye_TL","bakiye_Dolar","bakiye_Euro","bakiye_GBP","bakiye_Sek"]  # Adjust fields as needed # TODO gerekli alanlar eklencek
