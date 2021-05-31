# Generated by Django 3.1.7 on 2021-05-29 03:44

import apps.linabi.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('linabi', '0003_bifavorito_vuextore'),
    ]

    operations = [
        migrations.CreateModel(
            name='BIXLSXTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='Nombre')),
                ('descrip', models.TextField(blank=True, verbose_name='Descripción')),
                ('row', models.IntegerField(default=1, verbose_name='Fila Inicial')),
                ('col', models.IntegerField(default=1, verbose_name='Columna Inicial')),
                ('archivo', models.FileField(upload_to=apps.linabi.models.template_path, verbose_name='Archivo xlsx')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bixlsxtemplate_created', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bixlsxtemplate_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
            ],
            options={
                'verbose_name': 'Plantilla xlsx',
                'verbose_name_plural': 'Plantillas xlsx',
                'db_table': 'linabi_xlsxtemplate',
            },
        ),
        migrations.CreateModel(
            name='BIXLSXTemplateCol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Columna')),
                ('descrip', models.TextField(blank=True, verbose_name='Descripción')),
                ('orden', models.IntegerField(default=0, verbose_name='Orden')),
                ('posicion', models.IntegerField(default=1, verbose_name='Posición')),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bixlsxtemplatecol_created', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bixlsxtemplatecol_modified', to=settings.AUTH_USER_MODEL, verbose_name='Modificado por')),
                ('plantilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cols_x_plantilla', to='linabi.bixlsxtemplate', verbose_name='Plantilla')),
            ],
            options={
                'verbose_name': 'Columna',
                'verbose_name_plural': 'Columnas',
                'db_table': 'linabi_xlsxtemplatecol',
            },
        ),
    ]
