from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view_name"),
    path("passchange", views.passchange_view, name="passchange_view_name"),
    path("login", views.login_view, name="login_view_name"),
    path("logout", views.logout_view, name="logout_view_name"),
    path("profile/", views.profile_view, name="profile_view_name"),
    path("bakiye", views.bakiye_view, name="bakiye_view_name"),
    path("usergroups", views.usergroups_view, name="usergroups_view_name"),
    path("groupdetail/<int:group_id>", views.groupdetail_view, name="groupdetail_view_name"),
    path("groupcreate", views.groupcreate_view, name="groupcreate_view_name"),
    path("users/", views.muuserlist_view, name="muuserlist_view_name"),
    path("users/create/", views.muusercreate_view, name="muusercreate_view_name"),
    path("users/<int:pk>/update/", views.muuserupdate_view, name="muuserupdate_view_name"),
    path("users/<int:pk>/delete/", views.muuserdelete_view, name="muuserdelete_view_name"),
    # //----------------------------------------------------------------------------------------------------
    # Transaction URLs
    path("transactions/", views.TransactionList.as_view(), name="transaction_list_name"),
    path("transactions/create/", views.CreateTransaction.as_view(), name="transaction_create_name"),
    path("transactions/<int:pk>/", views.TransactionDetail.as_view(), name="transaction_detail_name"),
    path("transactions/<int:pk>/edit/", views.UpdateTransaction.as_view(), name="transaction_edit_name"),
    path("transactions/<int:pk>/delete/", views.DeleteTransaction.as_view(), name="transaction_delete_name"),
    # //-------------------------------------------------~~-------------------------------------------------
    path("tag/", views.tag_list, name="tag_list_name"),
    path("tag/create/", views.tag_create, name="tag_create_name"),
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail_name"),
    path("tag/<slug:slug>/update/", views.tag_update, name="tag_update_name"),
    path("tag/<slug:slug>/delete/", views.tag_delete, name="tag_delete_name"),
    # //-------------------------------------------------~~-------------------------------------------------
    path("transactions/table/", views.TransactionTable.as_view(), name="transaction_table_name"),
    path("monthlyspendings", views.monthly_spendings, name="monthly_spendings_name"),
]
