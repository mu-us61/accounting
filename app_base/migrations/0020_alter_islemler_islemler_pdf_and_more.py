# Generated by Django 4.2.5 on 2023-12-30 21:52

import app_base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0019_islemler_islemler_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='islemler',
            name='islemler_pdf',
            field=models.FileField(null=True, upload_to=app_base.models.generate_unique_filename),
        ),
        migrations.AlterField(
            model_name='islemler',
            name='islemler_picture',
            field=models.ImageField(null=True, upload_to=app_base.models.generate_unique_imagename),
        ),
    ]
