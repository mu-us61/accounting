# Generated by Django 4.2.5 on 2023-11-06 00:13

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0006_alter_exelusers_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exelusers',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
