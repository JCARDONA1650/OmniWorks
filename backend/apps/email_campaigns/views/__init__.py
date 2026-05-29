from .smtp import SMTPConfigListCreateView, SMTPConfigDetailView, SMTPTestView
from .templates import EmailTemplateListCreateView, EmailTemplateDetailView
from .campaigns import (
    CampaignListCreateView, CampaignDetailView,
    CampaignRecipientsView, CampaignExportView, CampaignLogsView,
)
from .sending import (
    CampaignStartView, CampaignPauseView,
    CampaignResumeView, CampaignStopView, CampaignStatusView,
)

__all__ = [
    'SMTPConfigListCreateView', 'SMTPConfigDetailView', 'SMTPTestView',
    'EmailTemplateListCreateView', 'EmailTemplateDetailView',
    'CampaignListCreateView', 'CampaignDetailView',
    'CampaignRecipientsView', 'CampaignExportView', 'CampaignLogsView',
    'CampaignStartView', 'CampaignPauseView',
    'CampaignResumeView', 'CampaignStopView', 'CampaignStatusView',
]
