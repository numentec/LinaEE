from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.core import models


class CiaAdmin(admin.ModelAdmin):
     list_display = ('id', 'codigo', 'nombre', 'ruc')

#@admin.register(User)
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


admin.site.register(models.Cia, CiaAdmin)
admin.site.register(models.User, UserAdminx)