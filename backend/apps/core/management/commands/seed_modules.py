from django.core.management.base import BaseCommand
from apps.core.models import Module


class Command(BaseCommand):
    help = 'Crea los módulos iniciales del sistema'

    def handle(self, *args, **kwargs):
        modules = [
            {
                'key': 'email_campaigns',
                'name': 'Envíos Corporativos',
                'description': 'Sistema de correos masivos personalizados con variables dinámicas.',
                'icon': 'mail',
                'route': '/email-campaigns',
                'order': 1,
            },
            {
                'key': 'notes',
                'name': 'Notas',
                'description': 'Sistema empresarial de notas internas con IA integrada.',
                'icon': 'note',
                'route': '/notes',
                'order': 2,
            },
            {
                'key': 'doc_generator',
                'name': 'Generador de Documentos',
                'description': 'Generación masiva de documentos desde plantillas Word con variables dinámicas.',
                'icon': 'file-text',
                'route': '/doc-generator',
                'order': 3,
            },
        ]

        for data in modules:
            obj, created = Module.objects.get_or_create(key=data['key'], defaults=data)
            action = 'Creado' if created else 'Ya existe'
            self.stdout.write(f'  {action}: {obj.name}')

        self.stdout.write(self.style.SUCCESS('Módulos iniciales cargados correctamente.'))
