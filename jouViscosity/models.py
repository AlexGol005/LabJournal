from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth.models import User



CHOICES = (
        ('6', '6'),
        ('12', '12'),
        ('24', '24'),
    )



class VG(models.Model):
    name = models.CharField('Название СО краткое', max_length=100, null=True, blank=True, default='')
    fullname = models.CharField('Название СО полное', max_length=100, null=True, blank=True, default='')
    number = models.CharField('Номер ГСО', max_length=100, null=True, blank=True, default='')
    expiration = models.CharField('Срок годности ГСО', max_length=100, null=True, blank=True, default='')
    typebegin = models.FloatField('Диапазон по описанию типа от', null=True, blank=True)
    typeend = models.FloatField('Диапазон по описанию типа до', null=True, blank=True)
    relerror = models.FloatField('Относительная погрешность', null=True, blank=True)

    def __str__(self):
        return f'{self.name} № ГСО {self.number}'

    class Meta:
        verbose_name = 'Название ГСО ВЖ-ПА'
        verbose_name_plural = 'Названия  ГСО ВЖ-ПА'


class VGrange(models.Model):
    nameSM = models.ForeignKey(VG, verbose_name='СО', max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    rangeindex = models.IntegerField('Индекс ГСО', null=True, blank=True)
    name = models.CharField('краткое название ГСО с индексом', max_length=100, null=True, blank=True)
    pricebegin = models.FloatField('Диапазон по прайсу от', null=True, blank=True)
    priceend = models.FloatField('Диапазон по прайсу до', null=True, blank=True)



    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name}({str(self.rangeindex)})'
        super(VGrange, self).save(*args, **kwargs)


    def __str__(self):
        return  f'{self.name}'

    class Meta:
        verbose_name = 'Диапазон ГСО ВЖ-ПА'
        verbose_name_plural = 'Диапазоны  ГСО ВЖ-ПА'
        unique_together = ('nameSM', 'rangeindex')


class CharacterVG(models.Model):
    name = models.CharField('Аттестуемая характеристика', max_length=100, null=True, blank=True, default='')
    expiration = models.CharField(max_length=300, choices=CHOICES, default='6', null=True, verbose_name='Срок годности аттестуемой характеристики в месяцах')


    def __str__(self):
        return f'{self.name} годен {self.expiration} месяцев'

    class Meta:
        verbose_name = 'Аттестуемая характеристика'
        verbose_name_plural = 'Аттестуемые характеристики'



