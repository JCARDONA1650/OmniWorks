from django.contrib import admin
from .models import SMTPConfig, EmailTemplate, EmailCampaign, EmailRecipient, CampaignLog


@admin.register(SMTPConfig)
class SMTPConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'host', 'port', 'from_email', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name', 'user__email', 'from_email')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'subject', 'updated_at')
    search_fields = ('name', 'subject', 'user__email')


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'total_recipients', 'sent_count', 'failed_count', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'user__email')
    readonly_fields = ('sent_count', 'failed_count', 'started_at', 'completed_at')


@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'campaign', 'status', 'sent_at')
    list_filter = ('status',)
    search_fields = ('email', 'campaign__name')


@admin.register(CampaignLog)
class CampaignLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'level', 'message', 'created_at')
    list_filter = ('level',)
    readonly_fields = ('created_at',)
