# Generated by Django 4.0.4 on 2022-04-28 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viscosimeters', '0006_remove_viscosimeters_viscosity1000_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viscosimeters',
            name='id_ViscosimeterType',
        ),
        migrations.AddField(
            model_name='viscosimeters',
            name='diameter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='viscosimeters.viscosimetertype', verbose_name='Диаметр'),
            preserve_default=False,
        ),
    ]
