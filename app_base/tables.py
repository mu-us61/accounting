# import django_tables2 as tables
# from .models import Islemler


# class IslemlerTable(tables.Table):
#     class Meta:
#         model = Islemler
#         attrs = {"class": "table table-striped table-bordered"}
#         per_page = 10  # Number of items to display per page
import django_tables2 as tables
from .models import Islemler, Tag, MuGroup

# from .templatetags.templatehelpers import trim_decimal


class IslemlerTable(tables.Table):
    tags = tables.Column(verbose_name="Harcama Kalemi")  # Create a custom column for the 'tags' field
    exelusers = tables.Column(verbose_name="Excel Kullanıcıları")
    islem_tarihi = tables.Column(verbose_name="Tarih")  # Customize the "evrak_date" column header
    islem_ismi = tables.LinkColumn(
        "transactionpublicdetail_view_name",  # Replace with your actual view name for evrak details
        text=lambda record: record.islem_ismi,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
        verbose_name="Islem Ismi",
    )
    # miktar = tables.Column(
    #     verbose_name="Miktar",
    #     accessor="miktar",
    #     orderable=True,
    #     empty_values=(),
    #     attrs={"td": {"class": "your-class"}},
    # )
    # miktar = tables.TemplateColumn("{% load custom_filters %}{{ record.miktar|remove_trailing_zeros }}{{ record.currency.abbreviation }}")
    miktar = tables.TemplateColumn('{% load custom_filters %}{{ record.miktar|remove_trailing_zeros }}<span style="white-space: nowrap;"> {{ record.currency.abbreviation }}</span>')

    class Meta:
        model = Islemler
        attrs = {"class": "table table-striped table-bordered"}
        per_page = 10  # Number of items to display per page
        # template_name = "app_base/transactions/transaction_big_table_pagination.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ("islem_tarihi", "islemler_type", "islemsahibi", "kimden_geldi", "kime_gitti", "exelusers", "tags", "islem_ismi", "currency", "miktar", "islemler_picture", "islemler_pdf")

    def render_tags(self, value):
        # Define how you want to display the ManyToMany field 'tags'
        # You can customize this based on your requirements
        return ", ".join(tag.name for tag in value.all())

    def render_exelusers(self, value):
        # Define how you want to display the ManyToMany field 'tags'
        # You can customize this based on your requirements
        return ", ".join(exeluser.name for exeluser in value.all())

    # def render_miktar(self, value):
    #     return trim_decimal(value)


# //------------------------~~--------------------------------------------------------------------------
# tables.py
import django_tables2 as tables
from .models import EvrakModel, EtkinlikModel, ActiveObjectsManager

# your_long_field = tables.TemplateColumn(template_code='{{ value|truncatechars:50 }}')


