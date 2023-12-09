from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import CurrencyListView, CurrencyCreateView, CurrencyUpdateView, CurrencyDeleteView, TransactionUpdateView, CurrencyListMaskedView


urlpatterns = [
    # //------------------------~~--------------------------------------------------------------------------
    path("", views.home_view, name="home_view_name"),
    # //------------------------~~--------------------------------------------------------------------------
    path("login/", views.login_view, name="login_view_name"),
    path("logout/", views.logout_view, name="logout_view_name"),
    path("passwordchange/", views.passwordchange_view, name="passwordchange_view_name"),
    # //------------------------~~--------------------------------------------------------------------------
    path("balance/", views.balance_view, name="balance_view_name"),
    # path("balance/", views.BalanceListView.as_view(), name="balance_view_name"),
    # path("balance/", views.BalanceTableView.as_view(), name="balance_view_name"),
    # //------------------------~~--------------------------------------------------------------------------
    path("grouplist/", views.grouplist_view, name="grouplist_view_name"),
    path("grouplistmasked/", views.grouplistmasked_view, name="grouplistmasked_view_name"),
    path("groupcreate/", views.groupcreate_view, name="groupcreate_view_name"),
    path("groupdetail/<int:group_id>/", views.groupdetail_view, name="groupdetail_view_name"),
    path("user-autocomplete/", views.user_autocomplete, name="user_autocomplete"),
    path("group/<int:group_id>/update/", views.groupupdate_view, name="groupupdate_view_name"),
    path("group/<int:group_id>/delete/", views.groupdelete_view, name="groupdelete_view_name"),
    # //------------------------~~--------------------------------------------------------------------------
    path("userlist/", views.userlist_view, name="userlist_view_name"),
    path("userlistmasked/", views.userlistmasked_view, name="userlistmasked_view_name"),
    path("user/create/", views.usercreate_view, name="usercreate_view_name"),
    path("user/<int:pk>/update/", views.userupdate_view, name="userupdate_view_name"),
    path("user/<int:pk>/delete/", views.userdelete_view, name="userdelete_view_name"),
    # //----------------------------------------------------------------------------------------------------
    # Transaction URLs
    path("transactionlist/", views.TransactionListView.as_view(), name="transactionlist_view_name"),  # kisisel islemler
    path("transaction/create/", views.TransactionCreateView.as_view(), name="transactioncreate_view_name"),
    path("transaction/<int:pk>/", views.TransactionDetailView.as_view(), name="transactiondetail_view_name"),
    path("transaction/p/<int:pk>/", views.TransactionPuplicDetailView.as_view(), name="transactionpublicdetail_view_name"),
    path("transaction/<int:pk>/update/", views.TransactionUpdateView.as_view(), name="transactionupdate_view_name"),
    path("transaction/<int:pk>/delete/", views.TransactionDeleteView.as_view(), name="transactiondelete_view_name"),
    # path("transactions/table/", views.TransactionTable.as_view(), name="transaction_table_name"),
    # path("transactions/bigtable/", views.FilteredTableListView.as_view(), name="transaction_bigtable_name"),
    path("transactions/bigtable/", views.TransactionTableView.as_view(), name="transactiontable_view_name"),
    path("transactions/bigtablemasked/", views.TransactionTableMaskedView.as_view(), name="transactiontablemasked_view_name"),
    # //-------------------------------------------------~~-------------------------------------------------
    path("taglist/", views.taglist_view, name="taglist_view_name"),
    path("taglistmasked/", views.taglistmasked_view, name="taglistmasked_view_name"),
    path("tag/create/", views.tagcreate_view, name="tagcreate_view_name"),
    path("tag/<slug:slug>/", views.tagdetail_view, name="tagdetail_view_name"),
    path("tag/<slug:slug>/update/", views.tagupdate_view, name="tagupdate_view_name"),
    path("tag/<slug:slug>/delete/", views.tagdelete_view, name="tagdelete_view_name"),
    # //-------------------------------------------------~~-------------------------------------------------
    path("monthlyspendings", views.monthlyspendings_view, name="monthlyspendings_view_name"),
    # path("proventags", views.ProvenTagsView.as_view(), name="proventags_view_name"),
    path("proventags", views.proventags_view, name="proventags_view_name"),
    path("uploadexel/", views.upload_excel_view, name="upload_exel_view_name"),
    path("mobile/", views.mobile_view, name="mobile_view_name"),
    path("downloadmobile/<path:file_path>/", views.downloadmobile, name="downloadmobile"),
    # //------------------------~~--------------------------------------------------------------------------
    path("currencylist/", CurrencyListView.as_view(), name="currencylist_view_name"),
    path("currencylistmasked/", CurrencyListMaskedView.as_view(), name="currencylistmasked_view_name"),
    path("currency/create/", CurrencyCreateView.as_view(), name="currencycreate_view_name"),
    path("currency/update/<int:pk>/", CurrencyUpdateView.as_view(), name="currencyupdate_view_name"),
    path("currency/delete/<int:pk>/", CurrencyDeleteView.as_view(), name="currencydelete_view_name"),
    # //------------------------~~--------------------------------------------------------------------------
    path("evrak/create/", views.EvrakCreateView.as_view(), name="evrak_create"),
    path("evrak/list/", views.EvrakListView.as_view(), name="evrak_list"),
    path("evrak/silinenlerlist/", views.EvrakSilinenlerListView.as_view(), name="evrak_silinenler_list"),
    path("evrak/update/<int:pk>/", views.EvrakUpdateView.as_view(), name="evrak_update"),
    path("evrak/delete/<int:pk>/", views.EvrakDeleteView.as_view(), name="evrak_delete"),
    path("evrak/detail/<int:pk>/", views.EvrakDetailView.as_view(), name="evrak_detail"),
    # //------------------------~~--------------------------------------------------------------------------
    path("etkinlik/create/", views.EtkinlikCreateView.as_view(), name="etkinlik_create"),
    path("etkinlik/list/", views.EtkinlikListView.as_view(), name="etkinlik_list"),
    path("etkinlik/listmasked/", views.EtkinlikListMaskedView.as_view(), name="etkinlik_listmasked"),
    path("etkinlik/update/<int:pk>/", views.EtkinlikUpdateView.as_view(), name="etkinlik_update"),
    path("etkinlik/delete/<int:pk>/", views.EtkinlikDeleteView.as_view(), name="etkinlik_delete"),
    path("etkinlik/detail/<int:pk>/", views.EtkinlikDetailView.as_view(), name="etkinlik_detail"),
    # //------------------------~~--------------------------------------------------------------------------
    path("exelusers/create/", views.ExelUsersCreateView.as_view(), name="exelusers_create"),
    # path("exelusers/list/", views.ExelUsersListView.as_view(), name="exelusers_list"),
    path("exelusers/list/", views.exelusers_list, name="exelusers_list"),
    path("exelusers/listmasked/", views.exelusers_listmasked, name="exelusers_listmasked"),
    path("exelusers/update/<int:pk>/", views.ExelUsersUpdateView.as_view(), name="exelusers_update"),
    path("exelusers/delete/<int:pk>/", views.ExelUsersDeleteView.as_view(), name="exelusers_delete"),
    path("exelusers/detail/<int:pk>/", views.ExelUsersDetailView.as_view(), name="exelusers_detail"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
