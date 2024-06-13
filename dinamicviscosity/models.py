from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from equipment.models import MeasurEquipment, Rooms
from jouViscosity.models import VG, VGrange, LotVG, CvDensityDinamicVG
from metods import get_avg, get_acc_measurement
from formuls import mrerrow, numberDigits

from viscosimeters.models import Viscosimeters, Kalibration
from .j_constants import *
from textconstants import *
from kinematicviscosity.constvisc import *


class Dinamicviscosity(models.Model):
    for_lot_and_name = models.ForeignKey(LotVG, verbose_name='Измерение для: ГСО и партия', on_delete=models.PROTECT,
                                         blank=True, null=True)
    exp = models.IntegerField('Срок годности плотности, месяцев', blank=True, null=True)
    date_exp = models.DateField('плотность годна до', blank=True, null=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performer', blank=True)
    performerdensity = models.ForeignKey(User, verbose_name='Плотность измерил', on_delete=models.CASCADE, null=True, related_name='performerdensity', blank=True)
    name = models.CharField('Наименование', max_length=100, default='0', null=True, blank=True)
    lot = models.CharField('Партия', max_length=100, null=True, blank=True)
    units = models.CharField('Единицы измерения', max_length=100, default='мПа * с',
                                 blank=True)
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
    density_avg = models.DecimalField('средняя плотность, г/мл', max_digits=7, decimal_places=4, null=True, blank=True)
    delta = models.CharField('Не превышает Δ', max_length=100, null=True, blank=True)
    kriteriy = models.DecimalField('Критерий приемлемости измерений', max_digits=2, decimal_places=1, null=True,
                                   blank=True)
    kinematicviscosity = models.CharField('Кинематическая вязкость при температуре измерений сСт', max_length=300, null=True,
                                           blank=True)
    dinamicviscosity_not_rouned = models.DecimalField('Динамическая вязкость неокругленная', max_digits=20,
                                                      decimal_places=6, null=True, blank=True)
    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True,  blank=True,
                                   default=RELERROR)
    certifiedValue = models.CharField('Аттестованное значение динамической вязкости', null=True,
                                         blank=True, max_length=300)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    accMeasurement = models.DecimalField('Оценка приемлемости измерений плотности', max_digits=5, decimal_places=1, null=True,
                                         blank=True)
    abserror = models.CharField('Абсолютная  погрешность', null=True, blank=True, max_length=300)
    olddensity = models.CharField('Предыдущее значение плотности', max_length=300, null=True, default='', blank=True)
    deltaolddensity = models.DecimalField('Оценка разницы с предыдущим значением плотности',
                                                 max_digits=10, decimal_places=2, null=True, blank=True)
    resultWarning = models.CharField(max_length=300, default='', null=True, blank=True)
    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False,
                                   null=True, blank=True)
    equipment = models.CharField('Способ измерения плотности', max_length=300, choices=DENSITYE, default='денсиметром', null=True,  blank=True)
    resultWarningkinematic = models.CharField('Если нет кинематики', max_length=300, null=True,  blank=True)
    kinematicviscositydead = models.DateField('кинематика годна до:', blank=True, null=True)
    havedensity = models.BooleanField(verbose_name='Есть значение плотности, измеренное ранее', default=False, blank=True)
    densitydead = models.DateField('Плотность, измеренная ранее, годна до:', null=True, blank=True)
    #  поля для записи - помещения, оборудования - для подготовки протокола анализа
    room = models.ForeignKey(Rooms, verbose_name='Номер комнаты', null=True,
                             on_delete=models.PROTECT, blank=True)
    equipment1 = models.ForeignKey(MeasurEquipment, verbose_name='Плотномер', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment1dinamic')
    equipment2 = models.ForeignKey(MeasurEquipment, verbose_name='Термометр', null=True,
                                   on_delete=models.PROTECT, blank=True, related_name='equipment2dinamic')
    equipment3 = models.ForeignKey(MeasurEquipment, verbose_name='Весы', null=True,
                                    on_delete=models.PROTECT, blank=True, related_name='equipment3dinamic')
    equipment4 = models.ForeignKey(MeasurEquipment, verbose_name='Пикнометр', null=True,
                                    on_delete=models.PROTECT, blank=True, related_name='equipment4dinamic')
    aim = models.CharField('Цель испытаний', max_length=100, choices=aimoptional,
                                  default=aimoptional[0][0],
                                  blank=True, null=True)
    numberexample = models.CharField('Номер(а) экземпляра', max_length=100, default=' ', null=True)
    index = models.CharField('ggg', max_length=100, default='0', null=True,  blank=True)
    x1 = models.CharField('ggg', max_length=100, default='0', null=True,  blank=True)
    x2 = models.CharField('ggg', max_length=100, default='0', null=True,  blank=True)
    x_avg = models.CharField('ggg', max_length=100, default='0', null=True,  blank=True)
    factconvergence= models.CharField('ggg', max_length=100, default='0', null=True,  blank=True)
    repr1comma= models.CharField('ggg', max_length=100, default='0', null=True,  blank=True)
    crit_K = models.CharField('Критерий К', max_length=90, null=True, blank=True)
    repr1 = models.CharField('Повторяемость, мм2/с', max_length=90, null=True, blank=True)
    Rep2 = models.CharField('Воспроизводимость, мм2/с', max_length=90, null=True, blank=True)


    def save(self, *args, **kwargs):
        # костыль для добавления приборов и комнаты
        self.equipment1 = MeasurEquipment.objects.get(equipment__exnumber=densimeter)
        self.equipment2 = MeasurEquipment.objects.get(equipment__exnumber=termometer)
        self.equipment3 = MeasurEquipment.objects.get(equipment__exnumber=balance)
        self.equipment4 = MeasurEquipment.objects.get(equipment__exnumber=piknometer)
        if self.equipment == 'денсиметром':
            self.room = Rooms.objects.get(roomnumber='249')
        if self.equipment != 'денсиметром':
            self.room = Rooms.objects.get(roomnumber='474')

        
        if self.havedensity and self.density_avg and self.densitydead:
            self.resultMeas = 'плотность измерена ранее'
            if not self.kinematicviscosity:
                self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. Динамика не рассчитана. ' \
                                              'Измерьте динамику и заполните новую форму'
            
            if self.kinematicviscosity:
                self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
                self.abserror = mrerrow((Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
                self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
        if not self.havedensity and not self.density_avg and not self.densitydead:
            if not (self.density1 and self.density2):
                self.SM_mass1 = self.piknometer_plus_SM_mass1 - self.piknometer_mass1
                self.SM_mass2 = self.piknometer_plus_SM_mass2 - self.piknometer_mass2
                self.density1 = self.SM_mass1 / self.piknometer_volume
                self.density2 = self.SM_mass2 / self.piknometer_volume
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
                    self.density_avg = get_avg(self.density1, self.density2, 4)
                    if not self.kinematicviscosity:
                        self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. Динамика не рассчитана. ' \
                                                      'Измерьте динамику и заполните новую форму'
                  
                    if self.kinematicviscosity:
                        self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
                        self.abserror = mrerrow(
                            (Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
                        self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
                if self.accMeasurement > self.kriteriy:
                    self.resultMeas = 'неудовлетворительно'
                    self.cause = 'Δ > r'
            if self.density1 and self.density2:
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
                    self.density_avg = get_avg(self.density1, self.density2, 4)
                    if not self.kinematicviscosity:
                        self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. Динамика не рассчитана. ' \
                                                      'Измерьте динамику и заполните новую форму'
                    if self.kinematicviscosity:
                        self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
                        self.abserror = mrerrow(
                            (Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
                        self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
                if self.accMeasurement > self.kriteriy:
                    self.resultMeas = 'неудовлетворительно'
                    self.cause = 'Δ > r'
            if self.name[0:2] == 'ВЖ':
                if int(self.name[8:-1]) <= 10:
                    self.exp = 12
                if 1000 > int(self.name[8:-1]) > 10:
                    self.exp = 12
                if int(self.name[8:-1]) >= 1000:
                    self.exp = 24
        if self.olddensity and self.density_avg:
            self.olddensity = self.olddensity.replace(',', '.')
            self.deltaolddensity = get_acc_measurement(Decimal(self.olddensity), self.density_avg)
            if self.deltaolddensity > Decimal(0.7):
                self.resultWarning = 'плотность отличается от предыдущей на > 0,7 %. Рекомендовано измерить повторно'
                if self.name[0:2] == 'ВЖ' and self.deltaolddensity <= Decimal(0.48):
                    self.density_avg = self.olddensity
                    self.resultWarning = 'Отличие результата от предыдущего не превышает CD (0,48%). Плотность остается прежней.'
        if not self.havedensity:
            self.date_exp = date.today() + timedelta(days=30 * self.exp)
        # связь с конкретной партией
        if self.name[0:2] == 'ВЖ':
            pk_VG = VG.objects.get(name=self.name[0:7])
            a = VGrange.objects.get_or_create(rangeindex=int(self.name[8:-1]), nameSM=pk_VG)
            b = a[0]
            LotVG.objects.get_or_create(lot=self.lot, nameVG=b)
            self.for_lot_and_name = LotVG.objects.get(lot=self.lot, nameVG=b)
        super(Dinamicviscosity, self).save(*args, **kwargs)
        # вносим АЗ в ЖАЗ
        if self.name[0:2] == 'ВЖ' and self.fixation:
            a = CvDensityDinamicVG.objects.get_or_create(namelot=self.for_lot_and_name)
            note = a[0]
            note = CvDensityDinamicVG.objects.get(namelot=note.namelot)
            if self.temperature == 20:
                note.cvt20 = self.density_avg
                note.cvtdinamic20 = self.certifiedValue
                if not self.havedensity:
                    note.cvt20date = self.date
                    note.cvt20exp = self.exp
                    note.cvt20dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt20dead = self.densitydead
                note.kinematicviscosityfordinamicdead20 = self.kinematicviscositydead
                note.save()
            if self.temperature == 25:
                note.cvt25 = self.density_avg
                note.cvtdinamic25 = self.certifiedValue
                if not self.havedensity:
                    note.cvt25date = self.date
                    note.cvt25exp = self.exp
                    note.cvt25dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt250dead = self.densitydead
                note.kinematicviscosityfordinamicdead25 = self.kinematicviscositydead
                note.save()
            if self.temperature == 40:
                note.cvt40 = self.density_avg
                note.cvtdinamic40 = self.certifiedValue
                if not self.havedensity:
                    note.cvt40date = self.date
                    note.cvt40exp = self.exp
                    note.cvt40dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt40dead = self.densitydead
                note.kinematicviscosityfordinamicdead40 = self.kinematicviscositydead
                note.save()
            if self.temperature == 50:
                note.cvt50 = self.density_avg
                note.cvtdinamic50 = self.certifiedValue
                if not self.havedensity:
                    note.cvt50date = self.date
                    note.cvt50exp = self.exp
                    note.cvt50dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt50dead = self.densitydead
                note.kinematicviscosityfordinamicdead50 = self.kinematicviscositydead
                note.save()
            if self.temperature == 60:
                note.cvt60 = self.density_avg
                note.cvtdinamic60 = self.certifiedValue
                if not self.havedensity:
                    note.cvt60date = self.date
                    note.cvt60exp = self.exp
                    note.cvt60dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt60dead = self.densitydead
                note.kinematicviscosityfordinamicdead60 = self.kinematicviscositydead
                note.save()
            if self.temperature == 80:
                note.cvt80 = self.density_avg
                note.cvtdinamic80 = self.certifiedValue
                if not self.havedensity:
                    note.cvt80date = self.date
                    note.cvt80exp = self.exp
                    note.cvt80dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt80dead = self.densitydead
                note.kinematicviscosityfordinamicdead80 = self.kinematicviscositydead
                note.save()
            if self.temperature == 100:
                note.cvt100 = self.density_avg
                note.cvtdinamic100 = self.certifiedValue
                if not self.havedensity:
                    note.cvt100date = self.date
                    note.cvt100exp = self.exp
                    note.cvt100dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt100dead = self.densitydead
                note.kinematicviscosityfordinamicdead100 = self.kinematicviscositydead
                note.save()
            if self.temperature == 150:
                note.cvt150 = self.density_avg
                note.cvtdinamic150 = self.certifiedValue
                if not self.havedensity:
                    note.cvt150date = self.date
                    note.cvt150exp = self.exp
                    note.cvt150dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvt150dead = self.densitydead
                note.kinematicviscosityfordinamicdead150 = self.kinematicviscositydead
                note.save()
            if self.temperature == -20:
                note.cvtminus20 = self.density_avg
                note.cvtdinamicminus20 = self.certifiedValue
                if not self.havedensity:
                    note.cvtminus20date = self.date
                    note.cvtminus20exp = self.exp
                    note.cvtminus20dead = self.date + timedelta(days=30 * self.exp)
                if self.havedensity:
                    note.cvtminus20dead = self.densitydead
                note.kinematicviscosityfordinamicdeadminus20 = self.kinematicviscositydead
                note.save()


    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('dinamicviscositystr', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Динамика и плотность: Расчёт АЗ'
        verbose_name_plural = 'Динамика и плотность: Расчёт АЗ'


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
        return reverse('dinamicviscositycomm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']
