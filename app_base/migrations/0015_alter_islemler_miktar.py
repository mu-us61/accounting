# Generated by Django 4.2.5 on 2023-12-03 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0014_alter_muuser_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='islemler',
            name='miktar',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=18),
        ),
    ]
