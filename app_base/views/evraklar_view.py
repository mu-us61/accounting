from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import EvrakModel
from ..forms import EvrakForm


class EvrakCreateView(CreateView):
    model = EvrakModel
    form_class = EvrakForm
    template_name = "app_base/evraklar/create_evrak.html"
    success_url = reverse_lazy("evrak_list")

    def form_valid(self, form):
        form.instance.evrak_owner = self.request.user  # Set the owner to the currently logged-in user
        return super().form_valid(form)


# class EvrakListView(ListView):
#     model = EvrakModel
#     template_name = "app_base/evraklar/evrak_list.html"
#     context_object_name = "evrak_list"
from django_tables2 import SingleTableView
from ..models import EvrakModel
from ..tables import EvrakTable


class EvrakListView(SingleTableView):
    table_class = EvrakTable
    model = EvrakModel
    template_name = "app_base/evraklar/evrak_list.html"
    context_table_name = "evrak_table"
    # paginate_by = 2  # Set your desired number of items per page

    def get(self, request, *args, **kwargs):
        aa = self.get_table()
        print(dir(aa.page.paginator))  # Print the request object for debugging
        return super().get(request, *args, **kwargs)


class EvrakUpdateView(UpdateView):
    model = EvrakModel
    form_class = EvrakForm
    template_name = "app_base/evraklar/update_evrak.html"
    success_url = reverse_lazy("evrak_list")


class EvrakDeleteView(DeleteView):
    model = EvrakModel
    template_name = "app_base/evraklar/delete_evrak.html"
    success_url = reverse_lazy("evrak_list")


class EvrakDetailView(DetailView):
    model = EvrakModel
    template_name = "app_base/evraklar/evrak_detail.html"
    context_object_name = "evrak"
