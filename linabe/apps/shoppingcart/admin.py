from django.contrib import admin
from apps.shoppingcart import models

# Register your models here.
class ExtOrderMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'created_by', 'source', 'customer_name', 'total')

class ExtOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'extorder', 'sku', 'name', 'quantity', 'price', 'total')


admin.site.register(models.ExtOrderMaster, ExtOrderMasterAdmin)
admin.site.register(models.ExtOrderItem, ExtOrderItemAdmin)