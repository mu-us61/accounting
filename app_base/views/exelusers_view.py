from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import ExelUsers
from ..forms import ExelUsersForm
from django.shortcuts import render
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from ..izinler import WritePermissionRequiredMixin, DeletePermissionRequiredMixin


class ExelUsersCreateView(WritePermissionRequiredMixin,CreateView):
    model = ExelUsers
    form_class = ExelUsersForm
    template_name = "app_base/exelusers/exelusers_create.html"
    success_url = reverse_lazy("exelusers_list")


# class ExelUsersListView(ListView):
#     model = ExelUsers
#     template_name = "app_base/exelusers/exelusers_list.html"
#     context_object_name = "exelusers_list"
from django_tables2 import RequestConfig
from ..models import ExelUsers
from ..tables import ExelUsersTable
from ..filters import ExelUsersFilter, ExelUsersFilterMasked


# def exelusers_list(request):
#     queryset = ExelUsers.objects.all()
#     table = ExelUsersTable(queryset)
#     RequestConfig(request).configure(table)

#     return render(request, "app_base/exelusers/exelusers_list.html", {"table": table})


# def exelusers_listmasked(request):
#     queryset = ExelUsers.all_objects.get_deleted()
#     table = ExelUsersTable(queryset)
#     RequestConfig(request).configure(table)

#     return render(request, "app_base/exelusers/exelusers_listmasked.html", {"table": table})


class ExelusersListView(SingleTableMixin, FilterView):
    table_class = ExelUsersTable
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_list.html"
    # context_table_name = "etkinlik_table"
    filterset_class = ExelUsersFilter


class ExelusersListMaskedView(SingleTableMixin, FilterView):
    table_class = ExelUsersTable
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_listmasked.html"
    # context_table_name = "etkinlik_table"
    filterset_class = ExelUsersFilterMasked

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


# class ExelUsersUpdateView(UpdateView):
#     model = ExelUsers
#     form_class = ExelUsersForm
#     template_name = "app_base/exelusers/exelusers_update.html"
#     success_url = reverse_lazy("exelusers_list")

#     def get_queryset(self):
#         return ExelUsers.all_objects.all()

from django.views.generic import UpdateView
from ..models import ExelUsers
from ..forms import ExelUsersForm
from django.urls import reverse_lazy


class ExelUsersUpdateView(WritePermissionRequiredMixin,UpdateView):
    model = ExelUsers
    form_class = ExelUsersForm
    template_name = "app_base/exelusers/exelusers_update.html"
    success_url = reverse_lazy("exelusers_list")

    def get_queryset(self):
        return ExelUsers.all_objects.all()

    def form_valid(self, form):
        # Get the current instance being updated
        exeluser_instance = form.instance

        # Handling is_active field update
        is_active = form.cleaned_data["is_active"]
        exeluser_instance.is_active = is_active

        # Save the changes
        exeluser_instance.save()

        return super().form_valid(form)


class ExelUsersDeleteView(DeletePermissionRequiredMixin,DeleteView):
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_delete.html"
    success_url = reverse_lazy("exelusers_list")

    def get_queryset(self):
        return ExelUsers.all_objects.all()


class ExelUsersDetailView(DetailView):
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_detail.html"
    context_object_name = "exelusers"

    def get_queryset(self):
        return ExelUsers.all_objects.all()
