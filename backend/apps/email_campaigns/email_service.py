"""
Servicio de envío de correos masivos.
Maneja SMTP configurable, variables dinámicas, lotes, pausas y logging.
"""
import re
import time
import threading
from datetime import datetime, timezone

from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend

from apps.email_campaigns.models import (
    EmailCampaign, EmailRecipient, CampaignLog, SMTPConfig,
)

VARIABLE_RE = re.compile(r'\{\{(\s*[\w\s]+\s*)\}\}')

# Almacena los threads activos por campaign_id para permitir pausa/stop
_running_campaigns: dict[int, threading.Event] = {}


def _get_backend(smtp: SMTPConfig) -> EmailBackend:
    return EmailBackend(
        host=smtp.host,
        port=smtp.port,
        username=smtp.username,
        password=smtp.password,
        use_tls=smtp.use_tls,
        use_ssl=smtp.use_ssl,
        fail_silently=False,
        timeout=15,
    )


def _replace_variables(text: str, variables: dict) -> str:
    def replacer(match):
        key = match.group(1).strip()
        return str(variables.get(key, match.group(0)))
    return VARIABLE_RE.sub(replacer, text)


def _log(campaign: EmailCampaign, message: str, level: str = 'info'):
    CampaignLog.objects.create(campaign=campaign, level=level, message=message)


def send_campaign(campaign_id: int):
    """Lanza el envío de la campaña en un thread separado."""
    stop_event = threading.Event()
    _running_campaigns[campaign_id] = stop_event
    thread = threading.Thread(
        target=_run_campaign,
        args=(campaign_id, stop_event),
        daemon=True,
    )
    thread.start()


def pause_campaign(campaign_id: int):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    campaign.status = EmailCampaign.Status.PAUSED
    campaign.save(update_fields=['status'])
    _log(campaign, 'Campaña pausada por el usuario.', 'warning')


def resume_campaign(campaign_id: int):
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    campaign.status = EmailCampaign.Status.RUNNING
    campaign.save(update_fields=['status'])
    _log(campaign, 'Campaña reanudada.', 'info')
    send_campaign(campaign_id)


def stop_campaign(campaign_id: int):
    if campaign_id in _running_campaigns:
        _running_campaigns[campaign_id].set()
    campaign = EmailCampaign.objects.get(pk=campaign_id)
    campaign.status = EmailCampaign.Status.PAUSED
    campaign.save(update_fields=['status'])
    _log(campaign, 'Campaña detenida manualmente.', 'warning')


def _run_campaign(campaign_id: int, stop_event: threading.Event):
    try:
        campaign = EmailCampaign.objects.select_related('template', 'smtp_config').get(pk=campaign_id)
    except EmailCampaign.DoesNotExist:
        return

    campaign.status = EmailCampaign.Status.RUNNING
    campaign.started_at = datetime.now(timezone.utc)
    campaign.save(update_fields=['status', 'started_at'])
    _log(campaign, f'Iniciando envío — {campaign.total_recipients} destinatarios.', 'info')

    backend = _get_backend(campaign.smtp_config)
    template = campaign.template
    from_email = f'{campaign.smtp_config.from_name} <{campaign.smtp_config.from_email}>' \
        if campaign.smtp_config.from_name else campaign.smtp_config.from_email

    pending = EmailRecipient.objects.filter(campaign=campaign, status=EmailRecipient.Status.PENDING)
    batch = []
    batch_num = 0

    for recipient in pending.iterator():
        if stop_event.is_set():
            break

        # Esperar si está pausada
        while True:
            fresh = EmailCampaign.objects.values('status').get(pk=campaign_id)
            if fresh['status'] == EmailCampaign.Status.PAUSED:
                time.sleep(2)
                continue
            if fresh['status'] not in (EmailCampaign.Status.RUNNING,):
                stop_event.set()
                break
            break

        if stop_event.is_set():
            break

        subject = _replace_variables(template.subject, recipient.variables)
        html_body = _replace_variables(template.html_body, recipient.variables)
        text_body = _replace_variables(template.text_body or '', recipient.variables)

        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body or 'Ver versión HTML',
                from_email=from_email,
                to=[recipient.email],
                connection=backend,
            )
            msg.attach_alternative(html_body, 'text/html')
            msg.send()

            recipient.status = EmailRecipient.Status.SENT
            recipient.sent_at = datetime.now(timezone.utc)
            recipient.save(update_fields=['status', 'sent_at'])

            EmailCampaign.objects.filter(pk=campaign_id).update(
                sent_count=models_F('sent_count') + 1
            )
            _log(campaign, f'✓ Enviado a {recipient.email}', 'success')

        except Exception as e:
            recipient.status = EmailRecipient.Status.FAILED
            recipient.error_message = str(e)[:500]
            recipient.save(update_fields=['status', 'error_message'])

            EmailCampaign.objects.filter(pk=campaign_id).update(
                failed_count=models_F('failed_count') + 1
            )
            _log(campaign, f'✗ Error en {recipient.email}: {str(e)[:100]}', 'error')

        batch.append(recipient.id)
        batch_num += 1

        if batch_num >= campaign.batch_size:
            _log(campaign, f'Lote de {batch_num} correos completado. Pausa de {campaign.delay_seconds}s.', 'info')
            time.sleep(campaign.delay_seconds)
            batch = []
            batch_num = 0

    # Finalizar
    if not stop_event.is_set():
        campaign.refresh_from_db()
        campaign.status = EmailCampaign.Status.COMPLETED
        campaign.completed_at = datetime.now(timezone.utc)
        campaign.save(update_fields=['status', 'completed_at'])
        _log(campaign, f'Campaña completada. Enviados: {campaign.sent_count} | Errores: {campaign.failed_count}', 'success')

    _running_campaigns.pop(campaign_id, None)
    try:
        backend.close()
    except Exception:
        pass


# Importación diferida para evitar circular
from django.db.models import F as models_F  # noqa
