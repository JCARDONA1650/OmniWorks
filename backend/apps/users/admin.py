from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('first_name',)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('OmniWorks', {'fields': ('role', 'avatar')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('OmniWorks', {'fields': ('email', 'first_name', 'last_name', 'role')}),
    )
