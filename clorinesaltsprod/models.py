from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class GetClorine(models.Model):
    date = models.DateField('Дата определения', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='performerCl', blank=True)
    namelot = models.CharField('Производитель и партия хлорида лития', max_length=100, default='', null=True, blank=True)
    AgNO3concentration = models.DecimalField('Концентрация раствора нитрата серебра, М', max_digits=5,
                                             decimal_places=4, null=True, blank=True)
    LiClmass1 = models.DecimalField('Масса хлорида лития №1, г', max_digits=5, decimal_places=4, null=True, blank=True)
    LiClmass2 = models.DecimalField('Масса хлорида лития №2, г', max_digits=5, decimal_places=4, null=True, blank=True)
    AgNO3volume1 = models.DecimalField('Объём нитрата серебра №1, мл', max_digits=3, decimal_places=1, null=True,
                                       blank=True)
    AgNO3volume2 = models.DecimalField('Объём нитрата серебра №2, мл', max_digits=3, decimal_places=1, null=True,
                                       blank=True)
    Clpercent1 = models.DecimalField('Массовая доля Cl- №1, %', max_digits=4, decimal_places=2, null=True, blank=True)
    Clpercent2 = models.DecimalField('Массовая доля Cl- №2, %', max_digits=4, decimal_places=2, null=True, blank=True)
    resultMeas = models.CharField('Результат уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    Clpercent = models.DecimalField('Массовая доля Cl-, %', max_digits=4, decimal_places=2, null=True, blank=True)

    @staticmethod
    def getClpercent(AgNO3concentration, AgNO3volume, LiClmass):
        Clpercent = ((AgNO3concentration * Decimal('35.5') * AgNO3volume) / (LiClmass * Decimal('10'))).\
            quantize(Decimal('1.00'), ROUND_HALF_UP)
        return Clpercent

    def save(self, *args, **kwargs):
        self.Clpercent1 = self.getClpercent(self.AgNO3concentration, self.AgNO3volume1, self.LiClmass1)
        self.Clpercent2 = self.getClpercent(self.AgNO3concentration, self.AgNO3volume2, self.LiClmass2)
        kr = (self.Clpercent1 - self.Clpercent2).copy_abs()
        if kr > Decimal('0.3'):
            self.resultMeas = 'Неудовлетворительно:'
            self.cause = 'разность между измерениями больше критического диапазона, измерьте повторно'
        if kr <= Decimal('0.3'):
            self.resultMeas = 'Удовлетворительно:'
            self.Clpercent = ((self.Clpercent1 + self.Clpercent2) / Decimal(2)).\
                quantize(Decimal('1.00'), ROUND_HALF_UP)



    def __str__(self):
        return f'Хлорид лития,  {self.Clpercent} %'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('getconcentrationCl', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'массовая доля хлористых солей'
        verbose_name_plural = 'массовые доли хлористых солей'
