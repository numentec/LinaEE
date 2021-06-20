from django.contrib import admin
from apps.linabi import models

class BIFavoritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'todos')

class BIXLSXTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class BIXLSXTemplateColAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ordinal', 'plantilla')

admin.site.register(models.BIFavorito, BIFavoritoAdmin)
admin.site.register(models.BIXLSXTemplate, BIXLSXTemplateAdmin)
admin.site.register(models.BIXLSXTemplateCol, BIXLSXTemplateColAdmin)