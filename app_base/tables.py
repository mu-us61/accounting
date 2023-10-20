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
from .models import EvrakModel


class EvrakTable(tables.Table):
    evrak_tags = tables.Column(verbose_name="Tags", empty_values=(), orderable=True)

    class Meta:
        model = EvrakModel
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "django_tables2/table.html"  # Use the default table template
        per_page = 10  # Number of items to display per page
        template_name = "app_base/evraklar/evrak_list_pagination.html"
        fields = ("evrak_date", "evrak_owner", "evrak_name", "evrak_type", "evrak_description", "evrak_tags")

    def render_evrak_tags(self, value):
        return ", ".join(tag.name for tag in value.all())
