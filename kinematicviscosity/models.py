from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import *

CHOICES = (
        ('да', 'Проба содержит октол/нефть'),
        ('нет', 'В пробе нет октола/нефти'),
        ('другое', 'другое'),
    )


class ViscosityMJL(models.Model):
    date = models.DateField('Дата', default=timezone.now)
    name = models.CharField('Наименование', max_length=100, default='0')
    lot = models.CharField('Партия', max_length=100)
    ndocumentoptional = (('ГОСТ 33', 'ГОСТ 33'),
                         ('МИ-01', 'МИ-01'),
                         ('оценка', 'оценка вязкости'))
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=ndocumentoptional, default='МИ-01')
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2, default='0')
    termostatition = models.BooleanField(verbose_name='Термостатировано не менее 20 минут', blank=True)
    temperatureCheck = models.BooleanField(verbose_name='Температура контролируется внешним поверенным термометром', blank=True)
    termometer = models.CharField('Внутренний номер термометра', max_length=10, default='0')
    ViscosimeterNumber1 = models.CharField('Заводской номер вискозиметра № 1', max_length=10, default='0')
    Konstant1 = models.DecimalField('Константа вискозиметра № 1', max_digits=7, decimal_places=6, default='0')
    ViscosimeterNumber2 = models.CharField('Заводской номер вискозиметра № 2', max_length=10, default='0')
    Konstant2 = models.DecimalField('Константа вискозиметра № 2', max_digits=7, decimal_places=6, default='0')
    plustimeminK1T1 = models.DecimalField('Время истечения K1T1, + мин', max_digits=3, decimal_places=0, default=0)
    plustimesekK1T1 = models.DecimalField('Время истечения K1T1, + cек', max_digits=5, decimal_places=2, default=0.00)
    plustimeminK1T2 = models.DecimalField('Время истечения K1T2, + мин', max_digits=3, decimal_places=0, default=0)
    plustimesekK1T2 = models.DecimalField('Время истечения K1T2, + cек', max_digits=5, decimal_places=2, default=0.00)
    plustimeminK2T1 = models.DecimalField('Время истечения K2T1, + мин', max_digits=3, decimal_places=0, default=0)
    plustimesekK2T1 = models.DecimalField('Время истечения K2T1, + cек', max_digits=5, decimal_places=2, default=0.00)
    plustimeminK2T2 = models.DecimalField('Время истечения K2T2, + мин', max_digits=3, decimal_places=0, default=0)
    plustimesekK2T2 = models.DecimalField('Время истечения K2T2, + cек', max_digits=5, decimal_places=2, default=0.00)
    performer = models.ForeignKey(User, on_delete=models.CASCADE)
    timeK1T1_sec = models.DecimalField('Время истечения K1T1, в секундах', max_digits=7, decimal_places=2, default=0.00)
    timeK1T2_sec = models.DecimalField('Время истечения K1T2, в секундах', max_digits=7, decimal_places=2, default=0.00)
    timeK2T1_sec = models.DecimalField('Время истечения K2T1, в секундах', max_digits=7, decimal_places=2, default=0.00)
    timeK2T2_sec = models.DecimalField('Время истечения K2T2, в секундах', max_digits=7, decimal_places=2, default=0.0)
    timeK1_avg = models.DecimalField('Время истечения среднее 1, в секундах', max_digits=7, decimal_places=2, default=0.00)
    timeK2_avg = models.DecimalField('Время истечения среднее 2, в секундах', max_digits=7, decimal_places=2, default=0.00)
    viscosity1 = models.DecimalField('Вязкость кинематическая 1', max_digits=20, decimal_places=7, default=0.0000000)
    viscosity2 = models.DecimalField('Вязкость кинематическая 2', max_digits=20, decimal_places=7, default=0.0000000)
    viscosityAVG = models.DecimalField('Вязкость кинематическая среднее', max_digits=20, decimal_places=7, default=0.0000000)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100,  default='неудовлетворительно')
    cause = models.CharField('Причина', max_length=100, default='')
    delta = models.CharField('Не превышает Δ', max_length=100)
    termostatition_words = models.CharField('Термостатировано не менее 20 минут - словами', max_length=1, default='0')
    constit = models.CharField(max_length=300, choices=CHOICES, default='Проба содержит октол/нефть')
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=2, decimal_places=1, default=0.0)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений', max_digits=5, decimal_places=1, default=0.0)

    def save(self, *args, **kwargs):
        # set the full name whenever the object is saved
        a = (self.plustimeminK1T1 * Decimal(60) + self.plustimesekK1T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
        b = (self.plustimeminK1T2 * Decimal(60) + self.plustimesekK1T2).quantize(Decimal('1.00'), ROUND_HALF_UP)
        c = (self.plustimeminK2T1 * Decimal(60) + self.plustimesekK2T1).quantize(Decimal('1.00'), ROUND_HALF_UP)
        d = (self.plustimeminK2T2 * Decimal(60) + self.plustimesekK2T2).quantize(Decimal('1.00'), ROUND_HALF_UP)
        self.timeK1T1_sec = a
        self.timeK1T2_sec = b
        self.timeK2T1_sec = c
        self.timeK2T2_sec = d
        self.timeK1_avg = ((a + b)/Decimal(2)).quantize(Decimal('1.00'), ROUND_HALF_UP)
        self.timeK2_avg = ((c + d)/Decimal(2)).quantize(Decimal('1.00'), ROUND_HALF_UP)
        self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
        self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
        self.viscosityAVG = ((self.viscosity1 + self.viscosity2)/Decimal(2)).quantize(Decimal('1.0000000'), ROUND_HALF_UP)
        self.accMeasurement = (((((self.viscosity1 - self.viscosity2).copy_abs()) / self.viscosityAVG) * Decimal(100)).quantize(Decimal('1.0'), ROUND_HALF_UP))
        if self.termostatition:
            self.termostatition_words = 'V'
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
            self.cause = 'Причина: различие между измерениями Δ превышает критерий приемлемости измерений r'

        super(ViscosityMJL, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;   {self.date}'


    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('Str', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Измерение кинематической вязкости'
        verbose_name_plural = 'Измерения кинематической вязкости'


