from django.contrib import admin
from apps.catalog import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'description', 'ext_related_id')
    search_fields = ('name', 'description')
    list_filter = ('parent',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class CatalogMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'created_at', 'ttl')
    search_fields = ('name', 'seller__username')
    list_filter = ('seller', 'ttl')

class CatalogDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku', 'name', 'price', 'catalog')
    search_fields = ('sku', 'name')
    list_filter = ('catalog',)

class CatalogDetailImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'itemdetail', 'image')
    search_fields = ('itemdetail__sku',)

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.CatalogMaster, CatalogMasterAdmin)
admin.site.register(models.CatalogDetail, CatalogDetailAdmin)
admin.site.register(models.CatalogDetailImage, CatalogDetailImageAdmin)
