from rest_framework import serializers
from .models import SMTPConfig, EmailTemplate, EmailCampaign, EmailRecipient, CampaignLog


class SMTPConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfig
        fields = ['id', 'name', 'host', 'port', 'use_tls', 'use_ssl',
                  'username', 'password', 'from_name', 'from_email', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SMTPConfigListSerializer(SMTPConfigSerializer):
    class Meta(SMTPConfigSerializer.Meta):
        fields = ['id', 'name', 'host', 'port', 'from_email', 'from_name', 'is_default', 'created_at']


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'subject', 'html_body', 'text_body', 'variables', 'created_at', 'updated_at']
        read_only_fields = ['id', 'variables', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class EmailRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailRecipient
        fields = ['id', 'email', 'variables', 'status', 'sent_at', 'error_message']
        read_only_fields = ['id', 'status', 'sent_at', 'error_message']


class CampaignLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignLog
        fields = ['id', 'level', 'message', 'created_at']


class EmailCampaignSerializer(serializers.ModelSerializer):
    template_name = serializers.SerializerMethodField()
    smtp_name = serializers.SerializerMethodField()
    progress_pct = serializers.ReadOnlyField()

    class Meta:
        model = EmailCampaign
        fields = [
            'id', 'name', 'template', 'template_name', 'smtp_config', 'smtp_name',
            'status', 'batch_size', 'delay_seconds',
            'total_recipients', 'sent_count', 'failed_count', 'progress_pct',
            'started_at', 'completed_at', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'status', 'total_recipients', 'sent_count', 'failed_count',
                            'started_at', 'completed_at', 'created_at', 'updated_at']

    def get_template_name(self, obj):
        return obj.template.name if obj.template else '—'

    def get_smtp_name(self, obj):
        return obj.smtp_config.name if obj.smtp_config else '—'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
