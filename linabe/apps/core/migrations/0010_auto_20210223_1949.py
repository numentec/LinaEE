# Generated by Django 3.1.6 on 2021-02-24 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_modulo_vista_vistaconfig_vistaconfiguser'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cia',
            table='core_cia',
        ),
        migrations.AlterModelTable(
            name='gensequence',
            table='core_gensequence',
        ),
        migrations.AlterModelTable(
            name='stakeholder',
            table='core_stakeholders',
        ),
        migrations.AlterModelTable(
            name='tipogenerico',
            table='core_tipo_generico',
        ),
    ]