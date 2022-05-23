# Generated by Django 4.0.4 on 2022-05-23 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viscosimeters', '0076_viscosimeters_viscosity1000_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscosimeters',
            name='viscosity1000',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='viscosity1000_on', to='viscosimeters.viscosimetertype', verbose_name='вязкость/1000'),
        ),
    ]
