from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from ..models import EtkinlikModel
from ..forms import EtkinlikForm


class EtkinlikCreateView(CreateView):
    model = EtkinlikModel
    form_class = EtkinlikForm
    template_name = "etkinlik_create.html"
    success_url = reverse_lazy("etkinlik_list")


class EtkinlikListView(ListView):
    model = EtkinlikModel
    template_name = "etkinlik_list.html"
    context_object_name = "etkinlik_list"


class EtkinlikUpdateView(UpdateView):
    model = EtkinlikModel
    form_class = EtkinlikForm
    template_name = "etkinlik_update.html"
    success_url = reverse_lazy("etkinlik_list")


class EtkinlikDeleteView(DeleteView):
    model = EtkinlikModel
    template_name = "etkinlik_delete.html"
    success_url = reverse_lazy("etkinlik_list")


class EtkinlikDetailView(DetailView):
    model = EtkinlikModel
    template_name = "etkinlik_detail.html"
    context_object_name = "etkinlik"
