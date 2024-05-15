from django.contrib import admin
from django.contrib.auth.models import Group
from .models import MuUser, Islemler, MuGroup, Tag, EvrakModel, EtkinlikModel, ExelUsers, MobileFile, Yetkiler
from import_export.admin import ImportExportModelAdmin


class CustomUserAdmin(admin.ModelAdmin):
    # list_display = ("username", "email", "first_name", "last_name", "is_staff", "date_joined")
    # list_display = [field.name for field in MuUser._meta.fields if not field.many_to_many]
    list_display = [field.name for field in MuUser._meta.fields if not (field.many_to_many or field.name == "password")]
    # list_display = ["__str__"]
    list_filter = ("is_staff", "is_superuser", "groups")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    def display_password(self, obj):
        return "Hidden"  # You can customize the placeholder text

    display_password.short_description = "Password"


# //------------------------~~--------------------------------------------------------------------------
admin.site.unregister(Group)  # no offical support for AUTH_GROUP_MODEL = 'your_app.MyGroup' unlike AUTH_USER_MODEL
# //------------------------~~--------------------------------------------------------------------------
admin.site.register(MuUser, CustomUserAdmin)
admin.site.register(Islemler)
admin.site.register(MuGroup)
admin.site.register(Tag)
admin.site.register(EvrakModel)
admin.site.register(EtkinlikModel)
admin.site.register(MobileFile)
admin.site.register(Yetkiler)

from import_export.results import RowResult
from import_export.results import RowResult
from import_export import resources


class MyResource(resources.ModelResource):
    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(MyResource, self).import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [row[val] for val in row]
            # Add a column with the error message
            import_result.diff.append("Errors: {}".format([err.error for err in import_result.errors]))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result

    class Meta:
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        model = ExelUsers


@admin.register(ExelUsers)
class MyModelAdmin(ImportExportModelAdmin):
    resource_class = MyResource


# @admin.register(ExelUsers)
# class userdat(ImportExportModelAdmin):
#     pass
