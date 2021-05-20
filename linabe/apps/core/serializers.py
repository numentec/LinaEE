from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from apps.core import models
from .utils import DynamicFieldSerializer

LinaUserModel = get_user_model()

class CommonSerializer(serializers.ModelSerializer):
    """Ensure the fields are included in the models."""

    common_fields = ['is_active', 'created_by', 'created_at', 'modified_by', 'modified_at']


class ListIntSerializer(serializers.ListField):
    child = serializers.IntegerField()


class GroupsSerializer(serializers.ModelSerializer):
    """Lista de Grupos del Sistema"""

    class Meta:
        model = Group
        fields = ('id', 'name')


class CiaSerializer(DynamicFieldSerializer):

    class Meta:
        model = models.Cia
        fields = ('__all__')


class StakeHolderSerializer(DynamicFieldSerializer):

    class Meta:
        model = models.StakeHolder
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = LinaUserModel
        fields = ('__all__')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
        read_only_fields = ('id', 'username', 'modified_at', 'groups', 'foto', 'date_joined')

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

class ProfileSerializer(serializers.ModelSerializer):
    
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = LinaUserModel
        fields = ('__all__')
        read_only_fields = (
            'id',
            'username',
            'password',
            'modified_at',
            'groups',
            'foto',
            'date_joined',
            'last_login',
            'user_permissions',
            'is_superuser',
            'is_staff',
        )

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

class UserFotoSerializer(serializers.ModelSerializer):
    """Serializer para carga de foto de perfil"""

    class Meta:
        model = LinaUserModel
        fields = ('id', 'foto')
        read_only_fields = ('id',)


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

        all_permissions = LinaUserModel(is_superuser=True).get_all_permissions()
        user_permissions = obj.get_all_permissions()

        return {p: p in user_permissions for p in persmin}

    def get_fullname(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinaUserModel
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'groups')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        groups_list = validated_data.pop('groups')
        registered_user = LinaUserModel(**validated_data)
        registered_user.set_password(password)
        registered_user.save()
        registered_user.groups.set(groups_list)
        return registered_user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = LinaUserModel
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class VistaConfigUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VistaConfig
        fields = ('id', 'user', 'vista',
        'configkey', 'configval1', 'configval2', 'configval3', 'configval4',
        'configval5', 'configval6', 'configval7', 'configval8', 'configval9', 'tipo')


class VistaConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.VistaConfig
        fields = ('id', 'vista', 
        'configkey', 'configval1', 'configval2', 'configval3', 'configval4',
        'configval5', 'configval6', 'configval7', 'configval8', 'configval9', 'tipo')


class VistaSerializer(serializers.ModelSerializer):

    configs_x_vista = VistaConfigSerializer(read_only=True, many=True)

    class Meta:
        model = models.Vista
        fields = ('id', 'nombre', 'descrip', 'link', 'tipo', 'configs_x_vista', 'modulo')


class ModuloSerializer(serializers.ModelSerializer):

    vistas_x_modulo = VistaSerializer(read_only=True, many=True)

    class Meta:
        model = models.Modulo
        fields = ('id', 'nombre', 'descrip', 'tipo', 'vistas_x_modulo')