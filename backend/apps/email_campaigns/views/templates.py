from rest_framework import generics
from apps.email_campaigns.models import EmailTemplate
from apps.email_campaigns.serializers import EmailTemplateSerializer


class EmailTemplateListCreateView(generics.ListCreateAPIView):
    serializer_class = EmailTemplateSerializer

    def get_queryset(self):
        return EmailTemplate.objects.filter(user=self.request.user)


class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmailTemplateSerializer

    def get_queryset(self):
        return EmailTemplate.objects.filter(user=self.request.user)
