# Generated by Django 4.2.5 on 2023-12-27 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0018_alter_etkinlikmodel_etkinlik_youtubelink'),
    ]

    operations = [
        migrations.AddField(
            model_name='islemler',
            name='islemler_type',
            field=models.CharField(blank=True, choices=[('gelen', 'Gelen'), ('giden', 'Giden'), ('vakifici', 'Vakifici')], max_length=10, null=True),
        ),
    ]
