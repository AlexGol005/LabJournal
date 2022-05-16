# Generated by Django 4.0.4 on 2022-05-16 14:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=100, verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='ViscosimeterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pairNumber', models.CharField(max_length=100, verbose_name='Номер пары')),
                ('diameter', models.CharField(max_length=5, verbose_name='Диаметр')),
                ('viscosity1000', models.CharField(max_length=30, verbose_name='Вязкость за 1000 сек, сСт')),
                ('range', models.CharField(max_length=30, verbose_name='Область измерений, сСт')),
                ('type', models.CharField(default='ВПЖ-1', max_length=30, verbose_name='Тип')),
                ('intervalVerification', models.CharField(default='4 года', max_length=30, verbose_name='Межповерочный интервал')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Тип вискозиметра',
                'verbose_name_plural': 'Типы вискозиметров',
            },
        ),
        migrations.CreateModel(
            name='Viscosimeters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serialNumber', models.CharField(max_length=30, verbose_name='Заводской номер')),
                ('datePov', models.DateField(verbose_name='Дата поверки')),
                ('datePovDedlain', models.DateField(verbose_name='Дата окончания поверки')),
                ('companyName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viscosimeters.manufacturer', verbose_name='Производитель')),
                ('diameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viscosimeters.viscosimetertype', verbose_name='Диаметр')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viscosimeters.status', verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Вискозиметр',
                'verbose_name_plural': 'Вискозиметры',
            },
        ),
        migrations.CreateModel(
            name='Kalibration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateKalib', models.DateField(default=django.utils.timezone.now, verbose_name='Дата калибровки')),
                ('konstant', models.CharField(max_length=9, verbose_name='Установленная константа')),
                ('dateKalibNext', models.DateField(verbose_name='Следующая дата калибровки')),
                ('id_Viscosimeter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='viscosimeters.viscosimeters', verbose_name='Номер вискозиметра')),
            ],
            options={
                'verbose_name': 'Калибровка',
                'verbose_name_plural': 'Калибровки',
            },
        ),
    ]
