from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.core.models import Module, ModulePermission
from apps.core.serializers import ModulePermissionSerializer
from apps.users.permissions import IsAdminUser

User = get_user_model()


class AdminModulePermissionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        perms = ModulePermission.objects.filter(user=user).select_related('module')
        return Response(ModulePermissionSerializer(perms, many=True).data)

    def post(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            module = Module.objects.get(pk=request.data.get('module_id'))
        except Module.DoesNotExist:
            return Response({'detail': 'Módulo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        perm, _ = ModulePermission.objects.update_or_create(
            user=user, module=module,
            defaults={'is_enabled': request.data.get('is_enabled', True)}
        )
        return Response(ModulePermissionSerializer(perm).data)