class LotVG(models.Model):
    nameVG = models.ForeignKey(VGrange, verbose_name='СО', max_length=100, on_delete=models.PROTECT, null=True, blank=True)
    lot = models.CharField('Партия', max_length=5, null=True, blank=True)
    person = models.ForeignKey(User, verbose_name='Изготовил', max_length=30,  on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField('Дата изготовления', max_length=30, null=True, blank=True)
    name = models.CharField('имя и партия', max_length=1000, null=True, blank=True)
    availability = models.BooleanField('наличие партии на складе', null=True, blank=True, default=True)


    def save(self, *args, **kwargs):
        self.name = f'{self.nameVG.name} п. {str(self.lot)}'
        super(LotVG, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.nameVG} п. {self.lot}'

    class Meta:
        verbose_name = 'Партия ВЖ'
        verbose_name_plural = 'Партии ВЖ'
        unique_together = ('nameVG', 'lot')

class CvKinematicviscosityVG(models.Model):
    namelot = models.OneToOneField(LotVG, verbose_name='Кинематическая вязкость для СО:',
                                on_delete=models.PROTECT, null=True, blank=True)
    cvt20 = models.CharField('Кинематика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt20date = models.DateField('Кинематика при 20 - дата измерения', blank=True, null=True)
    cvt20exp = models.IntegerField('Кинематика при 20 - срок годности', blank=True, null=True)
    cvt20dead = models.DateField('20 годен до', blank=True, null=True)

    cvt25 = models.CharField('Кинематика при 25 - АЗ', max_length=30, blank=True, null=True)
    cvt25date = models.DateField('Кинематика при 25 - дата измерения', blank=True, null=True)
    cvt25exp = models.IntegerField('Кинематика при 25 - срок годности', blank=True, null=True)
    cvt25dead = models.DateField('25 годен до', blank=True, null=True)

    cvt40 = models.CharField('Кинематика при 40 - АЗ', max_length=30, blank=True, null=True)
    cvt40date = models.DateField('Кинематика при 40 - дата измерения', blank=True, null=True)
    cvt40exp = models.IntegerField('Кинематика при 40 - срок годности', blank=True, null=True)
    cvt40dead = models.DateField('40 годен до', blank=True, null=True)

    cvt50 = models.CharField('Кинематика при 50 - АЗ', max_length=30, blank=True, null=True)
    cvt50date = models.DateField('Кинематика при 50 - дата измерения', blank=True, null=True)
    cvt50exp = models.IntegerField('Кинематика при 50 - срок годности', blank=True, null=True)
    cvt50dead = models.DateField('50 годен до', blank=True, null=True)

    cvt60 = models.CharField('Кинематика при 60 - АЗ', max_length=30, blank=True, null=True)
    cvt60date = models.DateField('Кинематика при 60 - дата измерения', blank=True, null=True)
    cvt60exp = models.IntegerField('Кинематика при 60 - срок годности', blank=True, null=True)
    cvt60dead = models.DateField('60 годен до', blank=True, null=True)

    cvt80 = models.CharField('Кинематика при 80 - АЗ', max_length=30, blank=True, null=True)
    cvt80date = models.DateField('Кинематика при 80 - дата измерения', blank=True, null=True)
    cvt80exp = models.IntegerField('Кинематика при 80 - срок годности', blank=True, null=True)
    cvt80dead = models.DateField('80 годен до', blank=True, null=True)

    cvt100 = models.CharField('Кинематика при 100 - АЗ', max_length=30, blank=True, null=True)
    cvt100date = models.DateField('Кинематика при 100 - дата измерения', blank=True, null=True)
    cvt100exp = models.IntegerField('Кинематика при 100 - срок годности', blank=True, null=True)
    cvt100dead = models.DateField('100 годен до', blank=True, null=True)

    cvt150 = models.CharField('Кинематика при 150 - АЗ', max_length=30, blank=True, null=True)
    cvt150date = models.DateField('Кинематика при 150 - дата измерения', blank=True, null=True)
    cvt150exp = models.IntegerField('Кинематика при 150 - срок годности', blank=True, null=True)
    cvt150dead = models.DateField('150 годен до', blank=True, null=True)

    cvtminus20 = models.CharField('Кинематика при -20 - АЗ', max_length=30, blank=True, null=True)
    cvtminus20date = models.DateField('Кинематика при -20 - дата измерения', blank=True, null=True)
    cvtminus20exp = models.IntegerField('Кинематика при -20 - срок годности', blank=True, null=True)
    cvtminus20dead = models.DateField('-20 годен до', blank=True, null=True)


    def __str__(self):
        return f'кинематика АЗ для {self.namelot}'

    class Meta:
        verbose_name = 'ВЖ-ПА, кинематика'
        verbose_name_plural = 'ВЖ-ПА, кинематика'

class CvDensityDinamicVG(models.Model):
    namelot = models.OneToOneField(LotVG, verbose_name='Плотность и динамика для СО:',
                                   on_delete=models.PROTECT, null=True, blank=True)
    cvt20 = models.CharField('Плотность при 20 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic20 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt20date = models.DateField('Плотность при 20 - дата измерения', blank=True, null=True)
    cvt20exp = models.IntegerField('Плотность при 20 - срок годности', blank=True, null=True)
    cvt20dead = models.DateField('20 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead20 = models.DateField('кинематика 20 годен до', blank=True, null=True)
    cvt25 = models.CharField('Плотность при 25 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic25 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt25date = models.DateField('Плотность при 25 - дата измерения', blank=True, null=True)
    cvt25exp = models.IntegerField('Плотность при 25 - срок годности', blank=True, null=True)
    cvt25dead = models.DateField('25 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead25 = models.DateField('кинематика 25 годен до', blank=True, null=True)
    cvt40 = models.CharField('Плотность при 40 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic40 = models.CharField('Динамика при 40 - АЗ', max_length=30, blank=True, null=True)
    cvt40date = models.DateField('Плотность при 40 - дата измерения', blank=True, null=True)
    cvt40exp = models.IntegerField('Плотность при 40 - срок годности', blank=True, null=True)
    cvt40dead = models.DateField('40 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead40 = models.DateField('кинематика 40 годен до', blank=True, null=True)
    cvt50 = models.CharField('Плотность при 50 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic50 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt50date = models.DateField('Плотность при 50 - дата измерения', blank=True, null=True)
    cvt50exp = models.IntegerField('Плотность при 50 - срок годности', blank=True, null=True)
    cvt50dead = models.DateField('50 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead50 = models.DateField('кинематика 50 годен до', blank=True, null=True)
    cvt60 = models.CharField('Плотность при 60 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic60 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt60date = models.DateField('Плотность при 60 - дата измерения', blank=True, null=True)
    cvt60exp = models.IntegerField('Плотность при 60 - срок годности', blank=True, null=True)
    cvt60dead = models.DateField('60 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead60 = models.DateField('кинематика 60 годен до', blank=True, null=True)
    cvt80 = models.CharField('Плотность при 80 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic80 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt80date = models.DateField('Плотность при 80 - дата измерения', blank=True, null=True)
    cvt80exp = models.IntegerField('Плотность при 80 - срок годности', blank=True, null=True)
    cvt80dead = models.DateField('80 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead80 = models.DateField('кинематика 80 годен до', blank=True, null=True)
    cvt100 = models.CharField('Плотность при 100 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic100 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt100date = models.DateField('Плотность при 100 - дата измерения', blank=True, null=True)
    cvt100exp = models.IntegerField('Плотность при 100 - срок годности', blank=True, null=True)
    cvt100dead = models.DateField('100 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead100 = models.DateField('кинематика 100 годен до', blank=True, null=True)
    cvt150 = models.CharField('Плотность при 150 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamic150 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt150date = models.DateField('Плотность при 150 - дата измерения', blank=True, null=True)
    cvt150exp = models.IntegerField('Плотность при 150 - срок годности', blank=True, null=True)
    cvt150dead = models.DateField('150 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdead150 = models.DateField('кинематика 150 годен до', blank=True, null=True)
    cvtminus20 = models.CharField('Плотность при -20 - АЗ', max_length=30, blank=True, null=True)
    cvtdinamicminus20 = models.CharField('Динамика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvtminus20date = models.DateField('Плотность при -20 - дата измерения', blank=True, null=True)
    cvtminus20exp = models.IntegerField('Плотность при -20 - срок годности', blank=True, null=True)
    cvtminus20dead = models.DateField('-20 плотность годен до', blank=True, null=True)
    kinematicviscosityfordinamicdeadminus20 = models.DateField('кинематика -20 годен до', blank=True, null=True)

    def __str__(self):
        return f'плотность и динамика АЗ для {self.namelot}'

    class Meta:
        verbose_name = 'ВЖ-ПА, плотность и динамика'
        verbose_name_plural = 'ВЖ-ПА, плотность и динамика'






