import json
from django.http import JsonResponse
from django.utils import timezone


class LicenseMiddleware:
    """
    Bloquea todas las llamadas al API cuando la licencia de uso ha vencido.
    El panel de administración Django (/django-admin/) sigue disponible
    para que OnmiTek pueda actualizar la fecha de vencimiento.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            expired, expiration_date = self._check_license()
            if expired:
                return JsonResponse(
                    {
                        'detail': 'license_expired',
                        'expiration_date': expiration_date,
                        'contact': 'info@onmiteksolutions.com',
                        'whatsapp': 'https://wa.me/573202828836',
                        'website': 'https://www.onmiteksolutions.com',
                    },
                    status=402,
                )
        return self.get_response(request)

    @staticmethod
    def _check_license() -> tuple[bool, str]:
        """Retorna (is_expired, expiration_date_str)."""
        try:
            from apps.core.models import LicenseConfig
            license_obj = LicenseConfig.objects.only('expiration_date').first()
            if license_obj is None:
                return False, ''  # Sin registro = sin restricción
            today = timezone.now().date()
            expired = today > license_obj.expiration_date
            return expired, str(license_obj.expiration_date)
        except Exception:
            return False, ''
