from django.contrib import admin
from apps.saleapp import models

# Register your models here.
class ExtOrderMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'created_by', 'source', 'customer_name', 'total')

class ExtOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'extorder', 'sku', 'name', 'quantity', 'price', 'total')

class SaleAppSettingsAdmin(admin.ModelAdmin):
    list_display = ('company', 'email_policy', 'email_attachments', 'email_include_images', 'modified_at')


admin.site.register(models.ExtOrderMaster, ExtOrderMasterAdmin)
admin.site.register(models.ExtOrderItem, ExtOrderItemAdmin)
admin.site.register(models.SaleAppSettings, SaleAppSettingsAdmin)