from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from metods import get_avg, get_acc_measurement
from formuls import mrerrow, numberDigits

from viscosimeters.models import Viscosimeters, Kalibration


CHOICES = (
    ('да', 'Проба содержит октол/нефть'),
    ('нет', 'В пробе нет октола/нефти'),
    ('другое', 'другое'),
)

DENSITYE = (
    ('денсиметром', 'денсиметром'),
    ('пикнометром', 'пикнометром'),
)

DOCUMENTS = (('МИ-02-2018', 'МИ-02-2018'),)

RELERROR = 0.3  # относительная погрешность СО из описания типа


class Dinamicviscosity(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performer', blank=True)
    performerdensity = models.ForeignKey(User, verbose_name='Плотность измерил', on_delete=models.CASCADE, null=True, related_name='performerdensity', blank=True)
    name = models.CharField('Наименование', max_length=100, default='0', null=True, blank=True)
    lot = models.CharField('Партия', max_length=100, null=True, blank=True)
    constit = models.CharField('Состав пробы', max_length=300, choices=CHOICES, default='Проба содержит октол/нефть', null=True,  blank=True)
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=DOCUMENTS, default='МИ-02-2018', blank=True)
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2, default='0', null=True,
                                      blank=True)
    piknometer_volume = models.DecimalField('Объём пикнометра, мл', max_digits=7, decimal_places=4, null=True,
                                            blank=True)
    piknometer_mass1 = models.DecimalField('Масса пикнометра 1, г', max_digits=7, decimal_places=4, null=True,
                                           blank=True)
    piknometer_mass2 = models.DecimalField('Масса пикнометра 2, г', max_digits=7, decimal_places=4, null=True,
                                           blank=True)
    piknometer_plus_SM_mass1 = models.DecimalField('Масса пикнометра + СО -  1, г', max_digits=7, decimal_places=4,
                                                   null=True, blank=True)
    piknometer_plus_SM_mass2 = models.DecimalField('Масса пикнометра + СО -  2, г', max_digits=7, decimal_places=4,
                                                   null=True, blank=True)
    SM_mass1 = models.DecimalField('Масса СО -  1, г', max_digits=7, decimal_places=4, null=True, blank=True)
    SM_mass2 = models.DecimalField('Масса СО -  2, г', max_digits=7, decimal_places=4, null=True, blank=True)
    density1 = models.DecimalField('плотность 1, г/мл', max_digits=7, decimal_places=5, null=True, blank=True)
    density2 = models.DecimalField('плотность 2, г/мл', max_digits=7, decimal_places=5, null=True, blank=True)
    density_avg = models.DecimalField('плотность 2, г/мл', max_digits=7, decimal_places=4, null=True, blank=True)
    delta = models.CharField('Не превышает Δ', max_length=100, null=True, blank=True)
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=2, decimal_places=1, null=True,
                                   blank=True)
    kinematicviscosity = models.FloatField('Кинематическая вязкость при температуре измерений сСт', null=True,
                                           blank=True)
    dinamicviscosity_not_rouned = models.DecimalField('Динамическая вязкость неокругленная', max_digits=20,
                                                      decimal_places=6, null=True, blank=True)
    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True,  blank=True,
                                   default=RELERROR)
    certifiedValue = models.FloatField('Аттестованное значение динамической вязкости', null=True,
                                         blank=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений плотности', max_digits=5, decimal_places=1, null=True,
                                         blank=True)
    abserror = models.FloatField('Абсолютная  погрешность', null=True, blank=True)
    olddensity = models.CharField('Предыдущее значение плотности', max_length=300, null=True, default='', blank=True)
    deltaolddensity = models.DecimalField('Оценка разницы с предыдущим значением плотности',
                                                 max_digits=10, decimal_places=2, null=True, blank=True)
    resultWarning = models.CharField(max_length=300, default='', null=True, blank=True)
    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False,
                                   null=True, blank=True)
    equipment = models.CharField('Способ измерения плотности', max_length=300, choices=DENSITYE, default='денсиметром', null=True,  blank=True)

    def save(self, *args, **kwargs):
        if not (self.density1 and self.density2):
            self.SM_mass1 = self.piknometer_plus_SM_mass1 - self.piknometer_mass1
            self.SM_mass2 = self.piknometer_plus_SM_mass2 - self.piknometer_mass2
            self.density1 = self.SM_mass1 / self.piknometer_volume
            self.density2 = self.SM_mass2 / self.piknometer_volume
        self.density_avg = get_avg(self.density1, self.density2, 4)
        if self.constit == 'да':
            self.kriteriy = Decimal(0.3)
        if self.constit == 'нет':
            self.kriteriy = Decimal(0.2)
        if self.constit == 'другое':
            self.kriteriy = Decimal(0.3)
        self.accMeasurement = get_acc_measurement(self.density1, self.density2)
        if self.accMeasurement < self.kriteriy:
            self.resultMeas = 'удовлетворительно'
            self.cause = ''
        if self.accMeasurement > self.kriteriy:
            self.resultMeas = 'неудовлетворительно'
            self.cause = 'Δ > r'
        if self.resultMeas == 'удовлетворительно':
            #если результаты сходимы, то вычисляем АЗ:
            self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
            self.abserror = mrerrow((Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
            self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
        # если указано предыдущее значение плотности, и есть измеренное АЗ, то вычисляем разницу с ним:
        if self.olddensity and self.certifiedValue:
            self.deltaolddensity = get_acc_measurement(Decimal(self.olddensity), self.density_avg)
            if self.deltaolddensity > Decimal(0.7):
                self.resultWarning = 'плотность отличается от предыдущей на > 0,7 %. Рекомендовано измерить повторно'
        super(Dinamicviscosity, self).save(*args, **kwargs)



    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('str', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Измерение плотности и расчёт динамической вязкости'
        verbose_name_plural = 'Измерения плотности и расчёт динамической вязкост'


class CommentsDinamicviscosity(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Dinamicviscosity, verbose_name='К странице аттестации', on_delete=models.CASCADE,
                                related_name='comments')
    author = models.ForeignKey(User, verbose_name='Наименование', on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.author.username} , {self.forNote.name},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('comm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']
