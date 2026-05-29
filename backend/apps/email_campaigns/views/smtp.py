from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.email_campaigns.models import SMTPConfig
from apps.email_campaigns.serializers import SMTPConfigSerializer, SMTPConfigListSerializer


class SMTPConfigListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        return SMTPConfig.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return SMTPConfigSerializer if self.request.method == 'POST' else SMTPConfigListSerializer


class SMTPConfigDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SMTPConfigSerializer

    def get_queryset(self):
        return SMTPConfig.objects.filter(user=self.request.user)


class SMTPTestView(APIView):
    """Prueba la configuración SMTP enviando un correo de test."""

    def post(self, request, pk):
        smtp = SMTPConfig.objects.filter(pk=pk, user=request.user).first()
        if not smtp:
            return Response({'detail': 'Configuración no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        from django.core.mail import EmailMessage
        from django.core.mail.backends.smtp import EmailBackend

        try:
            backend = EmailBackend(
                host=smtp.host, port=smtp.port,
                username=smtp.username, password=smtp.password,
                use_tls=smtp.use_tls, use_ssl=smtp.use_ssl,
                fail_silently=False, timeout=10,
            )
            msg = EmailMessage(
                subject='✓ Prueba de conexión SMTP — OmniWorks',
                body='Esta es una prueba de conexión SMTP desde OmniWorks. Si recibes este correo, la configuración es correcta.',
                from_email=smtp.from_email,
                to=[request.user.email],
                connection=backend,
            )
            msg.send()
            backend.close()
            return Response({'detail': f'Correo de prueba enviado correctamente a {request.user.email}.'})
        except Exception as e:
            return Response({'detail': f'Error de conexión: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
