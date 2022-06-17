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

    def __str__(self):
        return f'{self.name} № ГСО {self.number}'

    class Meta:
        verbose_name = 'Название ГСО ВЖ-ПА'
        verbose_name_plural = 'Названия  ГСО ВЖ-ПА'

class VGrange(models.Model):
    nameSM = models.ForeignKey(VG, verbose_name='СО', max_length=100, on_delete=models.CASCADE, null=True, blank=True)
    rangeindex = models.IntegerField('Индекс ГСО', null=True, blank=True)
    name = models.CharField('краткое название ГСО с индексом', max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name}({str(self.rangeindex)})'
        super(VGrange, self).save(*args, **kwargs)


    def __str__(self):
        return  f'{self.name}'

    class Meta:
        verbose_name = 'Диапазон ГСО ВЖ-ПА'
        verbose_name_plural = 'Диапазоны  ГСО ВЖ-ПА'


class CharacterVG(models.Model):
    name = models.CharField('Аттестуемая характеристика', max_length=100, null=True, blank=True, default='')
    expiration = models.CharField(max_length=300, choices=CHOICES, default='6', null=True, verbose_name='Срок годности аттестуемой характеристики в месяцах')


    def __str__(self):
        return f'{self.name} годен {self.expiration} месяцев'

    class Meta:
        verbose_name = 'Аттестуемая характеристика'
        verbose_name_plural = 'Аттестуемые характеристики'


class LotVG(models.Model):
    # viscosity = models.OneToOneField(ViscosityMJL, on_delete=models.CASCADE, null=True, blank=True,
    #                                  verbose_name='Инициатор записи (заполнено, если измерение произошло раньше создания партии)')
    nameVG = models.ForeignKey(VGrange, verbose_name='СО', max_length=100, on_delete=models.PROTECT, null=True, blank=True)
    lot = models.CharField('Партия', max_length=5, null=True, blank=True)
    person = models.ForeignKey(User, verbose_name='Изготовил', max_length=30,  on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField('Дата изготовления', max_length=30, null=True, blank=True)
    name = models.CharField('имя и партия', max_length=1000, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = f'{self.nameVG.name} п. {str(self.lot)}'
        super(LotVG, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nameVG} п. {self.lot}'

    class Meta:
        verbose_name = 'Партия ВЖ'
        verbose_name_plural = 'Партии ВЖ'

class CvKinematicviscosityVG(models.Model):
    namelot = models.ForeignKey(LotVG, verbose_name='Кинематическая вязкость для СО:',
                                on_delete=models.PROTECT, null=True, blank=True)
    cvt20 = models.CharField('Кинематика при 20 - АЗ', max_length=30, blank=True, null=True)
    cvt20date = models.DateField('Кинематика при 20 - дата измерения', blank=True, null=True)
    cvt20exp = models.IntegerField('Кинематика при 20 - срок годности', blank=True, null=True)
    cvt25 = models.CharField('Кинематика при 25 - АЗ', max_length=30, blank=True, null=True)
    cvt25date = models.DateField('Кинематика при 25 - дата измерения', blank=True, null=True)
    cvt25exp = models.IntegerField('Кинематика при 25 - срок годности', blank=True, null=True)
    cvt40 = models.CharField('Кинематика при 40 - АЗ', max_length=30, blank=True, null=True)
    cvt40date = models.DateField('Кинематика при 40 - дата измерения', blank=True, null=True)
    cvt40exp = models.IntegerField('Кинематика при 40 - срок годности', blank=True, null=True)
    cvt50 = models.CharField('Кинематика при 50 - АЗ', max_length=30, blank=True, null=True)
    cvt50date = models.DateField('Кинематика при 50 - дата измерения', blank=True, null=True)
    cvt50exp = models.IntegerField('Кинематика при 50 - срок годности', blank=True, null=True)
    cvt60 = models.CharField('Кинематика при 60 - АЗ', max_length=30, blank=True, null=True)
    cvt60date = models.DateField('Кинематика при 60 - дата измерения', blank=True, null=True)
    cvt60exp = models.IntegerField('Кинематика при 60 - срок годности', blank=True, null=True)
    cvt80 = models.CharField('Кинематика при 80 - АЗ', max_length=30, blank=True, null=True)
    cvt80date = models.DateField('Кинематика при 80 - дата измерения', blank=True, null=True)
    cvt80exp = models.IntegerField('Кинематика при 80 - срок годности', blank=True, null=True)
    cvt100 = models.CharField('Кинематика при 100 - АЗ', max_length=30, blank=True, null=True)
    cvt100date = models.DateField('Кинематика при 100 - дата измерения', blank=True, null=True)
    cvt100exp = models.IntegerField('Кинематика при 100 - срок годности', blank=True, null=True)
    cvt150 = models.CharField('Кинематика при 150 - АЗ', max_length=30, blank=True, null=True)
    cvt150date = models.DateField('Кинематика при 150 - дата измерения', blank=True, null=True)
    cvt150exp = models.IntegerField('Кинематика при 150 - срок годности', blank=True, null=True)
    cvtminus20 = models.CharField('Кинематика при -20 - АЗ', max_length=30, blank=True, null=True)
    cvtminus20date = models.DateField('Кинематика при -20 - дата измерения', blank=True, null=True)
    cvtminus20exp = models.IntegerField('Кинематика при -20 - срок годности', blank=True, null=True)

    def __str__(self):
        return f'{self.namelot}'

    class Meta:
        verbose_name = 'ВЖ-ПА, кинематика'
        verbose_name_plural = 'ВЖ-ПА, кинематика'





