from django.urls import path
from apps.doc_generator.views import (
    TemplateListCreateView, TemplateDetailView, TemplateVariablesView,
    SampleTemplatesListView, SampleTemplateDownloadView,
    GenerationListView, GenerateSingleView, GenerateBulkView, ImportExcelPreviewView,
)

urlpatterns = [
    # Plantillas de ejemplo (sin autenticación de usuario requerida para descarga)
    path('docs/samples/',                            SampleTemplatesListView.as_view(),    name='doc_samples'),
    path('docs/samples/<str:key>/download/',         SampleTemplateDownloadView.as_view(), name='doc_sample_download'),

    # Plantillas del usuario
    path('docs/templates/',                          TemplateListCreateView.as_view(),     name='doc_templates'),
    path('docs/templates/<int:pk>/',                 TemplateDetailView.as_view(),         name='doc_template_detail'),
    path('docs/templates/<int:pk>/variables/',       TemplateVariablesView.as_view(),      name='doc_template_variables'),

    # Generación
    path('docs/generations/',                        GenerationListView.as_view(),         name='doc_generations'),
    path('docs/templates/<int:template_id>/generate/', GenerateSingleView.as_view(),      name='doc_generate_single'),
    path('docs/templates/<int:template_id>/bulk/',   GenerateBulkView.as_view(),           name='doc_generate_bulk'),
    path('docs/import/preview/',                     ImportExcelPreviewView.as_view(),     name='doc_import_preview'),
]
