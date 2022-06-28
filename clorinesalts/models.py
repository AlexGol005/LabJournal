from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from jouViscosity.models import VG, VGrange, LotVG, CvDensityDinamicVG
from metods import get_avg, get_acc_measurement
from formuls import mrerrow, numberDigits

from viscosimeters.models import Viscosimeters, Kalibration


DENSITYE = (
    ('денсиметром', 'денсиметром'),
    ('пикнометром', 'пикнометром'),
)

DOCUMENTS = (('ГОСТ 21534 (Метод А)', 'ГОСТ 21534 (Метод А)'),)

RELERROR = 0.3  # относительная погрешность СО из описания типа

CHOICES = (('до 50 мг/л', 'до 50 мг/л'),
           ('50 - 100 мг/л', '50 - 100 мг/л'),
           ('100 - 200 мг/л', '100 - 200 мг/л'),
           ('200 - 500 мг/л', '200 - 500 мг/л'),
           ('500 - 1000 мг/л', '500 - 1000 мг/л'))

SOLVENTS = (('орто-ксилол', 'орто-ксилол'))


class Clorinesalts(models.Model):
    for_lot_and_name = models.ForeignKey(LotRM, verbose_name='Измерение для: СО и партия', on_delete=models.PROTECT,
                                         blank=True, null=True)
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=DOCUMENTS, default='ГОСТ 21534 (Метод А)',
                                 blank=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performer', blank=True)
    name = models.CharField('Наименование', max_length=90, null=True, blank=True)
    lot = models.CharField('Партия', max_length=90, null=True, blank=True)
    constit = models.CharField('Диапазон содержания хлористых солей', max_length=300, choices=CHOICES,
                               default= 'до 50 мг/л', null=True, blank=True)
    projectconc = models.CharField('Расчётное содержания хлористых солей', max_length=300, null=True, blank=True)
    solvent = models.CharField('Растворитель', max_length=90, choices=SOLVENTS, default='орто-ксилол',
                               blank=True)

    exp = models.IntegerField('Срок годности измерения, месяцев', blank=True, null=True)
    date_exp = models.DateField('Измерение годно до', blank=True, null=True)
    ndocconvergence = models.CharField('Сходимость, мг/л', max_length=90, null=True, blank=True)

    aliquotvolume = models.DecimalField('Аликвота пробы, мл', max_digits=3, decimal_places=0, null=True, blank=True)
    solventvolume = models.DecimalField('Объём растворителя, мл', max_digits=3, decimal_places=0, null=True, blank=True)
    lotHg = models.CharField('Партия раствора нитрата ртути', max_length=90, null=True, blank=True)
    titerHg = models.DecimalField('Титр нитрата ртути, мг/см3', max_digits=5, decimal_places=4, null=True, blank=True)
    Hgdate = models.DateField('Дата изготовления нитрата ртути', null=True, blank=True)
    titerHgdate = models.DateField('Дата установки титра', null=True, blank=True)
    titerHgdead = models.DateField('Титр годен до', null=True, blank=True)
    dfkdate = models.DateField('Дата изготовления дифенилкарбазида', null=True, blank=True)
    dfkdead = models.DateField('Дифенилкарбазид  годен до', null=True, blank=True)

    backgroundsamplevolume = models.DecimalField('Объём холостой пробы, мл', max_digits=4, decimal_places=2,
                                                 null=True, blank=True)
    V1E1 = models.DecimalField('Воронка1, экстракт1', max_digits=4, decimal_places=2, null=True, blank=True)
    V1E2 = models.DecimalField('Воронка1, экстракт2', max_digits=4, decimal_places=2, null=True, blank=True)
    V1E3 = models.DecimalField('Воронка1, экстракт3', max_digits=4, decimal_places=2, null=True, blank=True)
    V1E4 = models.DecimalField('Воронка1, экстракт4', max_digits=4, decimal_places=2, null=True, blank=True)
    V1E5 = models.DecimalField('Воронка1, экстракт5', max_digits=4, decimal_places=2, null=True, blank=True)
    V2E1 = models.DecimalField('Воронка2, экстракт1', max_digits=4, decimal_places=2, null=True, blank=True)
    V2E2 = models.DecimalField('Воронка2, экстракт2', max_digits=4, decimal_places=2, null=True, blank=True)
    V2E3 = models.DecimalField('Воронка2, экстракт3', max_digits=4, decimal_places=2, null=True, blank=True)
    V2E4 = models.DecimalField('Воронка2, экстракт4', max_digits=4, decimal_places=2, null=True, blank=True)
    V2E5 = models.DecimalField('Воронка2, экстракт5', max_digits=4, decimal_places=2, null=True, blank=True)

    a = models.DecimalField('А', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    x1 = models.DecimalField('X1', max_digits=7, decimal_places=3, null=True, blank=True)
    x2 = models.DecimalField('X2', max_digits=7, decimal_places=3, null=True, blank=True)
    factconvergence = models.CharField('Расхождение между результатами Х1-Х2, мг/л', max_length=90, null=True, blank=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)


    x3 = models.DecimalField('X3', max_digits=7, decimal_places=3, null=True, blank=True)
    x4 = models.DecimalField('X4', max_digits=7, decimal_places=3, null=True, blank=True)
    performer2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performer', blank=True)
    reproducibility = models.CharField('Воспроизводимость, мг/л', max_length=90, null=True, blank=True)
    cd = models.CharField('Критическая разность, мг/л', max_length=90, null=True, blank=True)
    x_avg = models.DecimalField('Xсреднее', max_digits=7, decimal_places=3, null=True, blank=True)
    x_avg_cd = models.BooleanField('Результаты измерений входят в диапазон Xсреднее+-CD ', blank=True)
    x_cd_warning = models.CharField('Если входят не все Х', max_length=300, default='', null=True, blank=True)
    x_dimension = models.DecimalField('(Xmax + Xmin)/2', max_digits=7, decimal_places=3, null=True, blank=True)


    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True,  blank=True,
                                   default=RELERROR)
    abserror = models.CharField('Абсолютная  погрешность', null=True, blank=True, max_length=300)
    certifiedValue = models.CharField('Аттестованное значение', null=True,
                                         blank=True, max_length=300)


    olddvalue = models.CharField('Предыдущее значение', max_length=300, null=True, default='', blank=True)
    deltaolddvalue = models.DecimalField('Оценка разницы с предыдущим значением ',
                                                 max_digits=10, decimal_places=2, null=True, blank=True)
    old_delta_warning = models.CharField(max_length=300, default='', null=True, blank=True)

    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False,
                                   null=True, blank=True)



    def save(self, *args, **kwargs):
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
                    self.exp = 6
                if 1000 > int(self.name[8:-1]) > 10:
                    self.exp = 12
                if int(self.name[8:-1]) >= 1000:
                    self.exp = 24
        if self.olddensity and self.density_avg:
            self.olddensity = self.olddensity.replace(',', '.')
            self.deltaolddensity = get_acc_measurement(Decimal(self.olddensity), self.density_avg)
            if self.deltaolddensity > Decimal(0.7):
                self.resultWarning = 'плотность отличается от предыдущей на > 0,7 %. Рекомендовано измерить повторно'
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
        return reverse('dinamicviscositycomm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']

