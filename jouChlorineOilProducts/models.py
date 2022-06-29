from django.db import models
from django.contrib.auth.models import User


class CSN(models.Model):
    name = models.CharField('Название СО краткое', max_length=100, null=True, blank=True, default='', unique=True)
    fullname = models.CharField('Название СО полное', max_length=100, null=True, blank=True, default='')
    number = models.CharField('Номер ГСО', max_length=100, null=True, blank=True, default='')
    expiration = models.CharField('Срок годности ГСО', max_length=100, null=True, blank=True, default='')
    typebegin = models.FloatField('Диапазон по описанию типа от', null=True, blank=True)
    typeend = models.FloatField('Диапазон по описанию типа до', null=True, blank=True)
    relerror = models.FloatField('Относительная погрешность', null=True, blank=True)

    def __str__(self):
        return f'{self.name} № ГСО {self.number}'

    class Meta:
        verbose_name = 'Название ГСО ХСН-ПА'
        verbose_name_plural = 'Названия  ГСО ХСН-ПА'


class CSNrange(models.Model):
    nameSM = models.ForeignKey(CSN, verbose_name='СО', max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    rangeindex = models.IntegerField('Индекс ГСО', null=True, blank=True)
    name = models.CharField('краткое название ГСО с индексом', max_length=100, null=True, blank=True)
    pricebegin = models.FloatField('Диапазон по прайсу от', null=True, blank=True)
    priceend = models.FloatField('Диапазон по прайсу до', null=True, blank=True)



    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name}({str(self.rangeindex)})'
        super(CSNrange, self).save(*args, **kwargs)


    def __str__(self):
        return  f'{self.name}'

    class Meta:
        verbose_name = 'Диапазон ГСО ХСН-ПА'
        verbose_name_plural = 'Диапазоны  ГСО ХСН-ПА'
        unique_together = ('nameSM', 'rangeindex')



class LotCSN(models.Model):
    nameSM = models.ForeignKey(CSNrange, verbose_name='СО', max_length=100, on_delete=models.PROTECT, null=True, blank=True)
    lot = models.CharField('Партия', max_length=5, null=True, blank=True)
    person = models.ForeignKey(User, verbose_name='Изготовил', max_length=30,  on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField('Дата изготовления', max_length=30, null=True, blank=True)
    name = models.CharField('имя и партия', max_length=1000, null=True, blank=True)
    availability = models.BooleanField('наличие партии на складе', null=True, blank=True, default=True)


    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name} п. {str(self.lot)}'
        super(LotCSN, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.nameSM} п. {self.lot}'

    class Meta:
        verbose_name = 'Партия ХСН-ПА'
        verbose_name_plural = 'Партии ХСН-ПА'
        unique_together = ('nameSM', 'lot')

class CVclorinesaltsCSN(models.Model):
    namelot = models.OneToOneField(LotCSN, verbose_name='для СО:',
                                on_delete=models.PROTECT, null=True, blank=True, unique=True)
    cv = models.CharField('Содержание хлористых солей', max_length=30, blank=True, null=True)
    cvdate = models.DateField('Дата измерения', blank=True, null=True)
    cvexp = models.IntegerField('Срок годности', blank=True, null=True)
    cvdead = models.DateField('Годен до', blank=True, null=True)

    def __str__(self):
        return f'Содержание хлористых солей АЗ для {self.namelot}'

    class Meta:
        verbose_name = 'ХСН-ПА, Содержание хлористых солей'
        verbose_name_plural = 'ХСН-ПА, Содержание хлористых солей'



