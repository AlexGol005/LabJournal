# Generated by Django 4.0.4 on 2022-05-16 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viscosityattestation', '0009_alter_viscositymjl_performer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viscositymjl',
            name='performer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель'),
        ),
    ]
