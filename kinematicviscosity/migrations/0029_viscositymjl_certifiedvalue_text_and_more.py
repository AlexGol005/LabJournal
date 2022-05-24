# Generated by Django 4.0.4 on 2022-05-24 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinematicviscosity', '0028_viscositymjl_certifiedvalue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viscositymjl',
            name='certifiedValue_text',
            field=models.CharField(default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='viscositymjl',
            name='certifiedValue',
            field=models.DecimalField(decimal_places=10, max_digits=20, null=True, verbose_name='Аттестованное значение'),
        ),
    ]
