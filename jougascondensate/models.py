from django.db import models
from django.contrib.auth.models import User


class GKCS(models.Model):
    name = models.CharField('Название СО краткое', max_length=100, null=True, blank=True, default='', unique=True)
    fullname = models.CharField('Название СО полное', max_length=100, null=True, blank=True, default='')
    number = models.CharField('Номер ГСО', max_length=100, null=True, blank=True, default='')
    expiration = models.CharField('Срок годности ГСО', max_length=100, null=True, blank=True, default='')
    typebegin = models.CharField('Диапазон по описанию типа от', null=True, blank=True, max_length=100)
    typeend = models.CharField('Диапазон по описанию типа до', null=True, blank=True, max_length=100)
    relerror = models.CharField('Относительная погрешность', null=True, blank=True, max_length=100)

    def __str__(self):
        return f'{self.name} № ГСО {self.number}'

    class Meta:
        verbose_name = 'Название ГСО ГК-ПА(Х)'
        verbose_name_plural = 'Названия  ГСО ГК-ПА(Х)'


class GKCSrange(models.Model):
    nameSM = models.ForeignKey(GKCS, verbose_name='СО', max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    rangeindex = models.CharField('Индекс ГСО', max_length=90, null=True, blank=True)
    name = models.CharField('краткое название ГСО с индексом', max_length=100, null=True, blank=True)
    pricebegin = models.CharField('Диапазон по прайсу от', null=True, blank=True, max_length=100)
    priceend = models.CharField('Диапазон по прайсу до', null=True, blank=True, max_length=100)



    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name}({str(self.rangeindex)})'
        super(GKCSrange, self).save(*args, **kwargs)


    def __str__(self):
        return  f'{self.name}'

    class Meta:
        verbose_name = 'Диапазон ГСО ГК-ПА(Х)'
        verbose_name_plural = 'Диапазоны  ГСО ГК-ПА(Х)'
        unique_together = ('nameSM', 'rangeindex')



class LotGKCS(models.Model):
    nameSM = models.ForeignKey(GKCSrange, verbose_name='СО', max_length=100, on_delete=models.PROTECT, null=True, blank=True)
    lot = models.CharField('Партия', max_length=5, null=True, blank=True)
    person = models.ForeignKey(User, verbose_name='Изготовил', max_length=30,  on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField('Дата изготовления', max_length=30, null=True, blank=True)
    name = models.CharField('имя и партия', max_length=1000, null=True, blank=True)
    availability = models.BooleanField('наличие партии на складе', null=True, blank=True, default=True)


    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name} п. {str(self.lot)}'
        super(LotGKCS, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.nameSM} п. {self.lot}'

    class Meta:
        verbose_name = 'Партия ГК-ПА(Х)'
        verbose_name_plural = 'Партии ГК-ПА(Х)'
        unique_together = ('nameSM', 'lot')

class CVclorinesaltsGKCS(models.Model):
    namelot = models.OneToOneField(LotGKCS, verbose_name='для СО:',
                                on_delete=models.PROTECT, null=True, blank=True, unique=True)
    cv = models.CharField('Содержание хлористых солей', max_length=30, blank=True, null=True)
    cvdate = models.DateField('Дата измерения', blank=True, null=True)
    cvexp = models.IntegerField('Срок годности', blank=True, null=True)
    cvdead = models.DateField('Годен до', blank=True, null=True)

    def __str__(self):
        return f'Содержание хлористых солей АЗ для {self.namelot}'

    class Meta:
        verbose_name = 'ГК-ПА(Х), Содержание хлористых солей'
        verbose_name_plural = 'ГК-ПА(Х), Содержание хлористых солей'

