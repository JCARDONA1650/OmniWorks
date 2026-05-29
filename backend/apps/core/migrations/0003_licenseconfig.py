from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=200, verbose_name='Nombre del cliente')),
                ('expiration_date', models.DateField(verbose_name='Fecha de vencimiento')),
                ('notes', models.TextField(blank=True, verbose_name='Notas internas')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Licencia',
                'verbose_name_plural': 'Configuración de Licencia',
                'db_table': 'license_config',
            },
        ),
    ]
