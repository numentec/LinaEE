from django.contrib import admin
from apps.core import models


class CiaAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'nombre', 'ruc')


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'dni', 'nombre_corto')
    #readonly_fields = ('created', 'updated')

admin.site.register(models.Cia, CiaAdmin)
admin.site.register(models.Perfil, PerfilAdmin)