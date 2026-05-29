from rest_framework.views import APIView
from rest_framework.response import Response

from apps.core.models import Module, ModulePermission
from apps.core.serializers import ModuleSerializer


class UserModulesView(APIView):
    def get(self, request):
        active_modules = Module.objects.filter(is_active=True)
        if request.user.is_admin:
            return Response(ModuleSerializer(active_modules, many=True).data)
        enabled_keys = ModulePermission.objects.filter(
            user=request.user, is_enabled=True
        ).values_list('module__key', flat=True)
        modules = active_modules.filter(key__in=enabled_keys)
        return Response(ModuleSerializer(modules, many=True).data)
