# Generated by Django 4.0.4 on 2022-05-16 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viscosityattestation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time12_sec',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time1_avg',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time21_sec',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time22_sec',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='time2_avg',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='viscosity1',
        ),
        migrations.RemoveField(
            model_name='viscositymjl',
            name='viscosity2',
        ),
    ]
