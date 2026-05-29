from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.email_campaigns.models import EmailCampaign
from apps.email_campaigns.serializers import EmailCampaignSerializer
from apps.email_campaigns import email_service


class CampaignStartView(APIView):
    def post(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        if campaign.status == EmailCampaign.Status.RUNNING:
            return Response({'detail': 'La campaña ya está en ejecución.'}, status=status.HTTP_400_BAD_REQUEST)
        if not campaign.smtp_config:
            return Response({'detail': 'La campaña no tiene una configuración SMTP asignada.'}, status=status.HTTP_400_BAD_REQUEST)
        if campaign.total_recipients == 0:
            return Response({'detail': 'La campaña no tiene destinatarios.'}, status=status.HTTP_400_BAD_REQUEST)

        email_service.send_campaign(campaign.id)
        campaign.refresh_from_db()
        return Response(EmailCampaignSerializer(campaign).data)


class CampaignPauseView(APIView):
    def post(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        email_service.pause_campaign(campaign.id)
        campaign.refresh_from_db()
        return Response(EmailCampaignSerializer(campaign).data)


class CampaignResumeView(APIView):
    def post(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        email_service.resume_campaign(campaign.id)
        campaign.refresh_from_db()
        return Response(EmailCampaignSerializer(campaign).data)


class CampaignStopView(APIView):
    def post(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        email_service.stop_campaign(campaign.id)
        campaign.refresh_from_db()
        return Response(EmailCampaignSerializer(campaign).data)


class CampaignStatusView(APIView):
    """Polling endpoint para el frontend — retorna estado actual y últimos logs."""
    def get(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        campaign.refresh_from_db()
        return Response(EmailCampaignSerializer(campaign).data)
