from rest_framework.permissions import (DjangoModelPermissions, SAFE_METHODS, BasePermission)

class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        # you need deepcopy when you inherit a dictionary type
        # self.perms_map = copy.deepcopy(self.perms_map)  
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class IsSuperUserOrReadOnly(BasePermission):
    """Permite lectura a cualquier usuario autenticado; escritura solo a superusuarios."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_superuser)