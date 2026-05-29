from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Module, ModulePermission, LicenseConfig


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


@admin.register(LicenseConfig)
class LicenseConfigAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'expiration_date', 'estado_licencia', 'dias_restantes', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'estado_licencia', 'dias_restantes')
    fields = ('client_name', 'expiration_date', 'notes', 'estado_licencia', 'dias_restantes', 'created_at', 'updated_at')

    # Solo puede existir UN registro de licencia
    def has_add_permission(self, request):
        return not LicenseConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # No se puede eliminar desde admin

    @admin.display(description='Estado')
    def estado_licencia(self, obj):
        if obj.is_expired:
            return format_html(
                '<span style="color:#fff;background:#c53030;padding:3px 10px;border-radius:12px;font-weight:700;font-size:12px;">● VENCIDA</span>'
            )
        days = obj.days_remaining
        if days <= 30:
            color = '#d97706'  # amarillo/naranja — próximo a vencer
        else:
            color = '#16a34a'  # verde — activa
        return format_html(
            '<span style="color:#fff;background:{};padding:3px 10px;border-radius:12px;font-weight:700;font-size:12px;">● ACTIVA</span>',
            color,
        )

    @admin.display(description='Días restantes')
    def dias_restantes(self, obj):
        days = obj.days_remaining
        if days < 0:
            return format_html('<b style="color:#c53030;">Vencida hace {} día(s)</b>', abs(days))
        if days <= 30:
            return format_html('<b style="color:#d97706;">{} día(s)</b>', days)
        return format_html('<span style="color:#16a34a;">{} días</span>', days)
