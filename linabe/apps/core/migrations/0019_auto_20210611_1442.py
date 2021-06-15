# Generated by Django 3.1.7 on 2021-06-11 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0018_auto_20210605_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='VistaConfigAcc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceso', models.BooleanField(default=True, verbose_name='Acceso')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_x_group', to='auth.group', verbose_name='Grupo')),
                ('vistaconf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc_x_vistaconf', to='core.vistaconfig', verbose_name='Vistaconf')),
            ],
            options={
                'verbose_name': 'Acceso a conf',
                'verbose_name_plural': 'Accesos a conf',
                'db_table': 'core_vistaconfacc',
            },
        ),
        migrations.RemoveField(
            model_name='vistaelementaccess',
            name='group',
        ),
        migrations.RemoveField(
            model_name='vistaelementaccess',
            name='vista_element',
        ),
        migrations.DeleteModel(
            name='VistaElement',
        ),
        migrations.DeleteModel(
            name='VistaElementAccess',
        ),
    ]