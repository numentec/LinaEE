from django.contrib import admin
from apps.linabi import models

class BIFavoritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'todos')


admin.site.register(models.BIFavorito, BIFavoritoAdmin)