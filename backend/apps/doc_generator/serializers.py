from rest_framework import serializers
from .models import DocumentTemplate, DocumentGeneration


class DocumentTemplateSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    variable_count = serializers.SerializerMethodField()

    class Meta:
        model = DocumentTemplate
        fields = ['id', 'name', 'description', 'file', 'filename', 'variables',
                  'variable_count', 'is_active', 'created_at']
        read_only_fields = ['id', 'variables', 'created_at']

    def get_filename(self, obj):
        return obj.filename()

    def get_variable_count(self, obj):
        return len(obj.variables)


class DocumentGenerationSerializer(serializers.ModelSerializer):
    template_name = serializers.SerializerMethodField()
    progress_pct = serializers.SerializerMethodField()

    class Meta:
        model = DocumentGeneration
        fields = ['id', 'name', 'template', 'template_name', 'status',
                  'total_records', 'processed_records', 'progress_pct',
                  'error_message', 'created_at']
        read_only_fields = fields

    def get_template_name(self, obj):
        return obj.template.name if obj.template else '—'

    def get_progress_pct(self, obj):
        if not obj.total_records:
            return 0
        return round((obj.processed_records / obj.total_records) * 100)
