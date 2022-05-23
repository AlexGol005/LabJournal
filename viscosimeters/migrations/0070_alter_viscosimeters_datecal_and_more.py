# Generated by Django 4.0.4 on 2022-05-23 08:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('viscosimeters', '0069_alter_viscosimeters_datecal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscosimeters',
            name='dateCal',
            field=models.DateField(default=datetime.datetime(2022, 5, 23, 8, 36, 38, 335190, tzinfo=utc), verbose_name='Дата калибровки'),
        ),
        migrations.AlterField(
            model_name='viscosimeters',
            name='datePov',
            field=models.DateField(default=datetime.datetime(2022, 5, 23, 8, 36, 38, 335190, tzinfo=utc), verbose_name='Дата поверки'),
        ),
        migrations.AlterField(
            model_name='viscosimeters',
            name='datePovDedlain',
            field=models.DateField(default=datetime.datetime(2022, 5, 23, 11, 36, 38, 335190), verbose_name='Дата окончания поверки'),
        ),
    ]
