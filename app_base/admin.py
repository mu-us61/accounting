from django.contrib import admin
from django.contrib.auth.models import Group
from .models import MuUser, Islemler, MuGroup, Tag


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
