from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from django.urls import reverse_lazy

from ..forms import CurrencyForm
from ..models import Currency
from ..izinler import WritePermissionRequiredMixin, DeletePermissionRequiredMixin


# //------------------------~ CURRENCY ~--------------------------------------------------------------------------
class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = "app_base/currencies/currencylist.html"
    context_object_name = "currencies"


class CurrencyListMaskedView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = "app_base/currencies/currencylistmasked.html"
    context_object_name = "currencies"  #!TODO eklencek all_objects.get_deleted()

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


class CurrencyCreateView(LoginRequiredMixin, WritePermissionRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currencies/currencyform.html"
    success_url = reverse_lazy("currencylist_view_name")


# class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
#     model = Currency
#     form_class = CurrencyForm
#     template_name = "app_base/currencies/currencyform.html"
#     success_url = reverse_lazy("currencylist_view_name")

#     def get_queryset(self):
#         return self.model.all_objects.all()
from django.views.generic import UpdateView
from ..models import Currency
from ..forms import CurrencyForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class CurrencyUpdateView(LoginRequiredMixin, WritePermissionRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currencies/currencyform.html"
    success_url = reverse_lazy("currencylist_view_name")

    def get_queryset(self):
        return self.model.all_objects.all()


class CurrencyDeleteView(LoginRequiredMixin, DeletePermissionRequiredMixin, DeleteView):
    model = Currency
    template_name = "app_base/currencies/currencyconfirm_delete.html"
    success_url = reverse_lazy("currencylist_view_name")

    def get_queryset(self):
        return self.model.all_objects.all()