class EvrakTable(tables.Table):
    evrak_tags = tables.Column(verbose_name="Harcama Kalemi", empty_values=(), orderable=True)
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
        attrs={"a": {"class": "evrak-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
        verbose_name="Evrak İsmi",
        # attrs={'td': {'class': 'long-text'}}
    )
    evrak_takipno = tables.Column(verbose_name="Evrak Takip no")

    class Meta:
        model = EvrakModel
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "django_tables2/table.html"  # Use the default table template
        per_page = 10  # Number of items to display per page
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ("evrak_date", "evrak_owner", "evrak_name", "evrak_type", "evrak_tags")

    def render_evrak_tags(self, value):
        return ", ".join(tag.name for tag in value.all())


class EvrakSilinenlerTable(tables.Table):
    evrak_tags = tables.Column(verbose_name="Harcama Kalemi", empty_values=(), orderable=True)
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
        attrs={"a": {"class": "evrak-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
        verbose_name="Evrak İsmi",
        # attrs={'td': {'class': 'long-text'}}
    )

    class Meta:
        model = EvrakModel
        queryset = EvrakModel.objects.filter(is_active=False)
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "django_tables2/table.html"  # Use the default table template
        per_page = 10  # Number of items to display per page
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ("evrak_date", "evrak_owner", "evrak_name", "evrak_type", "evrak_tags")

    # def __init__(self, *args, **kwargs):
    #     super(EvrakTable, self).__init__(*args, **kwargs)
    #     # Filter the queryset to show only instances where is_active is False
    #     self.queryset = EvrakModel.objects.filter(is_active=False)

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
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )
    etkinlik_tags = tables.Column(verbose_name="Harcama Kalemi", empty_values=(), orderable=True)

    class Meta:
        model = EtkinlikModel
        per_page = 10  # Number of items to display per page
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
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
from decimal import Decimal


# class UserBalanceTable(tables.Table):
#     username = tables.Column(verbose_name="Kullanıcılar")

#     def __init__(self, *args, currencies, **kwargs):
#         super(UserBalanceTable, self).__init__(*args, **kwargs)
#         for currency in currencies:
#             self.base_columns[currency.name] = tables.Column()

#     class Meta:
#         model = MuUser
#         fields = ["username"]
#         attrs = {"class": "table table-striped table-bordered is-narrow"}
#         template_name = "app_base/unsorted/django_tables_custom_bulma.html"  # You can choose a different template if needed


# class UserBalanceTable(tables.Table):
#     username = tables.Column(verbose_name="Username")

#     # Define columns for each currency
#     def __init__(self, *args, **kwargs):
#         currencies = kwargs.pop("currencies", [])
#         for currency in currencies:
#             # self.base_columns[currency.abbreviation] = tables.Column(verbose_name=currency.name)
#             self.base_columns[currency.abbreviation] = tables.Column(verbose_name=currency.name)
#         super().__init__(*args, **kwargs)

#     class Meta:
#         per_page = 10  # Number of items to display per page
#         attrs = {"class": "table table-striped table-bordered"}
#         template_name = "app_base/unsorted/django_tables_custom_bulma_balance.html"
import django_tables2 as tables


# class UserBalanceTable(tables.Table):
#     username = tables.Column(verbose_name="Username")

#     # Define columns for each currency
#     def __init__(self, *args, **kwargs):
#         currencies = kwargs.pop("currencies", [])
#         for currency in currencies:
#             self.base_columns[currency.abbreviation] = tables.Column(verbose_name=f"{currency.name} ({currency.abbreviation})", accessor=f"{currency.abbreviation}.balance_with_abbreviation", attrs={"th": {"class": "balance-header"}})  # Combined accessor  # Add CSS class to header
#         super().__init__(*args, **kwargs)

#     class Meta:
#         per_page = 10  # Number of items to display per page
#         attrs = {"class": "table table-striped table-bordered"}
#         template_name = "app_base/unsorted/django_tables_custom_bulma_balance.html"


class UserBalanceTable(tables.Table):
    username = tables.Column(verbose_name="Username")

    def __init__(self, *args, **kwargs):
        currencies = kwargs.pop("currencies", [])
        for currency in currencies:
            self.base_columns[currency.abbreviation] = tables.Column(verbose_name=f"{currency.name} ({currency.abbreviation})", accessor=currency.abbreviation, attrs={"th": {"class": "balance-header"}})  # Access the column directly without custom formatting
        super().__init__(*args, **kwargs)

    class Meta:
        per_page = 10
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma_balance.html"
        template_name = "django_tables2/bootstrap5-responsive.html"


# //------------------------~~--------------------------------------------------------------------------


class TableProvenTags(tables.Table):
    aylar = tables.Column(verbose_name="Aylar")
    toplam = tables.Column(verbose_name="Toplam İşlem Sayısı (Giden)")
    belgeli = tables.Column(verbose_name="Belgeli Sayısı (Giden)")
    yuzdesi = tables.Column(verbose_name="Belegeli Yüzdesi (Giden)")
    toplam_gelen = tables.Column(verbose_name="Toplam Gelen Para")
    toplam_giden = tables.Column(verbose_name="Toplam Giden Para")
    ispatlilar = tables.Column(verbose_name="İspatliların Yüzdesi")

    class Meta:
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"


# //------------------------~~--------------------------------------------------------------------------

import django_tables2 as tables
from .models import ExelUsers


class ExelUsersTable(tables.Table):
    # name = tables.Column()
    # surname = tables.Column()
    phonenumber = tables.Column(verbose_name="Telefon No")
    name = tables.LinkColumn(
        "exelusers_detail",  # Replace with your actual view name for evrak details
        text=lambda record: record.name,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
        verbose_name="Excel Kullanıcısı",
    )

    class Meta:
        model = ExelUsers
        fields = ["name", "phonenumber"]
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"  # You can choose a different template if needed
        template_name = "django_tables2/bootstrap5-responsive.html"


from django_tables2 import TemplateColumn


class DeletedExelUsersTable(tables.Table):
    # name = tables.Column()
    # surname = tables.Column()
    phonenumber = tables.Column(verbose_name="Telefon No")
    name = tables.LinkColumn(
        "exelusers_detail",  # Replace with your actual view name for evrak details
        text=lambda record: record.name,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
        verbose_name="Excel Kullanıcısı",
    )
    reactivate = TemplateColumn(verbose_name="Aktifleştir", template_name="exelusers_reactivate_button_column.html")

    class Meta:
        model = ExelUsers
        fields = ["name", "phonenumber"]
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"  # You can choose a different template if needed
        template_name = "django_tables2/bootstrap5-responsive.html"


class TagTable(tables.Table):
    name = tables.LinkColumn(
        "tagdetail_view_name",
        verbose_name="Harcama Kalemi İsmi",
        text=lambda record: record.name,
        args=[tables.A("slug")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )

    class Meta:
        model = Tag
        per_page = 10  # Number of items to display per page
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ["name"]


class DeletedTagTable(tables.Table):
    name = tables.LinkColumn(
        "tagdetail_view_name",
        verbose_name="Harcama Kalemi İsmi",
        text=lambda record: record.name,
        args=[tables.A("slug")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )
    reactivate = TemplateColumn(verbose_name="Aktifleştir", template_name="tag_reactivate_button_column.html")

    class Meta:
        model = Tag
        per_page = 10  # Number of items to display per page
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ["name"]


import django_tables2 as tables
from .models import MuGroup


class GroupTable(tables.Table):
    name = tables.LinkColumn(
        "groupdetail_view_name",
        verbose_name="Grup İsmi",
        text=lambda record: record.name,
        args=[tables.A("pk")],  # Pass the MuGroup's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )

    # Define columns for each permission field in Yetkiler model
    can_read_can_kullanicilar = tables.BooleanColumn(verbose_name="Okuma- Kullanıcılar")
    can_read_kullanici_gruplari = tables.BooleanColumn(verbose_name="Kullanıcı Grupları")
    can_read_excel_kullanici_yukleme = tables.BooleanColumn(verbose_name="Okuma- Excel Kullanıcı Yükleme")
    can_read_excel_kullanicilari = tables.BooleanColumn(verbose_name="Okuma- Excel Kullanıcıları")
    can_read_bakiye = tables.BooleanColumn(verbose_name="Okuma- Bakiye")
    can_read_harcama_kalemi = tables.BooleanColumn(verbose_name="Okuma- Harcama Kalemi")
    can_read_para_birimleri = tables.BooleanColumn(verbose_name="Okuma- Para Birimleri")
    can_read_Islemler = tables.BooleanColumn(verbose_name="Okuma- İşlemler")
    can_read_etkinlikler = tables.BooleanColumn(verbose_name="Okuma- Etkinlikler")
    can_read_evraklar = tables.BooleanColumn(verbose_name="Okuma- Evraklar")
    can_read_aylikharcamalar = tables.BooleanColumn(verbose_name="Okuma- Aylık Harcamalar")
    can_read_aylikispatliharcamalar = tables.BooleanColumn(verbose_name="Okuma- Aylık İspatlı Harcamalar")
    can_read_smsyonetimi = tables.BooleanColumn(verbose_name="Okuma- SMS Yönetimi")
    can_read_mobileapplinkleri = tables.BooleanColumn(verbose_name="Okuma- Mobile App Linkleri")

    can_write_can_kullanicilar = tables.BooleanColumn(verbose_name="Yazma- Kullancılar")
    can_write_kullanici_gruplari = tables.BooleanColumn(verbose_name="Yazma- Kullanıcı Grupları")
    can_write_excel_kullanici_yukleme = tables.BooleanColumn(verbose_name="Yazma- Excel Kullanıcı Yükleme")
    can_write_excel_kullanicilari = tables.BooleanColumn(verbose_name="Yazma- Excel Kullanıcıları")
    can_write_bakiye = tables.BooleanColumn(verbose_name="Yazma- Bakiye")
    can_write_harcama_kalemi = tables.BooleanColumn(verbose_name="Yazma- Harcama Kalemi")
    can_write_para_birimleri = tables.BooleanColumn(verbose_name="Yazma- Para Birimleri")
    can_write_Islemler = tables.BooleanColumn(verbose_name="Yazma- İslemler")
    can_write_etkinlikler = tables.BooleanColumn(verbose_name="Yazma- Etkinlikler")
    can_write_evraklar = tables.BooleanColumn(verbose_name="Yazma- Evraklar")
    can_write_aylikharcamalar = tables.BooleanColumn(verbose_name="Yazma- Aylık Harcamalar")
    can_write_aylikispatliharcamalar = tables.BooleanColumn(verbose_name="Yazma- Aylık İspatlı Harcamalar")
    can_write_smsyonetimi = tables.BooleanColumn(verbose_name="Yazma- SMS Yönetimi")
    can_write_mobileapplinkleri = tables.BooleanColumn(verbose_name="Yazma- Mobile App Linkleri")

    class Meta:
        model = MuGroup
        per_page = 10  # Number of items to display per page
        attrs = {"class": "table table-striped table-bordered"}
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = [
            "name",
            "can_read_can_kullanicilar",
            "can_read_kullanici_gruplari",
            "can_read_excel_kullanici_yukleme",
            "can_read_excel_kullanicilari",
            "can_read_bakiye",
            "can_read_harcama_kalemi",
            "can_read_para_birimleri",
            "can_read_Islemler",
            "can_read_etkinlikler",
            "can_read_evraklar",
            "can_read_aylikharcamalar",
            "can_read_aylikispatliharcamalar",
            "can_read_smsyonetimi",
            "can_read_mobileapplinkleri",
            "can_write_can_kullanicilar",
            "can_write_kullanici_gruplari",
            "can_write_excel_kullanici_yukleme",
            "can_write_excel_kullanicilari",
            "can_write_bakiye",
            "can_write_harcama_kalemi",
            "can_write_para_birimleri",
            "can_write_Islemler",
            "can_write_etkinlikler",
            "can_write_evraklar",
            "can_write_aylikharcamalar",
            "can_write_aylikispatliharcamalar",
            "can_write_smsyonetimi",
            "can_write_mobileapplinkleri",
        ]


from django_tables2 import TemplateColumn


class DeletedGroupTable(tables.Table):
    name = tables.LinkColumn(
        "groupdetail_view_name",
        verbose_name="Grup İsmi",
        text=lambda record: record.name,
        args=[tables.A("pk")],  # Pass the MuGroup's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )
    reactivate = TemplateColumn(verbose_name="Aktifleştir", template_name="group_reactivate_button_column.html")

    # Define columns for each permission field in Yetkiler model
    can_read_can_kullanicilar = tables.BooleanColumn(verbose_name="Okuma- Kullanıcılar")
    can_read_kullanici_gruplari = tables.BooleanColumn(verbose_name="Kullanıcı Grupları")
    can_read_excel_kullanici_yukleme = tables.BooleanColumn(verbose_name="Okuma- Excel Kullanıcı Yükleme")
    can_read_excel_kullanicilari = tables.BooleanColumn(verbose_name="Okuma- Excel Kullanıcıları")
    can_read_bakiye = tables.BooleanColumn(verbose_name="Okuma- Bakiye")
    can_read_harcama_kalemi = tables.BooleanColumn(verbose_name="Okuma- Harcama Kalemi")
    can_read_para_birimleri = tables.BooleanColumn(verbose_name="Okuma- Para Birimleri")
    can_read_Islemler = tables.BooleanColumn(verbose_name="Okuma- İşlemler")
    can_read_etkinlikler = tables.BooleanColumn(verbose_name="Okuma- Etkinlikler")
    can_read_evraklar = tables.BooleanColumn(verbose_name="Okuma- Evraklar")
    can_read_aylikharcamalar = tables.BooleanColumn(verbose_name="Okuma- Aylık Harcamalar")
    can_read_aylikispatliharcamalar = tables.BooleanColumn(verbose_name="Okuma- Aylık İspatlı Harcamalar")
    can_read_smsyonetimi = tables.BooleanColumn(verbose_name="Okuma- SMS Yönetimi")
    can_read_mobileapplinkleri = tables.BooleanColumn(verbose_name="Okuma- Mobile App Linkleri")

    can_write_can_kullanicilar = tables.BooleanColumn(verbose_name="Yazma- Kullancılar")
    can_write_kullanici_gruplari = tables.BooleanColumn(verbose_name="Yazma- Kullanıcı Grupları")
    can_write_excel_kullanici_yukleme = tables.BooleanColumn(verbose_name="Yazma- Excel Kullanıcı Yükleme")
    can_write_excel_kullanicilari = tables.BooleanColumn(verbose_name="Yazma- Excel Kullanıcıları")
    can_write_bakiye = tables.BooleanColumn(verbose_name="Yazma- Bakiye")
    can_write_harcama_kalemi = tables.BooleanColumn(verbose_name="Yazma- Harcama Kalemi")
    can_write_para_birimleri = tables.BooleanColumn(verbose_name="Yazma- Para Birimleri")
    can_write_Islemler = tables.BooleanColumn(verbose_name="Yazma- İslemler")
    can_write_etkinlikler = tables.BooleanColumn(verbose_name="Yazma- Etkinlikler")
    can_write_evraklar = tables.BooleanColumn(verbose_name="Yazma- Evraklar")
    can_write_aylikharcamalar = tables.BooleanColumn(verbose_name="Yazma- Aylık Harcamalar")
    can_write_aylikispatliharcamalar = tables.BooleanColumn(verbose_name="Yazma- Aylık İspatlı Harcamalar")
    can_write_smsyonetimi = tables.BooleanColumn(verbose_name="Yazma- SMS Yönetimi")
    can_write_mobileapplinkleri = tables.BooleanColumn(verbose_name="Yazma- Mobile App Linkleri")

    class Meta:
        model = MuGroup
        per_page = 10  # Number of items to display per page
        attrs = {"class": "table table-striped table-bordered"}
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = [
            "name",
            "can_read_can_kullanicilar",
            "can_read_kullanici_gruplari",
            "can_read_excel_kullanici_yukleme",
            "can_read_excel_kullanicilari",
            "can_read_bakiye",
            "can_read_harcama_kalemi",
            "can_read_para_birimleri",
            "can_read_Islemler",
            "can_read_etkinlikler",
            "can_read_evraklar",
            "can_read_aylikharcamalar",
            "can_read_aylikispatliharcamalar",
            "can_read_smsyonetimi",
            "can_read_mobileapplinkleri",
            "can_write_can_kullanicilar",
            "can_write_kullanici_gruplari",
            "can_write_excel_kullanici_yukleme",
            "can_write_excel_kullanicilari",
            "can_write_bakiye",
            "can_write_harcama_kalemi",
            "can_write_para_birimleri",
            "can_write_Islemler",
            "can_write_etkinlikler",
            "can_write_evraklar",
            "can_write_aylikharcamalar",
            "can_write_aylikispatliharcamalar",
            "can_write_smsyonetimi",
            "can_write_mobileapplinkleri",
        ]


# class GroupTable(tables.Table):
#     name = tables.LinkColumn(
#         "groupdetail_view_name",
#         verbose_name="Grup İsmi",
#         text=lambda record: record.name,
#         args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
#         attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
#     )

#     class Meta:
#         model = MuGroup
#         per_page = 10  # Number of items to display per page
#         attrs = {"class": "table table-striped table-bordered"}
#         # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
#         template_name = "django_tables2/bootstrap5-responsive.html"
#         fields = ["name", "can_write", "can_delete"]


class MuUserTable(tables.Table):
    username = tables.LinkColumn(
        "userupdate_view_name",
        verbose_name="Kullanıcı",
        text=lambda record: record.username,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )
    first_name = tables.Column(verbose_name="Ad Soyad")

    class Meta:
        model = MuUser
        per_page = 10  # Number of items to display per page
        attrs = {"class": "table table-striped table-bordered"}
        # template_name = "app_base/unsorted/django_tables_custom_bulma.html"
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ["username", "first_name"]


# class DeletedMuUserTable(tables.Table):
#     username = tables.LinkColumn(
#         "userupdate_view_name",
#         verbose_name="Kullanıcı",
#         text=lambda record: record.username,
#         args=[tables.A("pk")],
#         attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},
#     )
#     first_name = tables.Column(verbose_name="Ad Soyad")
#     reactivate_button = tables.TemplateColumn(
#         '<button type="button" class="btn btn-primary reactivate-btn" data-id="{{ record.pk }}">Reactivate</button>',
#         verbose_name="Reactivate",
#     )

#     class Meta:
#         model = MuUser
#         per_page = 10
#         attrs = {"class": "table table-striped table-bordered"}
#         template_name = "django_tables2/bootstrap5-responsive.html"
#         fields = ["username", "first_name"]

# tables.py
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_tables2 import TemplateColumn
from .models import MuUser


class ReactivateUserForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)


class DeletedMuUserTable(tables.Table):
    username = tables.LinkColumn(
        "userupdate_view_name",
        verbose_name="Kullanıcı",
        text=lambda record: record.username,
        args=[tables.A("pk")],  # Pass the evrak's primary key as an argument to the view
        attrs={"a": {"class": "etkinlik-name-link"}, "td": {"class": "long-text"}},  # Add any additional classes or attributes
    )
    first_name = tables.Column(verbose_name="Ad Soyad")
    reactivate = TemplateColumn(verbose_name="Aktifleştir", template_name="reactivate_button_column.html")

    class Meta:
        model = MuUser
        per_page = 10
        attrs = {"class": "table table-striped table-bordered"}
        template_name = "django_tables2/bootstrap5-responsive.html"
        fields = ["username", "first_name"]
