# Generated by Django 4.2.5 on 2023-10-08 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0004_alter_islemler_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='islemler',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_base.currency'),
        ),
        migrations.AlterField(
            model_name='islemler',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app_base.tag'),
        ),
        migrations.AlterField(
            model_name='muuser',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app_base.currency'),
        ),
    ]