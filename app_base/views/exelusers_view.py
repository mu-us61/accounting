from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import ExelUsers
from ..forms import ExelUsersForm


class ExelUsersCreateView(CreateView):
    model = ExelUsers
    form_class = ExelUsersForm
    template_name = "app_base/exelusers/exelusers_create.html"
    success_url = reverse_lazy("exelusers_list")


class ExelUsersListView(ListView):
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_list.html"
    context_object_name = "exelusers_list"


class ExelUsersUpdateView(UpdateView):
    model = ExelUsers
    form_class = ExelUsersForm
    template_name = "app_base/exelusers/exelusers_update.html"
    success_url = reverse_lazy("exelusers_list")


class ExelUsersDeleteView(DeleteView):
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_delete.html"
    success_url = reverse_lazy("exelusers_list")


class ExelUsersDetailView(DetailView):
    model = ExelUsers
    template_name = "app_base/exelusers/exelusers_detail.html"
    context_object_name = "exelusers"
