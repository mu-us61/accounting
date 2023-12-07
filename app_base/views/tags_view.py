from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import TagForm
from ..models import Tag


# //------------------------~~--------------------------------------------------------------------------
@login_required
def taglist_view(request):
    tags = Tag.objects.all().order_by("name")

    # Number of tags to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(tags, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }
    return render(request, "app_base/tags/taglist.html", context)


@login_required
def taglistmasked_view(request):
    tags = Tag.all_objects.get_deleted().order_by("name")

    # Number of tags to display per page
    per_page = 10  # You can adjust this as needed

    paginator = Paginator(tags, per_page)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
    }
    return render(request, "app_base/tags/taglistmasked.html", context)


@login_required
def tagdetail_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    return render(request, "app_base/tags/tagdetail.html", {"tag": tag})


@login_required
def tagcreate_view(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect("taglist_view_name")
    else:
        form = TagForm()
    return render(request, "app_base/tags/tagform.html", {"form": form})


@login_required
def tagupdate_view(request, slug):
    tag = get_object_or_404(Tag.all_objects, slug=slug)  #!TODO olmadi
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save()
            return redirect("tagdetail_view_name", slug=tag.slug)
    else:
        form = TagForm(instance=tag)
    return render(request, "app_base/tags/tagform.html", {"form": form, "tag": tag})


@login_required
def tagdelete_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    if request.method == "POST":
        tag.delete()
        return redirect("taglist_view_name")
    return render(request, "app_base/tags/tagconfirm_delete.html", {"tag": tag})
