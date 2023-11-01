# resources.py
from import_export import resources
from .models import ExelUsers


class ExelUsersResource(resources.ModelResource):
    class Meta:
        model = ExelUsers
