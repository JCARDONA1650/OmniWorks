from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea el usuario administrador principal de OmniWorks'

    def handle(self, *args, **kwargs):
        email = 'admin@omniteksolutions.com'
        if User.objects.filter(email=email).exists():
            self.stdout.write(f'El administrador ya existe: {email}')
            return

        user = User.objects.create_superuser(
            username='admin',
            email=email,
            password='Admin2026!',
            first_name='Admin',
            last_name='OmniTek',
            role='admin',
        )
        self.stdout.write(self.style.SUCCESS(
            f'Administrador creado: {user.email} / contraseña: Admin2026!'
        ))
