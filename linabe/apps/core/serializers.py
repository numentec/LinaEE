from rest_framework import serializers
from .models import Cia, User


class CiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cia
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('__all__')


# Devuelve el usuario actual con sus permisos
class UserPermsSerializer(serializers.ModelSerializer):

    perms = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'fullname', 'perms')
        read_only_fields = ('id', 'username', 'email', 'first_name', 'last_name', 'fullname', 'perms')

    def get_perms(self, obj):

        persmin = [
            'core.view_linabi_module',
            'core.view_user',
            'core.view_accounting_module',
            'core.view_hr_module',
            'core.view_cia',
            'core.add_cia',
            'core.view_purchase_module',
            'core.view_sys_module',
            'core.view_crm_module',
            'core.view_inv_module',
            'core.view_logistics_module',
            'core.view_sales_module'
            ]

        all_permissions = User(is_superuser=True).get_all_permissions()
        user_permissions = obj.get_all_permissions()

        return {p: p in user_permissions for p in persmin}

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)