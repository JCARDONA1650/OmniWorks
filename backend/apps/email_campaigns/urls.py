from django.urls import path
from apps.email_campaigns.views import (
    SMTPConfigListCreateView, SMTPConfigDetailView, SMTPTestView,
    EmailTemplateListCreateView, EmailTemplateDetailView,
    CampaignListCreateView, CampaignDetailView,
    CampaignRecipientsView, CampaignExportView, CampaignLogsView,
    CampaignStartView, CampaignPauseView,
    CampaignResumeView, CampaignStopView, CampaignStatusView,
)

urlpatterns = [
    # SMTP
    path('campaigns/smtp/',          SMTPConfigListCreateView.as_view(), name='smtp_list'),
    path('campaigns/smtp/<int:pk>/', SMTPConfigDetailView.as_view(),     name='smtp_detail'),
    path('campaigns/smtp/<int:pk>/test/', SMTPTestView.as_view(),        name='smtp_test'),

    # Plantillas
    path('campaigns/templates/',          EmailTemplateListCreateView.as_view(), name='email_template_list'),
    path('campaigns/templates/<int:pk>/', EmailTemplateDetailView.as_view(),     name='email_template_detail'),

    # Campañas
    path('campaigns/',          CampaignListCreateView.as_view(), name='campaign_list'),
    path('campaigns/<int:pk>/', CampaignDetailView.as_view(),     name='campaign_detail'),

    # Destinatarios y resultados
    path('campaigns/<int:pk>/recipients/', CampaignRecipientsView.as_view(), name='campaign_recipients'),
    path('campaigns/<int:pk>/export/',     CampaignExportView.as_view(),     name='campaign_export'),
    path('campaigns/<int:pk>/logs/',       CampaignLogsView.as_view(),       name='campaign_logs'),

    # Control de envío
    path('campaigns/<int:pk>/start/',  CampaignStartView.as_view(),  name='campaign_start'),
    path('campaigns/<int:pk>/pause/',  CampaignPauseView.as_view(),  name='campaign_pause'),
    path('campaigns/<int:pk>/resume/', CampaignResumeView.as_view(), name='campaign_resume'),
    path('campaigns/<int:pk>/stop/',   CampaignStopView.as_view(),   name='campaign_stop'),
    path('campaigns/<int:pk>/status/', CampaignStatusView.as_view(), name='campaign_status'),
]
