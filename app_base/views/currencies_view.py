from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from django.urls import reverse_lazy

from ..forms import CurrencyForm
from ..models import Currency


# //------------------------~ CURRENCY ~--------------------------------------------------------------------------
class CurrencyListView(LoginRequiredMixin, ListView):
    model = Currency
    template_name = "app_base/currencies/currencylist.html"
    context_object_name = "currencies"


class CurrencyCreateView(LoginRequiredMixin, CreateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currencies/currencyform.html"
    success_url = reverse_lazy("currencylist_view_name")


class CurrencyUpdateView(LoginRequiredMixin, UpdateView):
    model = Currency
    form_class = CurrencyForm
    template_name = "app_base/currencies/currencyform.html"
    success_url = reverse_lazy("currencylist_view_name")


class CurrencyDeleteView(LoginRequiredMixin, DeleteView):
    model = Currency
    template_name = "app_base/currencies/currencyconfirm_delete.html"
    success_url = reverse_lazy("currencylist_view_name")
