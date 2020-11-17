from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Cia, User

LinaUserModel = get_user_model()

class ListIntSerializer(serializers.ListField):
    child = serializers.IntegerField()


class GroupsSerializer(serializers.ModelSerializer):
    """Lista de Grupos del Sistema"""

    class Meta:
        model = Group
        fields = ('id', 'name')


class CiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cia
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = LinaUserModel
        fields = ('__all__')

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

# Devuelve el usuario actual con sus permisos
class UserPermsSerializer(serializers.ModelSerializer):

    perms = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = LinaUserModel
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

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinaUserModel
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'groups')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

