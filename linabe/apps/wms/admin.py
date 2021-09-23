from django.contrib import admin
from apps.wms import models

class WMSQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link', 'owner')

admin.site.register(models.WMSQuery, WMSQueryAdmin)