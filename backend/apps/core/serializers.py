from rest_framework import serializers
from .models import Module, ModulePermission


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'key', 'name', 'description', 'icon', 'route', 'is_active', 'order']


class ModulePermissionSerializer(serializers.ModelSerializer):
    module = ModuleSerializer(read_only=True)
    module_id = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(), source='module', write_only=True
    )

    class Meta:
        model = ModulePermission
        fields = ['id', 'module', 'module_id', 'is_enabled']
