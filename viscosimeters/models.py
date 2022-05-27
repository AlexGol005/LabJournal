from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.models import User

from equipment.models import Manufacturer, Equipment





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

# class Viscosimeters(models.Model):
#     viscosimeterType = models.ForeignKey(ViscosimeterType,  verbose_name='Диаметр',
#                                  on_delete=models.PROTECT)
#     equipment = models.ForeignKey(Equipment, verbose_name='СИ',
#                                          on_delete=models.PROTECT, related_name='equipment')
#
#
#     def __str__(self):
#         return f'№ {self.equipment.lot}'
#
#     def get_absolute_url(self):
#         """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
#         return reverse('Str', kwargs={'pk': self.pk})
#
#
#     class Meta:
#         verbose_name = 'Вискозиметр'
#         verbose_name_plural = 'Вискозиметры'
#
# class Kalibration(models.Model):
#     dateKalib = models.DateField('Дата калибровки', auto_now_add=True)
#     konstant = models.DecimalField('Установленная константа', max_digits=10, decimal_places=6, default='0')
#     id_Viscosimeter = models.ForeignKey(Viscosimeters, verbose_name='Номер вискозиметра', on_delete=models.CASCADE)
#     performer = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'Константа {self.konstant}'
#
#     class Meta:
#         verbose_name = 'Калибровка'
#         verbose_name_plural = 'Калибровки'








