import os
from django.db import models
from django.conf import settings


def template_upload_path(instance, filename):
    return f'doc_templates/{instance.user.id}/{filename}'


class DocumentTemplate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_templates')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=template_upload_path)
    variables = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doc_templates'
        ordering = ['-created_at']
        verbose_name = 'Plantilla de documento'
        verbose_name_plural = 'Plantillas de documentos'

    def __str__(self):
        return f'{self.name} ({self.user.email})'

    def filename(self):
        return os.path.basename(self.file.name)


class DocumentGeneration(models.Model):
    class Status(models.TextChoices):
        PENDING    = 'pending',    'Pendiente'
        PROCESSING = 'processing', 'Procesando'
        COMPLETED  = 'completed',  'Completado'
        ERROR      = 'error',      'Error'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_generations')
    template = models.ForeignKey(DocumentTemplate, on_delete=models.SET_NULL, null=True, related_name='generations')
    name = models.CharField(max_length=200)
    data = models.JSONField(default=list)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    total_records = models.PositiveIntegerField(default=0)
    processed_records = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    result_zip = models.FileField(upload_to='doc_results/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'doc_generations'
        ordering = ['-created_at']
        verbose_name = 'Generación de documentos'
        verbose_name_plural = 'Generaciones de documentos'

    def __str__(self):
        return f'{self.name} — {self.get_status_display()}'
