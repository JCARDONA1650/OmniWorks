from django.db import models
from django.conf import settings
from django.utils import timezone


class Module(models.Model):
    class ModuleKey(models.TextChoices):
        EMAIL_CAMPAIGNS = 'email_campaigns', 'Envíos Corporativos'
        NOTES = 'notes', 'Notas'

    key = models.CharField(max_length=50, choices=ModuleKey.choices, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    route = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'modules'
        ordering = ['order', 'name']
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return self.name


class ModulePermission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='module_permissions'
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='permissions')
    is_enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'module_permissions'
        unique_together = ('user', 'module')
        verbose_name = 'Permiso de módulo'
        verbose_name_plural = 'Permisos de módulos'

    def __str__(self):
        status = 'habilitado' if self.is_enabled else 'deshabilitado'
        return f'{self.user.email} — {self.module.name} ({status})'


class LicenseConfig(models.Model):
    """
    Configuración de licencia del sistema. Solo debe existir un registro.
    Si la fecha de vencimiento es superada, el acceso al API queda bloqueado.
    """
    client_name = models.CharField('Nombre del cliente', max_length=200)
    expiration_date = models.DateField('Fecha de vencimiento')
    notes = models.TextField('Notas internas', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'license_config'
        verbose_name = 'Licencia'
        verbose_name_plural = 'Configuración de Licencia'

    def __str__(self):
        return f'{self.client_name} — vence {self.expiration_date}'

    @property
    def is_expired(self) -> bool:
        return timezone.now().date() > self.expiration_date

    @property
    def days_remaining(self) -> int:
        return (self.expiration_date - timezone.now().date()).days
