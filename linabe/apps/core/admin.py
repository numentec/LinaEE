from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.core import models
from rest_framework.authtoken.admin import TokenAdmin


class UserAdminx(UserAdmin):
    """User admin."""

    list_display = ('pk', 'username', 'email', 'birth_date', 'foto')
    list_display_links = ('pk', 'username', 'email',)
    list_editable = ('birth_date', 'foto')

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    list_filter = (
        'is_active',
        'is_staff',
        'date_joined',
        'modified_at',
    )

    readonly_fields = ('date_joined', 'modified_at',)

TokenAdmin.raw_id_fields = ['user']


class CiaAdmin(admin.ModelAdmin):
     list_display = ('id', 'codigo', 'nombre', 'ruc')


class TipoGenAdmin(admin.ModelAdmin):
     list_display = ('id', 'idgenerico', 'descripcion')


class GenSecAdmin(admin.ModelAdmin):
     list_display = ('id', 'nombre', 'conteo', 'obs')


class ModuloAdmin(admin.ModelAdmin):
    """Modulos admin."""

    list_display = ('id', 'nombre', 'descrip', 'tipo', 'is_active')

    search_fields = (
        'id',
        'nombre',
    )

    list_filter = (
        'is_active',
        'tipo',
    )


class VistaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descrip', 'link', 'tipo', 'modulo', 'is_active')


class VistaConfigAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'vista',
        'configkey',
        'configval1',
        'configval2',
        'configval3',
        'configval4',
        'configval5',
        'configval6',
        'configval7',
        'configval8',
        'configval9',
        'tipo',
        'is_active'
    )
    readonly_fields = ('vista',)


class VistaConfigUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'vista',
        'configkey',
        'configval1',
        'configval2',
        'configval3',
        'configval4',
        'configval5',
        'configval6',
        'configval7',
        'configval8',
        'configval9',
        'tipo',
        'is_active'
    )
    readonly_fields = ('user', 'vista',)


class StakeHolderAdmin(admin.ModelAdmin):
    """StakeHolder admin"""

    list_display = ('id', 'codigo', 'nombre',)

    search_fields = (
        'id',
        'codigo',
        'nombre',
        'ruc',
        'is_cli',
        'is_pro',
        'is_ban',
        'is_soc',
        'foto',
        'is_active',
    )

    list_filter = (
        'nombre',
        'is_active',
        'is_cli',
        'is_pro',
        'is_ban',
        'is_soc',
    )

    readonly_fields = ('created_at', 'modified_at',)


admin.site.register(models.User, UserAdminx)
admin.site.register(models.Cia, CiaAdmin)
admin.site.register(models.TipoGenerico, TipoGenAdmin)
admin.site.register(models.GenSequence, GenSecAdmin)
admin.site.register(models.Modulo, ModuloAdmin)
admin.site.register(models.Vista, VistaAdmin)
admin.site.register(models.VistaConfig, VistaConfigAdmin)
admin.site.register(models.VistaConfigUser, VistaConfigUserAdmin)
admin.site.register(models.StakeHolder, StakeHolderAdmin)
