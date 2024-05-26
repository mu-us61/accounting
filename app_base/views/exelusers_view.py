from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import ExelUsers
from ..forms import ExelUsersForm
from django.shortcuts import render, redirect
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from ..izinler import WritePermissionRequiredMixin, DeletePermissionRequiredMixin


class ExelUsersCreateView(WritePermissionRequiredMixin, CreateView):
    model = ExelUsers
    form_class = ExelUsersForm
    template_name = "app_base/exelusers/exelusers_create.html"
    success_url = reverse_lazy("exelusers_list")

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     print(form.data)  # Print form data before validation
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        print(form.cleaned_data)  # Check the form data before saving
        return super().form_valid(form)


# class ExelUsersListView(ListView):
#     model = ExelUsers
#     template_name = "app_base/exelusers/exelusers_list.html"
#     context_object_name = "exelusers_list"
from django_tables2 import RequestConfig
from ..models import ExelUsers
from ..tables import ExelUsersTable, DeletedExelUsersTable
from ..filters import ExelUsersFilter, ExelUsersFilterMasked


from django.http import HttpResponse
from django.conf import settings
import os


def download_excel(request):
    # Path to your Excel file
    file_path = os.path.join(settings.STATIC_ROOT, "excel", "ornek.xlsx")

    # Open the file for reading
    with open(file_path, "rb") as f:
        # Prepare response
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        # Set the filename
        response["Content-Disposition"] = 'attachment; filename="ornek.xlsx"'
        return response


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
    table_class = DeletedExelUsersTable
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_listmasked.html"
    # context_table_name = "etkinlik_table"
    filterset_class = ExelUsersFilterMasked

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


from django.views.decorators.http import require_POST


@require_POST
def reactivate_exelusers(request):
    try:
        exelusers_id = request.POST.get("exelusers_id")

        exelusers = ExelUsers.all_objects.get(pk=exelusers_id)
        exelusers.is_active = True
        exelusers.save()

        return redirect("exelusers_list")
    except ExelUsers.DoesNotExist:
        pass


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


class ExelUsersUpdateView(WritePermissionRequiredMixin, UpdateView):
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


class ExelUsersDeleteView(DeletePermissionRequiredMixin, DeleteView):
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
