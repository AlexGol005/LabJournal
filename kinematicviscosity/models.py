from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from decimal import *
from django.db.models import Max


from viscosimeters.models import Viscosimeters, Kalibration
from formuls import mrerrow, numberDigits
from datetime import datetime, timedelta



CHOICES = (
        ('да', 'Проба содержит октол/нефть'),
        ('нет', 'В пробе нет октола/нефти'),
        ('другое', 'другое'),
    )


class ViscosityMJL(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.CharField('Наименование', max_length=100, default='0', null=True)
    lot = models.CharField('Партия', max_length=100, null=True)
    ndocumentoptional = (('ГОСТ 33', 'ГОСТ 33'),
                         ('МИ-01', 'МИ-01'),
                         ('оценка', 'оценка вязкости'))
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=ndocumentoptional, default='МИ-01')
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2, default='0', null=True)
    termostatition = models.BooleanField(verbose_name='Термостатировано не менее 20 минут', blank=True, null=True)
    temperatureCheck = models.BooleanField(verbose_name='Температура контролируется внешним поверенным термометром', blank=True, null=True)
    termometer = models.CharField('Внутренний номер термометра', max_length=10, default='0', null=True)
    ViscosimeterNumber1 = models.CharField('Заводской номер вискозиметра № 1', max_length=10, default='0', null=True)  # todo ForeignKey
    Konstant1 = models.DecimalField('Константа вискозиметра № 1', max_digits=20, decimal_places=6, default='0', null=True)
    ViscosimeterNumber2 = models.CharField('Заводской номер вискозиметра № 2', max_length=10, default='0', null=True)
    Konstant2 = models.DecimalField('Константа вискозиметра № 2', max_digits=20, decimal_places=6, default='0', null=True)
    plustimeminK1T1 = models.DecimalField('Время истечения K1T1, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK1T1 = models.DecimalField('Время истечения K1T1, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK1T2 = models.DecimalField('Время истечения K1T2, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK1T2 = models.DecimalField('Время истечения K1T2, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK2T1 = models.DecimalField('Время истечения K2T1, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK2T1 = models.DecimalField('Время истечения K2T1, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK2T2 = models.DecimalField('Время истечения K2T2, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK2T2 = models.DecimalField('Время истечения K2T2, + cек', max_digits=5, decimal_places=2, null=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timeK1T1_sec = models.DecimalField('Время истечения K1T1, в секундах', max_digits=7, decimal_places=2, default=0.00, null=True)
    timeK1T2_sec = models.DecimalField('Время истечения K1T2, в секундах', max_digits=7, decimal_places=2, default=0.00, null=True)
    timeK2T1_sec = models.DecimalField('Время истечения K2T1, в секундах', max_digits=7, decimal_places=2, default=0.00, null=True)
    timeK2T2_sec = models.DecimalField('Время истечения K2T2, в секундах', max_digits=7, decimal_places=2, default=0.0, null=True)
    timeK1_avg = models.DecimalField('Время истечения среднее 1, в секундах', max_digits=7, decimal_places=2, default=0.00, null=True)
    timeK2_avg = models.DecimalField('Время истечения среднее 2, в секундах', max_digits=7, decimal_places=2, default=0.00, null=True)
    viscosity1 = models.DecimalField('Вязкость кинематическая 1', max_digits=20, decimal_places=5, default=0.0000000, null=True)
    viscosity2 = models.DecimalField('Вязкость кинематическая 2', max_digits=20, decimal_places=5, default=0.0000000, null=True)
    viscosityAVG = models.DecimalField('Вязкость кинематическая среднее', max_digits=20, decimal_places=5, default=0.0000000, null=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100,  default='неудовлетворительно', null=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True)
    delta = models.CharField('Не превышает Δ', max_length=100, null=True)
    termostatition_words = models.CharField('Термостатировано не менее 20 минут - словами', max_length=1, null=True)
    constit = models.CharField(max_length=300, choices=CHOICES, default='Проба содержит октол/нефть', null=True)
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=2, decimal_places=1, null=True)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений', max_digits=5, decimal_places=1, null=True)
    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True, default=0.3)
    abserror = models.FloatField('Абсолютная  погрешность', null=True)
    abserror_text = models.CharField(max_length=300, default='', null=True)
    certifiedValue = models.DecimalField('Аттестованное значение', max_digits=20, decimal_places=10, null=True)
    certifiedValue_text = models.CharField(max_length=300, default='', null=True)
    oldCertifiedValue = models.CharField('Предыдущее аттестованное значение', max_length=300, null=True,  default='')
    deltaOldCertifiedValue = models.DecimalField('Оценка разницы с предыдущим значением',
                                                 max_digits=10, decimal_places=4, null=True)
    deltaOldCertifiedValue_text = models.CharField(max_length=300, default='', null=True)
    resultWarning = models.CharField(max_length=300, default='', null=True)
    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False, null=True)

    def save(self, *args, **kwargs):
        if (self.plustimeminK1T2 and self.plustimesekK1T2 and self.plustimeminK2T1 and
                self.plustimesekK2T1 and self.plustimeminK2T2 and self.plustimesekK2T2 and self.plustimeminK1T1 and
                self.plustimesekK1T1):
            # a = self._get_avg_time(self.plustimeminK1T1, self.plustimesekK1T1)
            a = (self.plustimeminK1T1 * Decimal(60) + self.plustimesekK1T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
            b = (self.plustimeminK1T2 * Decimal(60) + self.plustimesekK1T2).quantize(Decimal('1.00'), ROUND_HALF_UP)
            c = (self.plustimeminK2T1 * Decimal(60) + self.plustimesekK2T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
            d = (self.plustimeminK2T2 * Decimal(60) + self.plustimesekK2T2).quantize(Decimal('1.00'), ROUND_HALF_UP)
            self.timeK1T1_sec = a
            self.timeK1T2_sec = b
            self.timeK2T1_sec = c
            self.timeK2T2_sec = d
            self.timeK1_avg = ((a + b)/Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
            self.timeK2_avg = ((c + d)/Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = ((self.viscosity1 + self.viscosity2) / Decimal(2)).quantize(Decimal('1.0000000'), ROUND_HALF_UP)
            self.accMeasurement = ((((self.viscosity1 - self.viscosity2).copy_abs()) / self.viscosityAVG) * Decimal(100)).quantize(Decimal('1.0'), ROUND_HALF_UP)
            if self.constit == 'да':
                self.kriteriy = Decimal(0.3)
            if self.constit == 'нет':
                self.kriteriy = Decimal(0.2)
            if self.constit == 'другое':
                self.kriteriy = Decimal(0.3)
            if self.accMeasurement < self.kriteriy:
                self.resultMeas = 'удовлетворительно'
                self.cause = ''
            if self.accMeasurement > self.kriteriy:
                self.resultMeas = 'неудовлетворительно'
                self.cause = 'Δ > r'
        if (self.plustimeminK1T1 and self.plustimesekK1T1) and\
                not (self.plustimeminK1T2 and self.plustimesekK1T2 and self.plustimeminK2T2 and self.plustimesekK2T2 and self.plustimeminK2T2 and self.plustimesekK2T2):
            a = (self.plustimeminK1T1 * Decimal(60) + self.plustimesekK1T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
            self.timeK1T1_sec = a
            self.timeK1_avg = a
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = self.viscosity1
            self.accMeasurement = 0
            self.resultMeas = 'экспрес оценка вязкости'
            self.cause = 'не в условиях повторяемости'
        if (self.plustimeminK1T1 and self.plustimesekK1T1 and self.plustimeminK2T1 and self.plustimesekK2T1)\
                and not (self.plustimeminK1T2 and self.plustimesekK1T2 and self.plustimeminK2T2 and \
                self.plustimesekK2T2):
            a = (self.plustimeminK1T1 * Decimal(60) + self.plustimesekK1T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
            c = (self.plustimeminK2T1 * Decimal(60) + self.plustimesekK2T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
            self.timeK1T1_sec = a
            self.timeK2T1_sec = c
            self.timeK1_avg = a
            self.timeK2_avg = c
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP) # todo  self.Konstant1 -> self.ViscosimeterNumber1.Konstant1 когда поеле ForeignKey
            self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = ((self.viscosity1 + self.viscosity2) / Decimal(2)).quantize(Decimal('1.0000000'), ROUND_HALF_UP)
            self.accMeasurement = ((((self.viscosity1 - self.viscosity2).copy_abs()) / self.viscosityAVG) * Decimal(100)).quantize(Decimal('1.0'), ROUND_HALF_UP)
            if self.constit == 'да':
                self.kriteriy = Decimal(0.3)
            if self.constit == 'нет':
                self.kriteriy = Decimal(0.2)
            if self.constit == 'другое':
                self.kriteriy = Decimal(0.3)
            if self.accMeasurement < self.kriteriy:
                self.resultMeas = 'удовлетворительно'
                self.cause = ''
            if self.accMeasurement > self.kriteriy:
                self.resultMeas = 'неудовлетворительно'
                self.cause = ':  Δ > r'
        if self.termostatition:
            self.termostatition_words = 'V'
        if self.resultMeas == 'удовлетворительно':
            self.abserror = mrerrow((Decimal(self.relerror) * self.viscosityAVG) / Decimal(100))
            self.certifiedValue = numberDigits(self.viscosityAVG, self.abserror)
            self.certifiedValue_text = str(self.certifiedValue)
            if self.oldCertifiedValue:
                self.deltaOldCertifiedValue = (((((Decimal(self.oldCertifiedValue) - self.certifiedValue).copy_abs())/((Decimal(self.oldCertifiedValue)
                    + self.certifiedValue)/Decimal(2)))) * Decimal('100')).quantize(Decimal('1.00'), ROUND_HALF_UP)
        if self.abserror == None:
            self.abserror_text = ''
        if self.abserror:
            self.abserror_text = str(self.abserror)
        if self.deltaOldCertifiedValue == None:
            self.deltaOldCertifiedValue_text = ''
        if self.deltaOldCertifiedValue:
            self.deltaOldCertifiedValue_text = str(self.deltaOldCertifiedValue)
        if self.deltaOldCertifiedValue:
            if self.deltaOldCertifiedValue > Decimal(0.7):
                self.resultWarning = 'Результат отличается от предыдущего > 0,7 %. Рекомендовано измерить повторно.'

        super(ViscosityMJL, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;   {self.date}'

    @staticmethod
    def _get_avg_time(minutes: Decimal, seconds: Decimal):
        """

        :param minutes:
        :param seconds:
        :return:
        """
        time = (minutes * Decimal(60) + seconds).quantize(Decimal('1.00'), ROUND_HALF_UP)
        return time


    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('Str', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Измерение кинематической вязкости'
        verbose_name_plural = 'Измерения кинематической вязкости'

class CommentsKinematicviscosity(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(ViscosityMJL, verbose_name='К странице аттестации',  on_delete=models.CASCADE, related_name='comments')
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






