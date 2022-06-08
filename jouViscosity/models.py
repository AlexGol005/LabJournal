from django.db import models
from django.contrib.auth.models import User

from kinematicviscosity.models import ViscosityMJL

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
    rangeindex = models.CharField('Индекс ГСО', max_length=100, null=True, blank=True)
    name = models.CharField('краткое название ГСО с индексом', max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = f'{self.nameSM.name}({self.rangeindex})'
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
    viscosity = models.OneToOneField(ViscosityMJL, on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name='Инициатор записи (заполнено, если измерение произошло раньше создания партии)')
    nameVG = models.ForeignKey(VGrange, verbose_name='СО', max_length=100, on_delete=models.PROTECT, null=True, blank=True)
    lot = models.CharField('Партия', max_length=5, null=True, blank=True)
    person = models.ForeignKey(User, verbose_name='Изготовил', max_length=30,  on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField('Дата изготовления', max_length=30, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.viscosity:
            self.lot = self.viscosity.lot
            # self.nameVG = VGrange.objects.get(name=self.viscosity.name)

        super(LotVG, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nameVG} п. {self.lot}'



    class Meta:
        verbose_name = 'Партия ВЖ'
        verbose_name_plural = 'Партии ВЖ'




