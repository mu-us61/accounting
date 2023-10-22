# import django_tables2 as tables
# from .models import Islemler


# class IslemlerTable(tables.Table):
#     class Meta:
#         model = Islemler
#         attrs = {"class": "table table-striped table-bordered"}
#         per_page = 10  # Number of items to display per page
import django_tables2 as tables
from .models import Islemler


class IslemlerTable(tables.Table):
    tags = tables.Column(verbose_name="Tags")  # Create a custom column for the 'tags' field

    class Meta:
        model = Islemler
        attrs = {"class": "table table-striped table-bordered"}
        per_page = 10  # Number of items to display per page
        template_name = "app_base/transactions/transaction_big_table_pagination.html"

    def render_tags(self, value):
        # Define how you want to display the ManyToMany field 'tags'
        # You can customize this based on your requirements
        return ", ".join(tag.name for tag in value.all())


# //------------------------~~--------------------------------------------------------------------------
# tables.py
import django_tables2 as tables
from .models import EvrakModel, EtkinlikModel


class EvrakTable(tables.Table):
    evrak_tags = tables.Column(verbose_name="Etiketler", empty_values=(), orderable=True)
    evrak_date = tables.Column(verbose_name="Tarih")  # Customize the "evrak_date" column header
    evrak_owner = tables.Column(verbose_name="Evrağı Yükleyen")  # Customize the "evrak_owner" column header
    # evrak_name = tables.Column(verbose_name="Evrak İsmi")  # Customize the "evrak_name" column header
    evrak_type = tables.Column(verbose_name="Tür")  # Customize the "evrak_type" column header
    # evrak_description = tables.Column(verbose_name="Açıklama")  # Customize the "evrak_description" column header

    # Create a clickable link for the evrak_name field
    evrak_name = tables.LinkColumn(
        "evrak_detail",  # Replace with your actual view name for evrak details
        text=lambda record: record.evrak_name,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "evrak-name-link"}},  # Add any additional classes or attributes
        verbose_name="Evrak İsmi",
    )

    class Meta:
        model = EvrakModel
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "django_tables2/table.html"  # Use the default table template
        per_page = 10  # Number of items to display per page
        template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        fields = ("evrak_date", "evrak_owner", "evrak_name", "evrak_type", "evrak_tags")

    def render_evrak_tags(self, value):
        return ", ".join(tag.name for tag in value.all())


# //------------------------~~--------------------------------------------------------------------------


class EtkinlikTable(tables.Table):
    etkinlik_date = tables.Column(verbose_name="Tarih")
    etkinlik_owner = tables.Column(verbose_name="Etkinliği Oluşturan")
    etkinlik_name = tables.LinkColumn(
        "etkinlik_detail",
        verbose_name="Etkinlik İsmi",
        text=lambda record: record.etkinlik_name,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}},  # Add any additional classes or attributes
    )
    etkinlik_tags = tables.Column(verbose_name="Etiketler", empty_values=(), orderable=True)

    class Meta:
        model = EtkinlikModel
        attrs = {"class": "table table-striped table-bordered"}
        template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        fields = ("etkinlik_date", "etkinlik_owner", "etkinlik_name", "etkinlik_tags")

    def render_etkinlik_tags(self, value):
        return ", ".join(tag.name for tag in value.all())


# class EtkinlikModel(models.Model):
#     etkinlik_date = models.DateTimeField(auto_now_add=True)
#     etkinlik_last_updated = models.DateTimeField(auto_now=True)  # Auto-updated on every save
#     etkinlik_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
#     etkinlik_name = models.CharField(max_length=250)
#     etkinlik_description = models.TextField()
#     etkinlik_tags = models.ManyToManyField(Tag, blank=True)
#     etkinlik_youtubelink = models.CharField(max_length=200, blank=True, null=True)
#     etkinlik_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)

#     def __str__(self):
#         return self.etkinlik_name

# //------------------------~~--------------------------------------------------------------------------
# tables.py

# tables.py

import django_tables2 as tables
from .models import MuUser, Currency


class UserBalanceTable(tables.Table):
    username = tables.Column(verbose_name="Kullanıcılar")

    def __init__(self, *args, currencies, **kwargs):
        super(UserBalanceTable, self).__init__(*args, **kwargs)
        for currency in currencies:
            self.base_columns[currency.name] = tables.Column()

    class Meta:
        model = MuUser
        attrs = {"class": "table table-striped table-bordered"}
        fields = ["username"]
