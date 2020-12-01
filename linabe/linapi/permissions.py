from rest_framework.permissions import (DjangoModelPermissions)

class CustomDjangoModelPermissions(DjangoModelPermissions):
    def __init__(self):
        # you need deepcopy when you inherit a dictionary type
        # self.perms_map = copy.deepcopy(self.perms_map)  
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']