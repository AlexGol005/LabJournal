from datetime import timedelta, date

from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from viscosimeters.models import Viscosimeters, Kalibration
from jouViscosity.models import LotVG, VGrange, VG, CvKinematicviscosityVG
from formuls import mrerrow, numberDigits
from metods import get_sec, get_avg, get_acc_measurement

RELERROR = 0.3  # относительная погрешность

ndocumentoptional = (
    ('МИ-02-2018', 'МИ-02-2018'),
    ('оценка', 'оценка вязкости'),
    ('ГОСТ 33', 'ГОСТ 33'))  # нормативные документы

CHOICES = (
    ('да', 'Проба содержит октол/нефть'),
    ('нет', 'В пробе нет октола/нефти'),
    ('другое', 'другое'),
)


class ViscosityMJL(models.Model):
    """уникальный класс, хранит первичные данные измерения и вычисляет результаты"""
    # поля для всех моделей
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.CharField('Наименование', max_length=100, default='0', null=True)
    lot = models.CharField('Партия', max_length=100, null=True)
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=ndocumentoptional,
                                 default=ndocumentoptional[0][0],
                                 blank=True, null=True)
    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True,
                                   default=RELERROR)
    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False,
                                   null=True)
    for_lot_and_name = models.ForeignKey(LotVG, verbose_name='Измерение для: ГСО и партия', on_delete=models.PROTECT, blank=True, null=True)
    exp = models.IntegerField('Срок годности, месяцев',  blank=True, null=True)
    date_exp = models.DateField('Годен до', blank=True, null=True)
    # вычисляемые поля для всех моделей
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=2, decimal_places=1, null=True)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений', max_digits=5, decimal_places=1, null=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    abserror = models.CharField('Абсолютная  погрешность',  max_length=100, null=True)
    certifiedValue = models.DecimalField('Аттестованное значение', max_digits=100, decimal_places=10, null=True)
    certifiedValue_text = models.CharField(max_length=300, default='', null=True)
    # уникальные поля (первичные данные)
    oldCertifiedValue = models.CharField('Предыдущее аттестованное значение',  null=True, blank=True, max_length=300, default='')
    termostatition = models.BooleanField(verbose_name='Термостатировано не менее 20 минут', blank=True, null=True)
    temperatureCheck = models.BooleanField(verbose_name='Температура контролируется внешним поверенным термометром',
                                           blank=True, null=True)
    constit = models.CharField(max_length=300, choices=CHOICES, default='Проба содержит октол/нефть', null=True)
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2, default='0', null=True)
    ViscosimeterNumber1 = models.ForeignKey(Viscosimeters, verbose_name='Заводской номер вискозиметра № 1',
                                            on_delete=models.PROTECT, related_name='k1', blank=True)
    Konstant1 = models.DecimalField('Константа вискозиметра № 1', max_digits=20, decimal_places=6, default='0',
                                    null=True, blank=True)
    ViscosimeterNumber2 = models.ForeignKey(Viscosimeters, verbose_name='Заводской номер вискозиметра № 2',
                                            on_delete=models.PROTECT, related_name='k2', blank=True)
    Konstant2 = models.DecimalField('Константа вискозиметра № 2', max_digits=20, decimal_places=6, default='0',
                                    null=True, blank=True)
    plustimeminK1T1 = models.DecimalField('Время истечения K1T1, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK1T1 = models.DecimalField('Время истечения K1T1, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK1T2 = models.DecimalField('Время истечения K1T2, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK1T2 = models.DecimalField('Время истечения K1T2, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK2T1 = models.DecimalField('Время истечения K2T1, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK2T1 = models.DecimalField('Время истечения K2T1, + cек', max_digits=5, decimal_places=2, null=True)
    plustimeminK2T2 = models.DecimalField('Время истечения K2T2, + мин', max_digits=3, decimal_places=0, null=True)
    plustimesekK2T2 = models.DecimalField('Время истечения K2T2, + cек', max_digits=5, decimal_places=2, null=True)
    # уникальные вычисляемые поля (расчёты)
    timeK1T1_sec = models.DecimalField('Время истечения K1T1, в секундах', max_digits=7, decimal_places=2, default=0.00,
                                       null=True)
    timeK1T2_sec = models.DecimalField('Время истечения K1T2, в секундах', max_digits=7, decimal_places=2, default=0.00,
                                       null=True)
    timeK2T1_sec = models.DecimalField('Время истечения K2T1, в секундах', max_digits=7, decimal_places=2, default=0.00,
                                       null=True)
    timeK2T2_sec = models.DecimalField('Время истечения K2T2, в секундах', max_digits=7, decimal_places=2, default=0.0,
                                       null=True)
    timeK1_avg = models.DecimalField('Время истечения среднее 1, в секундах', max_digits=7, decimal_places=2,
                                     default=0.00, null=True)
    timeK2_avg = models.DecimalField('Время истечения среднее 2, в секундах', max_digits=7, decimal_places=2,
                                     default=0.00, null=True)
    viscosity1 = models.DecimalField('Вязкость кинематическая 1', max_digits=20, decimal_places=5, default=0.0000000,
                                     null=True)
    viscosity2 = models.DecimalField('Вязкость кинематическая 2', max_digits=20, decimal_places=5, default=0.0000000,
                                     null=True)
    viscosityAVG = models.DecimalField('Вязкость кинематическая среднее', max_digits=20, decimal_places=5,
                                       default=0.0000000, null=True)
    deltaOldCertifiedValue = models.DecimalField('Оценка разницы с предыдущим значением',
                                                 max_digits=10, decimal_places=2, null=True, blank=True)
    resultWarning = models.CharField(max_length=300, default='', null=True,  blank=True)


    def save(self, *args, **kwargs):
    # срок годности зависит от диапазона ВЖ
        if self.name[0:2] == 'ВЖ':
            if int(self.name[8:-1]) <= 10:
                self.exp = 6
            if int(self.name[8:-1]) > 10:
                self.exp = 12
    # переводим минуты в секунды
        if (self.plustimeminK1T2 and self.plustimesekK1T2 and self.plustimeminK2T1 and self.plustimesekK2T1
                and self.plustimeminK2T2 and self.plustimesekK2T2 and self.plustimeminK1T1 and self.plustimesekK1T1):
            self.timeK1T1_sec = get_sec(self.plustimeminK1T1, self.plustimesekK1T1)
            self.timeK1T2_sec = get_sec(self.plustimeminK1T2, self.plustimesekK1T2)
            self.timeK2T1_sec = get_sec(self.plustimeminK2T1, self.plustimesekK2T1)
            self.timeK2T2_sec = get_sec(self.plustimeminK2T2, self.plustimesekK2T2)
            self.timeK1_avg = get_avg(self.timeK1T1_sec, self.timeK1T2_sec, 3)
            self.timeK2_avg = get_avg(self.timeK2T1_sec, self.timeK2T2_sec, 3)
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
    # стандартные вычисления среднего
            self.viscosityAVG = get_avg(self.viscosity1, self.viscosity2, 5)
        if (self.plustimeminK1T1 and self.plustimesekK1T1) and not (self.plustimeminK1T2
                                                                    and self.plustimesekK1T2 and self.plustimeminK2T2
                                                                    and self.plustimesekK2T2 and self.plustimeminK2T2
                                                                    and self.plustimesekK2T2):
            self.timeK1T1_sec = get_sec(self.plustimeminK1T1, self.plustimesekK1T1)
            self.timeK1_avg = self.timeK1T1_sec
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = self.viscosity1
            self.resultMeas = 'экспрес оценка вязкости'
            self.cause = 'не в условиях повторяемости'
        if (self.plustimeminK1T1 and self.plustimesekK1T1 and self.plustimeminK2T1 and self.plustimesekK2T1) \
                and not (self.plustimeminK1T2 and self.plustimesekK1T2 and self.plustimeminK2T2 and
                         self.plustimesekK2T2):
            self.timeK1T1_sec = get_sec(self.plustimeminK1T1, self.plustimesekK1T1)
            self.timeK2T1_sec = get_sec(self.plustimeminK2T1, self.plustimesekK2T1)
            self.timeK1_avg = self.timeK1T1_sec
            self.timeK2_avg = self.timeK2T1_sec
            self.viscosity1 = (self.Konstant1 * self.timeK1_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosity2 = (self.Konstant2 * self.timeK2_avg).quantize(Decimal('1.00000'), ROUND_HALF_UP)
            self.viscosityAVG = get_avg(self.viscosity1, self.viscosity2, 5)
        self.accMeasurement = get_acc_measurement(Decimal(self.viscosity1), Decimal(self.viscosity2))
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
        if self.resultMeas == 'удовлетворительно':
            self.abserror = mrerrow((Decimal(self.relerror) * self.viscosityAVG) / Decimal(100))
            self.certifiedValue = numberDigits(self.viscosityAVG, self.abserror)
            self.certifiedValue_text = self.certifiedValue
        if self.oldCertifiedValue and self.certifiedValue:
            self.oldCertifiedValue = self.oldCertifiedValue.replace(',', '.')
            self.deltaOldCertifiedValue = \
                get_acc_measurement(Decimal(self.oldCertifiedValue), self.certifiedValue, 2)
            if self.deltaOldCertifiedValue:
                if self.deltaOldCertifiedValue > Decimal(0.7):
                    self.resultWarning = 'Результат отличается от предыдущего > 0,7 %. Рекомендовано измерить повторно.'
    # срок годности
        if self.name[0:2] == 'ВЖ':
            self.date_exp = date.today() + timedelta(days=30*self.exp)

    # связь с конкретной партией
        if self.name[0:2] == 'ВЖ':
            pk_VG = VG.objects.get(name=self.name[0:7])
            a = VGrange.objects.get_or_create(rangeindex=int(self.name[8:-1]), nameSM=pk_VG)
            b = a[0]
            LotVG.objects.get_or_create(lot=self.lot, nameVG=b)
            self.for_lot_and_name = LotVG.objects.get(lot=self.lot, nameVG=b)

    # вносим АЗ в ЖАЗ
            if self.name[0:2] == 'ВЖ' and self.fixation:
                a = CvKinematicviscosityVG.objects.get_or_create(namelot=self.for_lot_and_name)
                note = a[0]
                note = CvKinematicviscosityVG.objects.get(namelot=note.namelot)
                if self.temperature == 20:
                    note.cvt20 = self.certifiedValue_text
                    note.cvt20date = self.date
                    note.cvt20exp = self.exp
                    note.cvt20dead = self.date + timedelta(days=30*self.exp)
                    note.save()
                if self.temperature == 25:
                    note.cvt25 = self.certifiedValue_text
                    note.cvt25date = self.date
                    note.cvt25exp = self.exp
                    note.cvt25dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == 40:
                    note.cvt40 = self.certifiedValue_text
                    note.cvt40date = self.date
                    note.cvt40exp = self.exp
                    note.cvt40dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == 50:
                    note.cvt50 = self.certifiedValue_text
                    note.cvt50date = self.date
                    note.cvt50exp = self.exp
                    note.cvt50dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == 60:
                    note.cvt60 = self.certifiedValue_text
                    note.cvt60date = self.date
                    note.cvt60exp = self.exp
                    note.cvt60dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == 80:
                    note.cvt80 = self.certifiedValue_text
                    note.cvt80date = self.date
                    note.cvt80exp = self.exp
                    note.cvt80dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == 100:
                    note.cvt100 = self.certifiedValue_text
                    note.cvt100date = self.date
                    note.cvt100exp = self.exp
                    note.cvt100dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == 150:
                    note.cvt150 = self.certifiedValue_text
                    note.cvt150date = self.date
                    note.cvt150exp = self.exp
                    note.cvt150dead = self.date + timedelta(days=30 * self.exp)
                    note.save()
                if self.temperature == -20:
                    note.cvtminus20 = self.certifiedValue_text
                    note.cvtminus20date = self.date
                    note.cvtminus20exp = self.exp
                    note.cvtminus20dead = self.date + timedelta(days=30 * self.exp)
                    note.save()

        super(ViscosityMJL, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;   {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('kinematicviscositystr', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Кинематика: аттестация'
        verbose_name_plural = 'Кинематика: аттестация'


class CommentsKinematicviscosity(models.Model):
    """стандартнрый класс для комментариев, поменять только get_absolute_url"""
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(ViscosityMJL, verbose_name='К странице аттестации', on_delete=models.CASCADE,
                                related_name='comments')
    author = models.ForeignKey(User, verbose_name='Наименование', on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.author.username} , {self.forNote.name},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('kinematicviscositycomm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']
