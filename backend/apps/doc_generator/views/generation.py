import io
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import HttpResponse

from apps.doc_generator.models import DocumentTemplate, DocumentGeneration
from apps.doc_generator.serializers import DocumentGenerationSerializer
from apps.doc_generator.doc_service import (
    generate_document, generate_bulk, parse_excel_data
)


class GenerationListView(generics.ListAPIView):
    serializer_class = DocumentGenerationSerializer

    def get_queryset(self):
        return DocumentGeneration.objects.filter(user=self.request.user)


class GenerateSingleView(APIView):
    """Genera un único documento a partir de una plantilla y datos."""

    def post(self, request, template_id):
        tmpl = DocumentTemplate.objects.filter(pk=template_id, user=request.user, is_active=True).first()
        if not tmpl:
            return Response({'detail': 'Plantilla no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.get('data', {})
        if not isinstance(data, dict):
            return Response({'detail': 'El campo "data" debe ser un objeto con variables.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            docx_bytes = generate_document(tmpl.file.path, data)
        except Exception as e:
            return Response({'detail': f'Error al generar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        filename = f'{tmpl.name}.docx'
        response = HttpResponse(
            docx_bytes,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class GenerateBulkView(APIView):
    """Genera documentos en masa y retorna ZIP."""
    parser_classes = [MultiPartParser, JSONParser]

    def post(self, request, template_id):
        tmpl = DocumentTemplate.objects.filter(pk=template_id, user=request.user, is_active=True).first()
        if not tmpl:
            return Response({'detail': 'Plantilla no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        records = None

        # Si viene archivo Excel
        excel_file = request.FILES.get('excel')
        if excel_file:
            try:
                records = parse_excel_data(excel_file)
            except Exception as e:
                return Response({'detail': f'Error al leer Excel: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Si vienen datos JSON directos
        if records is None:
            records = request.data.get('records', [])

        if not records:
            return Response({'detail': 'No se recibieron registros para procesar.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            zip_bytes, processed, errors = generate_bulk(tmpl.file.path, records)
        except Exception as e:
            return Response({'detail': f'Error al generar documentos: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        gen = DocumentGeneration.objects.create(
            user=request.user,
            template=tmpl,
            name=f'Generación masiva — {tmpl.name}',
            data=records,
            status=DocumentGeneration.Status.COMPLETED,
            total_records=len(records),
            processed_records=processed,
        )

        response = HttpResponse(zip_bytes, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="documentos_{gen.id}.zip"'
        response['X-Generation-Id'] = str(gen.id)
        response['X-Processed'] = str(processed)
        response['X-Errors'] = str(errors)
        return response


class ImportExcelPreviewView(APIView):
    """Previsualiza los datos de un Excel antes de generar."""
    parser_classes = [MultiPartParser]

    def post(self, request):
        excel_file = request.FILES.get('excel')
        if not excel_file:
            return Response({'detail': 'Se requiere un archivo Excel.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            records = parse_excel_data(excel_file)
            return Response({
                'total': len(records),
                'columns': list(records[0].keys()) if records else [],
                'preview': records[:5],
            })
        except Exception as e:
            return Response({'detail': f'Error al procesar Excel: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
