from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, template_name="app_base/index.html")
