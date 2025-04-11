"""
Admin page code.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin page for the user models."""
    ordering = ['id']
    list_display = ['username', 'email', 'password']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']


admin.site.register(models.User, UserAdmin)
