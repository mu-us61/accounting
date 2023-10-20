in my django project , here is my model;

EVRAK_TYPE_CHOICES = [
    ("gelen", "Gelen"),
    ("giden", "Giden"),
]


class EvrakModel(models.Model):
    evrak_date = models.DateTimeField(auto_now_add=True)
    evrak_last_updated = models.DateTimeField(auto_now=True)
    evrak_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    evrak_tags = models.ManyToManyField(Tag, blank=True)
    evrak_name = models.CharField(max_length=250)
    evrak_description = models.TextField()
    evrak_type = models.CharField(max_length=7, choices=EVRAK_TYPE_CHOICES, default="gelen")
    evrak_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
    evrak_pdf = models.FileField(upload_to=generate_unique_filename, blank=True, null=True)

    def __str__(self):
        return self.evrak_name
    

and its list view;

class EvrakListView(ListView):
    model = EvrakModel
    template_name = "app_base/evraklar/evrak_list.html"
    context_object_name = "evrak_list"


so what I want is instead of list I want table and please use django_tables2 , also with pagination