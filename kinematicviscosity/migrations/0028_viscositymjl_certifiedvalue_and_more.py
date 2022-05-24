# Generated by Django 4.0.4 on 2022-05-24 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinematicviscosity', '0027_alter_viscositymjl_viscosimeternumber1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viscositymjl',
            name='certifiedValue',
            field=models.FloatField(null=True, verbose_name='Аттестованное значение'),
        ),
        migrations.AddField(
            model_name='viscositymjl',
            name='oldCertifiedValue',
            field=models.FloatField(null=True, verbose_name='Предыдущее аттестованное значение'),
        ),
    ]
