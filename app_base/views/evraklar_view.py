from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import EvrakModel
from ..forms import EvrakForm
from django_filters.views import FilterView
from ..filters import EvrakModelFilter
from ..izinler import WritePermissionRequiredMixin, DeletePermissionRequiredMixin

# from ..izinler import CanWriteMixin, CanDeleteMixin


class EvrakCreateView(WritePermissionRequiredMixin, CreateView):
    model = EvrakModel
    form_class = EvrakForm
    template_name = "app_base/evraklar/create_evrak.html"
    success_url = reverse_lazy("evrak_list")

    def form_valid(self, form):
        form.instance.evrak_owner = self.request.user  # Set the owner to the currently logged-in user
        form.instance.is_active = True  # Set is_active to True
        return super().form_valid(form)


# class EvrakListView(ListView):
#     model = EvrakModel
#     template_name = "app_base/evraklar/evrak_list.html"
#     context_object_name = "evrak_list"
from django_tables2 import SingleTableMixin
from ..models import EvrakModel
from ..tables import EvrakTable, EvrakSilinenlerTable


class EvrakListView(SingleTableMixin, FilterView):
    table_class = EvrakTable
    model = EvrakModel
    template_name = "app_base/evraklar/evrak_list.html"
    filterset_class = EvrakModelFilter
    # context_table_name = "evrak_table"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["filter"] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
    #     return context

    # def get(self, request, *args, **kwargs):
    #     aa = self.get_table()
    #     print(dir(aa.page.paginator))  # Print the request object for debugging
    #     return super().get(request, *args, **kwargs)


class EvrakSilinenlerListView(SingleTableMixin, FilterView):
    table_class = EvrakSilinenlerTable
    model = EvrakModel
    template_name = "app_base/evraklar/evrak_silinenler_list.html"
    filterset_class = EvrakModelFilter
    # context_table_name = "evrak_table"

    def get_queryset(self):
        # Fetch both active and deleted objects using all_objects manager
        return self.model.all_objects.get_deleted()


# class EvrakUpdateView(UpdateView):
#     model = EvrakModel
#     form_class = EvrakForm
#     template_name = "app_base/evraklar/update_evrak.html"
#     success_url = reverse_lazy("evrak_list")

#     def get_queryset(self):
#         return self.model.all_objects.all()
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from ..models import EvrakModel
from ..forms import EvrakForm


class EvrakUpdateView(WritePermissionRequiredMixin, UpdateView):
    model = EvrakModel
    form_class = EvrakForm
    template_name = "app_base/evraklar/update_evrak.html"
    success_url = reverse_lazy("evrak_list")

    def get_queryset(self):
        return self.model.all_objects.all()


class EvrakDeleteView(DeletePermissionRequiredMixin, DeleteView):
    model = EvrakModel
    template_name = "app_base/evraklar/delete_evrak.html"
    success_url = reverse_lazy("evrak_list")

    def get_queryset(self):
        return self.model.all_objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context[""] =
    #     print(context)
    #     return context

    # print(evrak.evrak_name)
    # def get(self, request, *args, **kwargs):
    #     # aa = self.get_table()
    #     # print(dir(aa.page.paginator))  # Print the request object for debugging
    #     print(dir(request))
    #     return super().get(request, *args, **kwargs)


class EvrakDetailView(DetailView):
    model = EvrakModel
    template_name = "app_base/evraklar/evrak_detail.html"
    context_object_name = "evrak"

    def get_queryset(self):
        return self.model.all_objects.all()
