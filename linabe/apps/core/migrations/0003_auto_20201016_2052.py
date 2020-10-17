# Generated by Django 3.1.2 on 2020-10-17 01:52

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
