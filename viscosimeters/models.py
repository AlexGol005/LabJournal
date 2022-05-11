from django.db import models
from django.utils import timezone


class Manufacturer(models.Model):
    companyName = models.CharField('Производитель', max_length=100)

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Status(models.Model):
    status = models.CharField('Статус', max_length=100)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class ViscosimeterType(models.Model):
    pairNumber = models.CharField('Номер пары', max_length=100)
    diameter = models.CharField('Диаметр', max_length=5)
    viscosity1000 = models.CharField('Вязкость за 1000 сек, сСт', max_length=30)
    range = models.CharField('Область измерений, сСт', max_length=30)
    type = models.CharField('Тип', max_length=30, default='ВПЖ-1')
    intervalVerification = models.CharField('Межповерочный интервал', max_length=30, default='4 года')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.diameter}'

    class Meta:
        verbose_name = 'Тип вискозиметра'
        verbose_name_plural = 'Типы вискозиметров'

class Viscosimeters(models.Model):
    diameter = models.ForeignKey(ViscosimeterType, verbose_name='Диаметр', on_delete=models.CASCADE)
    serialNumber = models.CharField('Заводской номер', max_length=30)
    datePov = models.DateField('Дата поверки')
    datePovDedlain = models.DateField('Дата окончания поверки')
    status = models.ForeignKey(Status, verbose_name='Статус', on_delete=models.CASCADE)
    companyName = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)

    def __str__(self):
        return f'№ {self.serialNumber}'

    class Meta:
        verbose_name = 'Вискозиметр'
        verbose_name_plural = 'Вискозиметры'


class Kalibration(models.Model):
    dateKalib = models.DateField('Дата калибровки', default=timezone.now)
    konstant = models.CharField('Установленная константа', max_length=9)
    dateKalibNext = models.DateField('Следующая дата калибровки')
    id_Viscosimeter = models.ForeignKey(Viscosimeters, verbose_name='Номер вискозиметра', on_delete=models.CASCADE)

    def __str__(self):
        return f'Константа {self.konstant}'

    class Meta:
        verbose_name = 'Калибровка'
        verbose_name_plural = 'Калибровки'






