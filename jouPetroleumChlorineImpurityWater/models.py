from django.db import models
from django.contrib.auth.models import User


class SSTN(models.Model):
    name = models.CharField('Название СО краткое', max_length=100, null=True, blank=True, default='', unique=True)
    fullname = models.CharField('Название СО полное', max_length=100, null=True, blank=True, default='')
    number = models.CharField('Номер ГСО', max_length=100, null=True, blank=True, default='')
    expiration = models.CharField('Срок годности ГСО', max_length=100, null=True, blank=True, default='')
    typebeginCS = models.FloatField('Диапазон хлористых солей по описанию типа от', null=True, blank=True)
    typeendCS = models.FloatField('Диапазон хлористых солей по описанию типа до', null=True, blank=True)
    relerrorCS = models.FloatField('Относительная погрешность хлористых солей', null=True, blank=True)
    typebeginS = models.FloatField('Диапазон серы по описанию типа от', null=True, blank=True)
    typeendS = models.FloatField('Диапазон серы по описанию типа до', null=True, blank=True)
    relerrorS = models.FloatField('Относительная погрешность серы', null=True, blank=True)
    typebeginI = models.FloatField('Диапазон мехпримесей по описанию типа от', null=True, blank=True)
    typeendI = models.FloatField('Диапазон мехпримесей по описанию типа до', null=True, blank=True)
    relerrorI = models.FloatField('Относительная погрешность мехпримесей', null=True, blank=True)
    typebeginW = models.FloatField('Диапазон воды по описанию типа от', null=True, blank=True)
    typeendW = models.FloatField('Диапазон воды по описанию типа до', null=True, blank=True)
    relerrorW = models.FloatField('Относительная погрешность воды', null=True, blank=True)

    def __str__(self):
        return f'{self.name} № ГСО {self.number}'

    class Meta:
        verbose_name = 'Название ГСО СС-ТН-ПА(ХПВS)'
        verbose_name_plural = 'Названия  ГСО СС-ТН-ПА(ХПВS)'


class SSTNrange(models.Model):
    nameSM = models.ForeignKey(SSTN, verbose_name='СО', max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    rangeindex = models.CharField('Индекс ГСО', null=True, blank=True)
    name = models.CharField('краткое название ГСО с индексом', max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name}({str(self.rangeindex)})'
        super(SSTNrange, self).save(*args, **kwargs)


    def __str__(self):
        return  f'{self.name}'

    class Meta:
        verbose_name = 'подтип ГСО СС-ТН-ПА-1'
        verbose_name_plural = 'подтипы  ГСО СС-ТН-ПА-1)'
        unique_together = ('nameSM', 'rangeindex')



class LotSSTN(models.Model):
    nameSM = models.ForeignKey(SSTNrange, verbose_name='СО', max_length=100, on_delete=models.PROTECT, null=True, blank=True)
    lot = models.CharField('Партия', max_length=5, null=True, blank=True)
    person = models.ForeignKey(User, verbose_name='Изготовил', max_length=30,  on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField('Дата изготовления', max_length=30, null=True, blank=True)
    name = models.CharField('имя и партия', max_length=1000, null=True, blank=True)
    availability = models.BooleanField('наличие партии на складе', null=True, blank=True, default=True)


    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name} п. {str(self.lot)}'
        super(LotSSTN, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.nameSM} п. {self.lot}'

    class Meta:
        verbose_name = 'Партия СС-ТН-ПА-1'
        verbose_name_plural = 'Партии СС-ТН-ПА-1)'
        unique_together = ('nameSM', 'lot')

class CVforSSTN(models.Model):
    namelot = models.OneToOneField(LotSSTN, verbose_name='для СО:',
                                on_delete=models.PROTECT, null=True, blank=True, unique=True)
    cvCS = models.CharField('Содержание хлористых солей', max_length=30, blank=True, null=True)
    cvdateCS = models.DateField('Дата измерения хлористых солей', blank=True, null=True)
    cvexpCS = models.IntegerField('Срок годности хлористых солей', blank=True, null=True)
    cvdeadCS = models.DateField('Годен до хлористых солей', blank=True, null=True)
    cvS = models.CharField('Содержание сера', max_length=30, blank=True, null=True)
    cvdateS = models.DateField('Дата измерения сера', blank=True, null=True)
    cvexpS = models.IntegerField('Срок годности сера', blank=True, null=True)
    cvdeadS = models.DateField('Годен до сера', blank=True, null=True)
    cvI = models.CharField('Содержание мехпримесей', max_length=30, blank=True, null=True)
    cvdateI = models.DateField('Дата измерения мехпримесей', blank=True, null=True)
    cvexpI = models.IntegerField('Срок годности мехпримесей', blank=True, null=True)
    cvdeadI = models.DateField('Годен до мехпримесей', blank=True, null=True)
    cvW = models.CharField('Содержание вода', max_length=30, blank=True, null=True)
    cvdateW = models.DateField('Дата измерения вода', blank=True, null=True)
    cvexpW = models.IntegerField('Срок годности водай', blank=True, null=True)
    cvdeadW = models.DateField('Годен до вода', blank=True, null=True)

    def __str__(self):
        return f'АЗ для {self.namelot}'

    class Meta:
        verbose_name = 'СС-ТН-ПА-1, АЗ'
        verbose_name_plural = 'СС-ТН-ПА-1, АЗ'
