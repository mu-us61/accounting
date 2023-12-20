from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import EtkinlikModel
from ..forms import EtkinlikForm
from django_tables2 import SingleTableView
from ..tables import EtkinlikTable
from ..filters import EtkinlikModelFilter


class EtkinlikCreateView(CreateView):
    model = EtkinlikModel
    form_class = EtkinlikForm
    template_name = "app_base/etkinlikler/etkinlik_create.html"
    success_url = reverse_lazy("etkinlik_list")

    def form_valid(self, form):
        form.instance.etkinlik_owner = self.request.user  # Set the owner to the currently logged-in user
        return super().form_valid(form)


# class EtkinlikListView(ListView):
#     model = EtkinlikModel
#     template_name = "app_base/etkinlikler/etkinlik_list.html"
#     context_object_name = "etkinlik_list"

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView


class EtkinlikListView(SingleTableMixin, FilterView):
    table_class = EtkinlikTable
    model = EtkinlikModel
    template_name = "app_base/etkinlikler/etkinlik_list.html"
    context_table_name = "etkinlik_table"
    filterset_class = EtkinlikModelFilter


class EtkinlikListMaskedView(SingleTableMixin, FilterView):
    table_class = EtkinlikTable
    model = EtkinlikModel
    template_name = "app_base/etkinlikler/etkinlik_listmasked.html"
    context_table_name = "etkinlik_table"
    filterset_class = EtkinlikModelFilter

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


# class EtkinlikUpdateView(UpdateView):
#     model = EtkinlikModel
#     form_class = EtkinlikForm
#     template_name = "app_base/etkinlikler/etkinlik_update.html"
#     success_url = reverse_lazy("etkinlik_list")

#     def get_queryset(self):
#         return self.model.all_objects.all()
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from ..models import EtkinlikModel
from ..forms import EtkinlikForm


class EtkinlikUpdateView(UpdateView):
    model = EtkinlikModel
    form_class = EtkinlikForm
    template_name = "app_base/etkinlikler/etkinlik_update.html"
    success_url = reverse_lazy("etkinlik_list")

    def get_queryset(self):
        return self.model.all_objects.all()


class EtkinlikDeleteView(DeleteView):
    model = EtkinlikModel
    template_name = "app_base/etkinlikler/etkinlik_delete.html"
    success_url = reverse_lazy("etkinlik_list")

    def get_queryset(self):
        return self.model.all_objects.all()


class EtkinlikDetailView(DetailView):
    model = EtkinlikModel
    template_name = "app_base/etkinlikler/etkinlik_detail.html"
    context_object_name = "etkinlik"

    def get_queryset(self):
        return self.model.all_objects.all()
