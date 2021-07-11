from rest_framework.permissions import (BasePermission, DjangoModelPermissions)
from ipware import get_client_ip
from django.core.exceptions import PermissionDenied

class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        # you need deepcopy when you inherit a dictionary type
        # self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class ValidExternalAccess(BasePermission):
    
    def has_permission(self, request, view):
        client_ip, is_routable = get_client_ip(request)

        if client_ip is None:
            # Unable to get the client's IP address
            raise PermissionDenied("No se pudo comprobar la dirección de origen")
        else:
            # We got the client's IP address
            if is_routable:
                # The client's IP address is publicly routable on the Internet
                if request.user.has_perm('core.ext_acc'):
                    return True
                raise PermissionDenied("Solo puede acceder desde la Intranet")
            else:
                # The client's IP address is private
                return True