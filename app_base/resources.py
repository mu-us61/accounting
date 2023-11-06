from import_export import resources
from .models import ExelUsers
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError


class ExelUsersResource(resources.ModelResource):
    class Meta:
        model = ExelUsers

    # def skip_row(self, instance, original, row, import_validation_errors=None):
    #     # Extract the value of the "phonenumber" field from the row
    #     phonenumber_value = row.get("phonenumber")

    #     try:
    #         # Attempt to validate the phone number field
    #         PhoneNumberField().clean(phonenumber_value)
    #     except ValidationError as e:
    #         # If a validation error is raised, skip the row
    #         return True

    #     # If the phone number is valid, do not skip the row
    #     return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)
