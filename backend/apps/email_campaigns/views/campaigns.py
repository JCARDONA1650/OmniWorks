import io
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import HttpResponse

from apps.email_campaigns.models import EmailCampaign, EmailRecipient, CampaignLog
from apps.email_campaigns.serializers import (
    EmailCampaignSerializer, EmailRecipientSerializer, CampaignLogSerializer,
)


class CampaignListCreateView(generics.ListCreateAPIView):
    serializer_class = EmailCampaignSerializer

    def get_queryset(self):
        return EmailCampaign.objects.filter(user=self.request.user)


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailCampaignSerializer

    def get_queryset(self):
        return EmailCampaign.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        campaign = self.get_object()
        if campaign.status == EmailCampaign.Status.RUNNING:
            return Response({'detail': 'No se puede eliminar una campaña en ejecución.'}, status=status.HTTP_400_BAD_REQUEST)
        campaign.delete()
        return Response({'detail': 'Campaña eliminada.'})


class CampaignRecipientsView(APIView):
    """Obtiene o importa destinatarios de una campaña."""
    parser_classes = [MultiPartParser, JSONParser]

    def get(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        recipients = EmailRecipient.objects.filter(campaign=campaign)
        serializer = EmailRecipientSerializer(recipients, many=True)
        return Response({'total': recipients.count(), 'recipients': serializer.data})

    def post(self, request, pk):
        """Importa destinatarios desde JSON o archivo Excel/CSV."""
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        if campaign.status not in (EmailCampaign.Status.DRAFT, EmailCampaign.Status.READY):
            return Response({'detail': 'Solo se pueden modificar destinatarios en campañas en borrador.'}, status=status.HTTP_400_BAD_REQUEST)

        records = []

        excel_file = request.FILES.get('file')
        if excel_file:
            try:
                import openpyxl
                wb = openpyxl.load_workbook(excel_file, read_only=True)
                ws = wb.active
                headers = [str(c.value).strip() for c in next(ws.iter_rows(max_row=1))]
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if any(v is not None for v in row):
                        records.append({headers[i]: (str(v) if v is not None else '') for i, v in enumerate(row)})
            except Exception as e:
                return Response({'detail': f'Error al leer archivo: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            records = request.data.get('recipients', [])

        if not records:
            return Response({'detail': 'No se recibieron destinatarios.'}, status=status.HTTP_400_BAD_REQUEST)

        email_field = request.data.get('email_field', 'email')

        created = 0
        for record in records:
            email = record.get(email_field, '').strip()
            if not email or '@' not in email:
                continue
            variables = {k: v for k, v in record.items() if k != email_field}
            EmailRecipient.objects.get_or_create(
                campaign=campaign, email=email,
                defaults={'variables': variables}
            )
            created += 1

        total = EmailRecipient.objects.filter(campaign=campaign).count()
        campaign.total_recipients = total
        campaign.status = EmailCampaign.Status.READY
        campaign.save(update_fields=['total_recipients', 'status'])

        return Response({'imported': created, 'total': total})


class CampaignExportView(APIView):
    """Exporta los resultados de la campaña en Excel."""

    def get(self, request, pk):
        campaign = EmailCampaign.objects.filter(pk=pk, user=request.user).first()
        if not campaign:
            return Response({'detail': 'Campaña no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Resultados'

        headers = ['Email', 'Estado', 'Fecha envío', 'Error']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill('solid', fgColor='1E6FFF')
            cell.alignment = Alignment(horizontal='center')

        status_map = {'pending': 'Pendiente', 'sent': 'Enviado', 'failed': 'Error'}
        for row_idx, r in enumerate(EmailRecipient.objects.filter(campaign=campaign), 2):
            ws.cell(row=row_idx, column=1, value=r.email)
            ws.cell(row=row_idx, column=2, value=status_map.get(r.status, r.status))
            ws.cell(row=row_idx, column=3, value=str(r.sent_at) if r.sent_at else '')
            ws.cell(row=row_idx, column=4, value=r.error_message)

        for col in range(1, 5):
            ws.column_dimensions[get_column_letter(col)].auto_size = True

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        filename = f'{campaign.name}_resultados.xlsx'
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class CampaignLogsView(generics.ListAPIView):
    serializer_class = CampaignLogSerializer

    def get_queryset(self):
        campaign = EmailCampaign.objects.filter(pk=self.kwargs['pk'], user=self.request.user).first()
        if not campaign:
            return CampaignLog.objects.none()
        since_id = self.request.query_params.get('since_id', 0)
        return CampaignLog.objects.filter(campaign=campaign, id__gt=since_id).order_by('created_at')
