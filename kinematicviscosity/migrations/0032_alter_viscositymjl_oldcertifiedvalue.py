# Generated by Django 4.0.4 on 2022-05-24 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinematicviscosity', '0031_alter_viscositymjl_oldcertifiedvalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscositymjl',
            name='oldCertifiedValue',
            field=models.FloatField(null=True, verbose_name='Предыдущее аттестованное значение'),
        ),
    ]
