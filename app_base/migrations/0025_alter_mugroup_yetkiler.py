# Generated by Django 4.2.6 on 2024-05-06 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0024_yetkiler_remove_mugroup_can_delete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mugroup',
            name='yetkiler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gruplar_related', to='app_base.yetkiler'),
        ),
    ]
