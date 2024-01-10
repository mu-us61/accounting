from django.http import HttpResponseForbidden


# class WritePermissionRequiredMixin:
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_write_permission(request.user):
#             return HttpResponseForbidden("You don't have permission to write.")

#         return super().dispatch(request, *args, **kwargs)

#     def has_write_permission(self, user):
#         groups_with_write_permission = user.gruplar.filter(can_write=True)
#         return groups_with_write_permission.exists()
#         # return False


# class DeletePermissionRequiredMixin:
#     def dispatch(self, request, *args, **kwargs):
#         if not self.has_delete_permission(request.user):
#             return HttpResponseForbidden("You don't have permission to delete.")

#         return super().dispatch(request, *args, **kwargs)

#     def has_delete_permission(self, user):
#         groups_with_delete_permission = user.gruplar.filter(can_delete=True)
#         return groups_with_delete_permission.exists()

from django.http import HttpResponseForbidden


# class PermissionRequiredMixin:
#     def has_permission(self, user):
#         raise NotImplementedError("Subclasses must implement this method.")

#     def dispatch(self, request, *args, **kwargs):
#         user = request.user
#         if not self.has_permission(user):
#             return HttpResponseForbidden("Silme Veya Duzenleme Yetkiniz Yok")

#         if hasattr(super(), "dispatch"):
#             # This is a class-based view
#             return super().dispatch(request, *args, **kwargs)
#         else:
#             # This is a function-based view
#             return self.view_func(request, *args, **kwargs)

#     def __call__(self, view_func):
#         # This method allows the mixin to be used as a decorator for function-based views
#         self.view_func = view_func
#         return self


# class WritePermissionRequiredMixin(PermissionRequiredMixin):
#     def has_permission(self, user):
#         groups_with_write_permission = user.gruplar.filter(can_write=True)
#         return groups_with_write_permission.exists()


# class DeletePermissionRequiredMixin(PermissionRequiredMixin):
#     def has_permission(self, user):
#         groups_with_delete_permission = user.gruplar.filter(can_delete=True)
#         return groups_with_delete_permission.exists()


from django.http import HttpResponseForbidden


class PermissionRequiredMixin:
    def has_permission(self, user):
        raise NotImplementedError("Subclasses must implement this method.")

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_staff:
            # Staff users have permission regardless of group criteria
            return super().dispatch(request, *args, **kwargs) if hasattr(super(), "dispatch") else self.view_func(request, *args, **kwargs)

        if not self.has_permission(user):
            return HttpResponseForbidden("You don't have permission.")

        return super().dispatch(request, *args, **kwargs) if hasattr(super(), "dispatch") else self.view_func(request, *args, **kwargs)

    def __call__(self, view_func):
        # This method allows the mixin to be used as a decorator for function-based views
        self.view_func = view_func
        return self


class WritePermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self, user):
        if user.is_staff:
            return True

        groups_with_write_permission = user.gruplar.filter(can_write=True)
        return groups_with_write_permission.exists()


class DeletePermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self, user):
        if user.is_staff:
            return True

        groups_with_delete_permission = user.gruplar.filter(can_delete=True)
        return groups_with_delete_permission.exists()
