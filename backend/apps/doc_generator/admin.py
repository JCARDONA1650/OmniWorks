from django.contrib import admin
from .models import DocumentTemplate, DocumentGeneration


@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'variable_count', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'user__email')

    def variable_count(self, obj):
        return len(obj.variables)
    variable_count.short_description = 'Variables'


@admin.register(DocumentGeneration)
class DocumentGenerationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'status', 'processed_records', 'total_records', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at',)
