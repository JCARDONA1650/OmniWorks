from django.contrib import admin
from .models import Module, ModulePermission


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    ordering = ('order',)


@admin.register(ModulePermission)
class ModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'is_enabled')
    list_filter = ('module', 'is_enabled')
    search_fields = ('user__email',)
