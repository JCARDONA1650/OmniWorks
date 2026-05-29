from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from apps.doc_generator.models import DocumentTemplate
from apps.doc_generator.serializers import DocumentTemplateSerializer
from apps.doc_generator.doc_service import extract_variables, SAMPLE_TEMPLATES, generate_sample_template


class TemplateListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentTemplateSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return DocumentTemplate.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        try:
            variables = extract_variables(instance.file.path)
            instance.variables = variables
            instance.save(update_fields=['variables'])
        except Exception:
            pass


class TemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentTemplateSerializer

    def get_queryset(self):
        return DocumentTemplate.objects.filter(user=self.request.user, is_active=True)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response({'detail': 'Plantilla eliminada.'})


class TemplateVariablesView(APIView):
    def get(self, request, pk):
        tmpl = DocumentTemplate.objects.filter(pk=pk, user=request.user).first()
        if not tmpl:
            return Response({'detail': 'Plantilla no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'variables': tmpl.variables})


class SampleTemplatesListView(APIView):
    """Devuelve la lista de plantillas de ejemplo disponibles."""
    def get(self, request):
        samples = [
            {'key': k, 'name': v['name']}
            for k, v in SAMPLE_TEMPLATES.items()
        ]
        return Response(samples)


class SampleTemplateDownloadView(APIView):
    """Descarga una plantilla de ejemplo como archivo .docx."""
    def get(self, request, key):
        if key not in SAMPLE_TEMPLATES:
            return Response({'detail': 'Plantilla no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            docx_bytes = generate_sample_template(key)
            name = SAMPLE_TEMPLATES[key]['name']
            response = HttpResponse(
                docx_bytes,
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            )
            response['Content-Disposition'] = f'attachment; filename="{name}.docx"'
            return response
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
