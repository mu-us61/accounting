# Generated by Django 4.2.6 on 2024-05-06 01:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_base', '0023_alter_mugroup_can_delete_alter_mugroup_can_write'),
    ]

    operations = [
        migrations.CreateModel(
            name='Yetkiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_read_can_kullanicilar', models.BooleanField(default=False)),
                ('can_read_kullanici_gruplari', models.BooleanField(default=False)),
                ('can_read_excel_kullanici_yukleme', models.BooleanField(default=False)),
                ('can_read_excel_kullanicilari', models.BooleanField(default=False)),
                ('can_read_bakiye', models.BooleanField(default=False)),
                ('can_read_harcama_kalemi', models.BooleanField(default=False)),
                ('can_read_Islemleretkinlikler', models.BooleanField(default=False)),
                ('can_read_evraklar', models.BooleanField(default=False)),
                ('can_read_aylikharcamalar', models.BooleanField(default=False)),
                ('can_read_aylikispatliharcamalar', models.BooleanField(default=False)),
                ('can_read_smsyonetimi', models.BooleanField(default=False)),
                ('can_read_mobileapplinkleri', models.BooleanField(default=False)),
                ('can_write_can_kullanicilar', models.BooleanField(default=False)),
                ('can_write_kullanici_gruplari', models.BooleanField(default=False)),
                ('can_write_excel_kullanici_yukleme', models.BooleanField(default=False)),
                ('can_write_excel_kullanicilari', models.BooleanField(default=False)),
                ('can_write_bakiye', models.BooleanField(default=False)),
                ('can_write_harcama_kalemi', models.BooleanField(default=False)),
                ('can_write_Islemleretkinlikler', models.BooleanField(default=False)),
                ('can_write_evraklar', models.BooleanField(default=False)),
                ('can_write_aylikharcamalar', models.BooleanField(default=False)),
                ('can_write_aylikispatliharcamalar', models.BooleanField(default=False)),
                ('can_write_smsyonetimi', models.BooleanField(default=False)),
                ('can_write_mobileapplinkleri', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='mugroup',
            name='can_delete',
        ),
        migrations.RemoveField(
            model_name='mugroup',
            name='can_write',
        ),
        migrations.AddField(
            model_name='mugroup',
            name='yetkiler',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='gruplar', to='app_base.yetkiler'),
            preserve_default=False,
        ),
    ]
