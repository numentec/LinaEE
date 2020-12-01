from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.core import models
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']


class CiaAdmin(admin.ModelAdmin):
     list_display = ('id', 'codigo', 'nombre', 'ruc')


class UserAdminx(UserAdmin):
    """User admin."""

    list_display = ('pk', 'username', 'email',)
    list_display_links = ('pk', 'username', 'email',)

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


class GenSecAdmin(admin.ModelAdmin):
     list_display = ('id', 'nombre', 'conteo', 'obs')


class TipoGenAdmin(admin.ModelAdmin):
     list_display = ('id', 'idgenerico', 'descripcion')


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


admin.site.register(models.Cia, CiaAdmin)
admin.site.register(models.User, UserAdminx)
admin.site.register(models.GenSequence, GenSecAdmin)
admin.site.register(models.TipoGenerico, TipoGenAdmin)
admin.site.register(models.StakeHolder, StakeHolderAdmin)
