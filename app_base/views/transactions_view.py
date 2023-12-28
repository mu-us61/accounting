from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, redirect, render

from django.utils.decorators import method_decorator

from django.views import View
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from ..filters import IslemlerFilter
from ..forms import TransactionForm
from ..models import Islemler
from ..tables import IslemlerTable


# //------------------------~ TRANSACTIONS ~--------------------------------------------------------------------------
class TransactionListView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_list.html"
    items_per_page = 10  # You can change the number of items per page as needed

    def get(self, request):
        transactions = Islemler.objects.filter(islemsahibi=request.user).order_by("-islem_tarihi")

        # Create a Paginator instance
        paginator = Paginator(transactions, self.items_per_page)

        # Get the current page number from the request's GET parameters
        page = request.GET.get("page")

        # Get the transactions for the current page
        transactions = paginator.get_page(page)

        return render(request, self.template_name, {"transactions": transactions})


# @method_decorator(login_required, name="dispatch")
class TransactionCreateView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_create.html"

    def get(self, request):
        form = TransactionForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # print(request.POST)
        # form = TransactionForm(request.POST)
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form)
            transaction = form.save(commit=False)
            transaction.islemsahibi = request.user
            transaction.is_active = True
            transaction.save()
            form.save_m2m()
            # Update balances here if needed
            return redirect("transactiontable_view_name")
        return render(request, self.template_name, {"form": form})


# @method_decorator(login_required, name="dispatch")
class TransactionDetailView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_detail.html"

    def get(self, request, pk):
        transaction = Islemler.all_objects.get(pk=pk, islemsahibi=request.user)
        return render(request, self.template_name, {"transaction": transaction})


class TransactionPuplicDetailView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_public_detail.html"

    def get(self, request, pk):
        transaction = Islemler.all_objects.get(pk=pk)
        return render(request, self.template_name, {"transaction": transaction})


def is_owner_or_admin(user, transaction):
    return user == transaction.islemsahibi or user.is_staff


# class TransactionUpdateView(LoginRequiredMixin, View):
#     template_name = "app_base/transactions/transaction_update.html"

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         self.transaction = get_object_or_404(Islemler.all_objects, pk=kwargs["pk"])  #!TODO burda sorun var
#         # Apply the user_passes_test decorator here
#         if not is_owner_or_admin(request.user, self.transaction):
#             return redirect("permission_denied_page_name")
#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         form = TransactionForm(instance=self.transaction)
#         return render(request, self.template_name, {"form": form, "transaction": self.transaction})

#     def post(self, request, *args, **kwargs):
#         # form = TransactionForm(request.POST, instance=self.transaction)
#         form = TransactionForm(request.POST, request.FILES, instance=self.transaction)
#         if form.is_valid():
#             form.save()
#             # Update balances here if needed
#             return redirect("transactionlist_view_name")
#         return render(request, self.template_name, {"form": form, "transaction": self.transaction})


#     def get_queryset(self):
#         return self.model.all_objects.all()
class TransactionUpdateView(LoginRequiredMixin, View):
    template_name = "app_base/transactions/transaction_update.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.transaction = get_object_or_404(Islemler.all_objects, pk=kwargs["pk"])
        if not is_owner_or_admin(request.user, self.transaction):
            return redirect("permission_denied_page_name")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TransactionForm(instance=self.transaction)
        return render(request, self.template_name, {"form": form, "transaction": self.transaction})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST, request.FILES, instance=self.transaction)
        if form.is_valid():
            form.save()
            return redirect("transactiontable_view_name")
        return render(request, self.template_name, {"form": form, "transaction": self.transaction})

    # def get_queryset(self):
    #     # Fetch both active and deleted objects using all_objects manager
    #     return self.model.all_objects()


# @method_decorator(login_required, name="dispatch")
class TransactionDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        transaction = get_object_or_404(Islemler.all_objects, pk=pk, islemsahibi=request.user)
        return render(request, "app_base/transactions/transaction_delete.html", {"transaction": transaction})

    def post(self, request, pk):
        transaction = get_object_or_404(Islemler.all_objects, pk=pk, islemsahibi=request.user)
        transaction.delete()
        # Update balances here if needed
        return redirect("transactionlist_view_name")


# //------------------------~TRANSACTION BIG TABLE~--------------------------------------------------------------------------


class TransactionTableView(SingleTableMixin, FilterView):
    table_class = IslemlerTable
    model = Islemler
    template_name = "app_base/transactions/transaction_big_table.html"
    filterset_class = IslemlerFilter

    # def get(self, request, *args, **kwargs):
    #     # Log information to the console using print()
    #     print("Request:", dir(request.GET))
    #     # You can print other information as needed

    #     # Call the super class's get method to continue the view execution
    #     return super().get(request, *args, **kwargs)


class TransactionTableMaskedView(SingleTableMixin, FilterView):
    table_class = IslemlerTable
    model = Islemler
    template_name = "app_base/transactions/transaction_big_tablemasked.html"
    filterset_class = IslemlerFilter

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()
