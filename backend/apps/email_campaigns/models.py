import re
from django.db import models
from django.conf import settings

VARIABLE_RE = re.compile(r'\{\{(\s*[\w\s]+\s*)\}\}')


class SMTPConfig(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='smtp_configs')
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=200)
    port = models.PositiveIntegerField(default=587)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    from_name = models.CharField(max_length=100, blank=True)
    from_email = models.EmailField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'smtp_configs'
        verbose_name = 'Configuración SMTP'
        verbose_name_plural = 'Configuraciones SMTP'

    def __str__(self):
        return f'{self.name} ({self.from_email})'

    def save(self, *args, **kwargs):
        if self.is_default:
            SMTPConfig.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class EmailTemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_templates')
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=500)
    html_body = models.TextField()
    text_body = models.TextField(blank=True)
    variables = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_templates'
        ordering = ['-updated_at']
        verbose_name = 'Plantilla de correo'
        verbose_name_plural = 'Plantillas de correo'

    def __str__(self):
        return self.name

    def extract_variables(self):
        found = set(VARIABLE_RE.findall(self.subject))
        found |= set(VARIABLE_RE.findall(self.html_body))
        self.variables = sorted(v.strip() for v in found)

    def save(self, *args, **kwargs):
        self.extract_variables()
        super().save(*args, **kwargs)


class EmailCampaign(models.Model):
    class Status(models.TextChoices):
        DRAFT      = 'draft',      'Borrador'
        READY      = 'ready',      'Lista'
        RUNNING    = 'running',    'Enviando'
        PAUSED     = 'paused',     'Pausada'
        COMPLETED  = 'completed',  'Completada'
        ERROR      = 'error',      'Error'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='email_campaigns')
    name = models.CharField(max_length=200)
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    smtp_config = models.ForeignKey(SMTPConfig, on_delete=models.SET_NULL, null=True, related_name='campaigns')
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    batch_size = models.PositiveIntegerField(default=10, help_text='Correos por lote')
    delay_seconds = models.PositiveIntegerField(default=5, help_text='Segundos de pausa entre lotes')
    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'email_campaigns'
        ordering = ['-created_at']
        verbose_name = 'Campaña de correo'
        verbose_name_plural = 'Campañas de correo'

    def __str__(self):
        return f'{self.name} [{self.get_status_display()}]'

    @property
    def progress_pct(self):
        if not self.total_recipients:
            return 0
        return round(((self.sent_count + self.failed_count) / self.total_recipients) * 100)


class EmailRecipient(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        SENT    = 'sent',    'Enviado'
        FAILED  = 'failed',  'Error'

    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='recipients')
    email = models.EmailField()
    variables = models.JSONField(default=dict)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = 'email_recipients'
        ordering = ['id']
        verbose_name = 'Destinatario'
        verbose_name_plural = 'Destinatarios'

    def __str__(self):
        return f'{self.email} ({self.get_status_display()})'


class CampaignLog(models.Model):
    class Level(models.TextChoices):
        INFO    = 'info',    'Info'
        SUCCESS = 'success', 'Éxito'
        WARNING = 'warning', 'Advertencia'
        ERROR   = 'error',   'Error'

    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE, related_name='logs')
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'campaign_logs'
        ordering = ['-created_at']
        verbose_name = 'Log de campaña'
        verbose_name_plural = 'Logs de campaña'

    def __str__(self):
        return f'[{self.level}] {self.message[:60]}'
