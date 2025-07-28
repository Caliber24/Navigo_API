from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_admin']
    list_filter = ['is_active', 'is_admin', 'notifications_enabled']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Other Settings'), {'fields': ('notifications_enabled',)}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )
