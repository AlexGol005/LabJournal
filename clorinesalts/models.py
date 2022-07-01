from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from jouChlorineOilProducts.models import LotCSN, CSN, CSNrange
from jouPetroleumChlorineImpurityWater.models import LotSSTN, SSTN, SSTNrange

from metods import get_avg, get_acc_measurement, get_abserror
from formuls import mrerrow, numberDigits

MATERIAL = (('ХСН-ПА-1', 'ХСН-ПА-1'),
           ('ХСН-ПА-2', 'ХСН-ПА-2'),
           ('СС-ТН-ПА-1', 'СС-ТН-ПА-1'),
           ('ГК-ПА-2', 'ГК-ПА-2'),
           ('другое', 'другое'))

DOCUMENTS = (('ГОСТ 21534 (Метод А)', 'ГОСТ 21534 (Метод А)'),)

RELERROR_XSN_1 = 5  # относительная погрешность ХС ХСН-ПА-1 из описания типа, %
RELERROR_XSN_2 = 2  # относительная погрешность ХС ХСН-ПА-2 из описания типа, %
RELERROR_SSTN = 1  # относительная погрешность ХС СС-ТН-ПА-1 из описания типа, %
RELERROR_GK = 3  # относительная погрешность ХС ГК-ПА-2 из описания типа, %

CHOICES = (('до 50 мг/л', 'до 50 мг/л'),
           ('50 - 100 мг/л', '50 - 100 мг/л'),
           ('100 - 200 мг/л', '100 - 200 мг/л'),
           ('200 - 500 мг/л', '200 - 500 мг/л'),
           ('500 - 1000 мг/л', '500 - 1000 мг/л'))

SOLVENTS = (('орто-ксилол', 'орто-ксилол'),)

BEHAVIOUR = (('Расслаивается', 'Расслаивается'),
           ('Плохо расслаивается', 'Плохо расслаивается'),
           ('Добавлен деэмульгатор', 'Добавлен деэмульгатор'),
           ('Другое (см комментарии)', 'Другое (см комментарии)'),)

VOLUMENACL = (('10', '10'),)

TITRKRIT = Decimal('0.008')

M_NaCl = '58.44'


# оригинальные модели для методов с титрованием

class TitrantHg(models.Model):
    '''приготовление раствора титранта'''
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    lot = models.IntegerField('Партия титранта нитрата ртути', null=True, blank=True, unique=True)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='performerHg', blank=True)
    lotreakt1 = models.CharField('Партия и производитель нитрата ртути', max_length=90, null=True, blank=True)
    lotreakt2 = models.CharField('Партия и производитель дистиллированной воды', max_length=90, null=True, blank=True)
    lotreakt3 = models.CharField('Партия и производитель азотной кислоты', max_length=90, null=True, blank=True)
    massHgNO3 = models.DecimalField('Масса нитрата ртути', max_digits=3, decimal_places=2, null=True, blank=True)
    volumeH2O = models.DecimalField('Вместимость колбы, мл', max_digits=4, decimal_places=0, null=True, blank=True)
    volumeHNO3 = models.DecimalField('Объём раствора азотной кислоты, мл', max_digits=3, decimal_places=1, null=True, blank=True)
    availablity = models.BooleanField('наличие', default=True, blank=True)


    def __str__(self):
        return f'Hg(NO3)2 р-р, п. {self.pk}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('titranthg', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Hg(NO3)2 титрант'
        verbose_name_plural = 'Hg(NO3)2 титрант'


class GetTitrHg(models.Model):
    date = models.DateField('Дата установки титра', auto_now_add=True, db_index=True, blank=True)
    datedead = models.DateField('Дата окончания срока годности титра', blank=True,  null=True)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='performerHgTitr', blank=True)
    lot = models.ForeignKey(TitrantHg, verbose_name='Партия титранта нитрата ртути', blank=True, on_delete=models.PROTECT)
    backvolume = models.DecimalField('Объём холостой пробы, мл', max_digits=4, decimal_places=2,
                                     null=True, blank=True)
    volumeNaCl = models.CharField('Объём 0,01М NaCl', max_length=100, default='10', blank=True)
    massaNaCl = models.DecimalField('Масса NaCl', max_length=100, max_digits=5, decimal_places=3, blank=True)
    volumeHGNO1 = models.DecimalField('Объём Hg(NO3)2 - 1', max_digits=4, decimal_places=2, null=True, blank=True)
    volumeHGNO2 = models.DecimalField('Объём Hg(NO3)2 - 2', max_digits=4, decimal_places=2, null=True, blank=True)
    volumeHGNO3 = models.DecimalField('Объём Hg(NO3)2 - 3', max_digits=4, decimal_places=2, null=True, blank=True)
    titr1 = models.DecimalField('титр 1', max_digits=5, decimal_places=4, null=True, blank=True)
    titr2 = models.DecimalField('титр 2', max_digits=5, decimal_places=4, null=True, blank=True)
    titr3 = models.DecimalField('титр 3', max_digits=5, decimal_places=4, null=True, blank=True)
    ndockrit = models.DecimalField('критерий для титра из НД', max_digits=4, decimal_places=3, default=TITRKRIT)
    krit = models.DecimalField('критерий факт', max_digits=5, decimal_places=3, null=True, blank=True)
    titr = models.DecimalField('титр', max_digits=5, decimal_places=4, null=True, blank=True)
    resultMeas = models.CharField('Результат уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)

    def save(self, *args, **kwargs):

        # self.massaNaCl = Decimal(self.volumeNaCl) * Decimal(M_NaCl)
        self.massaNaCl = Decimal('5.844')
        clearvolumeHGNO1 = self.volumeHGNO1 - self.backvolume
        clearvolumeHGNO2 = self.volumeHGNO2 - self.backvolume
        clearvolumeHGNO3 = self.volumeHGNO3 - self.backvolume
        self.titr1 = (self.massaNaCl / clearvolumeHGNO1).quantize(Decimal('1.0000'), ROUND_HALF_UP)
        self.titr2 = (self.massaNaCl / clearvolumeHGNO2).quantize(Decimal('1.0000'), ROUND_HALF_UP)
        self.titr3 = (self.massaNaCl / clearvolumeHGNO3).quantize(Decimal('1.0000'), ROUND_HALF_UP)
        a = max(self.titr1, self.titr2, self.titr3)
        b = min(self.titr1, self.titr2, self.titr3)
        self.krit = (a - b).copy_abs()
        if self.krit > self.ndockrit:
            self.resultMeas = 'Неудовлетворительно:'
            self.cause = f'Tmax - Tmin > {TITRKRIT}'
        if self.krit <= self.ndockrit:
            self.resultMeas = 'Удовлетворительно:'
            self.cause = f'Tmax - Tmin <= {TITRKRIT}'
            self.datedead = date.today() + timedelta(days=30 * 2)
            self.titr = ((self.titr1 + self.titr2 + self.titr3) / Decimal('3')).quantize(Decimal('1.000'), ROUND_HALF_UP)
        super(GetTitrHg, self).save(*args, **kwargs)

    def __str__(self):
        return f'Hg(NO3)2, п {self.lot},  T: {self.titr} мг/л'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('gettitrhg', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Hg(NO3)2 титр'
        verbose_name_plural = 'Hg(NO3)2 титр'


class IndicatorDFK(models.Model):
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='performerDFK', blank=True)
    datedead = models.DateField('Дата окончания срока годности', blank=True)
    lotreakt1 = models.CharField('Партия и производитель ДФК', max_length=90, null=True, blank=True)
    lotreakt2 = models.CharField('Партия и производитель спирта', max_length=90, null=True, blank=True)
    mass = models.DecimalField('Масса ДФК', max_digits=3, decimal_places=2,  null=True, blank=True)
    volume = models.DecimalField('Вместимость колбы, мл', max_digits=3, decimal_places=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.datedead = date.today() + timedelta(days=30 * 2)
        super(IndicatorDFK, self).save(*args, **kwargs)

    def __str__(self):
        return f'Индикатор ДФК, изготовлен: {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('dpk', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Индикатор ДФК'
        verbose_name_plural = 'Индикатор ДФК'

class Clorinesalts(models.Model):
    for_lot_and_nameLotCSN = models.ForeignKey(LotCSN, verbose_name='Измерение для: СО и партия', on_delete=models.PROTECT,
                                         blank=True, null=True)
    for_lot_and_nameLotSSTN = models.ForeignKey(LotSSTN, verbose_name='Измерение для: СО и партия',
                                               on_delete=models.PROTECT,
                                               blank=True, null=True)
    # for_lot_and_nameLotGK = models.ForeignKey(LotGK, verbose_name='Измерение для: СО и партия',
    #                                             on_delete=models.PROTECT,
    #                                             blank=True, null=True)
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=DOCUMENTS, default='ГОСТ 21534 (Метод А)',
                                 blank=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performercs', blank=True)
    name = models.CharField('Наименование', max_length=100, choices=MATERIAL, default='ХСН-ПА-1',
                                 blank=True)
    namedop = models.CharField('Наименование другое', max_length=100, null=True, blank=True)
    lot = models.CharField('Партия', max_length=90, null=True, blank=True)
    constit = models.CharField('Диапазон содержания хлористых солей', max_length=300, choices=CHOICES,
                               default= 'до 50 мг/л', null=True, blank=True)
    projectconc = models.CharField('Расчётное содержание хлористых солей', max_length=300, null=True, blank=True)
    que = models.IntegerField('Очередность отбора пробы', blank=True, null=True, default=1)
    solvent = models.CharField('Растворитель', max_length=90, choices=SOLVENTS, default='орто-ксилол',
                               blank=True)
    truevolume = models.BooleanField('Для каждой экстракции: горячей воды на экстракцию 100 мл, промывка  + 35 мл, промывка фильтра + 15 мл')
    behaviour = models.CharField('Поведение пробы', max_length=100, choices=BEHAVIOUR, default='Расслаивается')

    exp = models.IntegerField('Срок годности измерения, месяцев', blank=True, null=True, default=24)
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

    backvolume = models.DecimalField('Объём холостой пробы, мл', max_digits=4, decimal_places=2,
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

    aV1E1 = models.DecimalField('А в1э1', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV1E2 = models.DecimalField('А в1э2', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV1E3 = models.DecimalField('А в1э3', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV1E4 = models.DecimalField('А в1э4', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV1E5 = models.DecimalField('А в1э5', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV2E1 = models.DecimalField('А в2э1', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV2E2 = models.DecimalField('А в2э2', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV2E3 = models.DecimalField('А в2э3', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV2E4 = models.DecimalField('А в2э4', max_digits=1, decimal_places=0, null=True, blank=True, default=1)
    aV2E5 = models.DecimalField('А в2э5', max_digits=1, decimal_places=0, null=True, blank=True, default=1)

    x1 = models.DecimalField('X1', max_digits=7, decimal_places=3, null=True, blank=True)
    x2 = models.DecimalField('X2', max_digits=7, decimal_places=3, null=True, blank=True)
    date2 = models.DateField('Дата второго измерения', null=True, blank=True,)
    factconvergence = models.CharField('Расхождение между результатами Х1-Х2, мг/л', max_length=90, null=True, blank=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)

    x3 = models.DecimalField('X3', max_digits=7, decimal_places=3, null=True, blank=True)
    x4 = models.DecimalField('X4', max_digits=7, decimal_places=3, null=True, blank=True)
    performer2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performer2cs', blank=True)
    ndocreproducibility = models.CharField('Воспроизводимость, мг/л', max_length=90, null=True, blank=True)
    ndoccd = models.CharField('Критическая разность, мг/л', max_length=90, null=True, blank=True)
    x_avg = models.DecimalField('Xсреднее', max_digits=7, decimal_places=3, null=True, blank=True)
    x_avg_cd = models.BooleanField('Результаты измерений входят в диапазон Xсреднее+-CD ', blank=True)
    x_cd_warning = models.CharField('Если входят не все Х', max_length=300, default='', null=True, blank=True)
    x_dimension = models.DecimalField('(Xmax + Xmin)/2', max_digits=7, decimal_places=3, null=True, blank=True)

    relerror = models.DecimalField('Относительная  погрешность', max_digits=3, decimal_places=1, null=True,  blank=True)
    abserror = models.CharField('Абсолютная  погрешность', null=True, blank=True, max_length=300)
    certifiedValue = models.CharField('Аттестованное значение', null=True,
                                         blank=True, max_length=300)

    certifiedValue_type_diap = models.BooleanField('АЗ входит в описание типа', blank=True)

    olddvalue = models.CharField('Предыдущее значение', max_length=300, null=True, default='', blank=True)
    deltaolddvalue = models.DecimalField('Оценка разницы с предыдущим значением ',
                                                 max_digits=10, decimal_places=2, null=True, blank=True)
    old_delta_warning = models.CharField(max_length=300, default='', null=True, blank=True)

    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False,
                                   null=True, blank=True)

    def save(self, *args, **kwargs):
        # связь с конкретной партией и  относительной погрешностью СО
        if self.name == 'СС-ТН-ПА-1':
            pk_SSTN = SSTN.objects.get(name=self.name[0:10])
            a = SSTNrange.objects.get_or_create(rangeindex=self.name[11:-1], nameSM=pk_SSTN)
            b = a[0]
            LotSSTN.objects.get_or_create(lot=self.lot, nameSM=b)
            self.for_lot_and_nameSSTN = LotSSTN.objects.get(lot=self.lot, nameSM=b)
            self.relerror = RELERROR_SSTN
        if self.name == 'ХСН-ПА-1' or self.name == 'ХСН-ПА-2':
            pk_CSN = CSN.objects.get(name=self.name[0:8])
            a = CSNrange.objects.get_or_create(rangeindex=self.name[9:-1], nameSM=pk_CSN)
            b = a[0]
            LotCSN.objects.get_or_create(lot=self.lot, nameSM=b)
            self.for_lot_and_nameCSN = LotCSN.objects.get(lot=self.lot, nameSM=b)
            if self.name == 'ХСН-ПА-1':
                self.relerror = RELERROR_XSN_1
            if self.name == 'ХСН-ПА-2':
                self.relerror = RELERROR_XSN_2
        if self.name == 'ГК-ПА-2':
            # pk_CSN = CSN.objects.get(name=self.name[0:8])
            # a = SSTNrange.objects.get_or_create(rangeindex=self.name[9:-1], nameSM=pk_CSN)
            # b = a[0]
            # LotCSN.objects.get_or_create(lot=self.lot, nameSM=b)
            # self.for_lot_and_nameCSN = LotCSN.objects.get(lot=self.lot, nameSM=b)
            self.relerror = RELERROR_GK

        # расчёты первичные
        clearvolume11 = self.V1E1 - self.backvolume
        clearvolume12 = self.V1E2 - self.backvolume
        clearvolume13 = self.V1E3 - self.backvolume
        clearvolume21 = self.V2E1 - self.backvolume
        clearvolume22 = self.V2E2 - self.backvolume
        clearvolume23 = self.V2E3 - self.backvolume

        cV1E1 = (clearvolume11 * self.titerHg * Decimal(1000) * self.aV1E1) / self.aliquotvolume
        cV1E2 = (clearvolume12 * self.titerHg * Decimal(1000) * self.aV1E2) / self.aliquotvolume
        cV1E3 = (clearvolume13 * self.titerHg * Decimal(1000) * self.aV1E3) / self.aliquotvolume
        cV2E1 = (clearvolume21 * self.titerHg * Decimal(1000) * self.aV2E1) / self.aliquotvolume
        cV2E2 = (clearvolume22 * self.titerHg * Decimal(1000) * self.aV2E2) / self.aliquotvolume
        cV2E3 = (clearvolume23 * self.titerHg * Decimal(1000) * self.aV2E3) / self.aliquotvolume
        self.x1 = cV1E1 + cV1E2 + cV1E3
        self.x2 = cV2E1 + cV2E2 + cV2E3
        if self.V1E4:
            clearvolume14 = self.V1E4 - self.backvolume
            cV1E4 = (clearvolume14 * self.titerHg * Decimal(1000) * self.aV1E1) / self.aliquotvolume
            self.x1 = self.x1 + cV1E4
        if self.V2E4:
            clearvolume24 = self.V2E4 - self.backvolume
            cV2E4 = (clearvolume24 * self.titerHg * Decimal(1000) * self.aV1E5) / self.aliquotvolume
            self.x2 = self.x2 + cV2E4
        if self.V1E5:
            clearvolume15 = self.V1E5 - self.backvolume
            cV1E5 = (clearvolume15 * self.titerHg * Decimal(1000) * self.aV1E5) / self.aliquotvolume
            self.x1 = self.x1 + cV1E5
        if self.V2E5:
            clearvolume25 = self.V2E5 - self.backvolume
            cV2E5 = (clearvolume25 * self.titerHg * Decimal(1000) * self.aV1E1) / self.aliquotvolume
            self.x2 = self.x2 + cV2E5
        # определяем сходимость, воспроизводимость и CD, соответствующие диапазону, сначала вычисляем среднее:
        self.x_avg = get_avg(self.x1, self.x2, 4)
        if self.x_avg < Decimal(10):
            self.ndocconvergence = '1.5'
            self.ndocreproducibility = '3.0'
            self.ndoccd = '2.0'
        if Decimal(10) <= self.x_avg < Decimal(50):
            self.ndocconvergence = '3.0'
            self.ndocreproducibility = '6.0'
            self.ndoccd = '4.0'
        if Decimal(50) <= self.x_avg < Decimal(200):
            self.ndocconvergence = '6'
            self.ndocreproducibility = '12'
            self.ndoccd = '8'
        if Decimal(200) <= self.x_avg:
            self.ndocconvergence = '25'
            self.ndocreproducibility = '50'
            self.ndoccd = '33'

        # сравниваем х1-х2 со сходимостью и комментируем результат измерений
        if (self.x1 - self.x2).copy_abs() > Decimal(self.ndocconvergence):
            self.resultMeas = 'Неудовлетворительно.'
            self.cause = 'Разница между Х1 и Х2 превышает сходимость.'
        if (self.x1 - self.x2).copy_abs() <= Decimal(self.ndocconvergence):
            self.resultMeas = 'Удовлетворительно'

        # рассчитываем абсолютную погрешность и аз если результат измерений удовлетворительный
        if self.resultMeas == 'Удовлетворительно':
            self.abserror = mrerrow(get_abserror(self.x_avg, Decimal(self.relerror)))
            self.certifiedValue = numberDigits(self.x_avg, self.abserror)

        # проверяем соответствие АЗ диапазону по прайсу и по описанию типа
        typeSM = CSNrange.objects.get(rangeindex=self.name[9:-1])
        if typeSM.typebegin <= self.certifiedValue <= typeSM.typeend:
            self.certifiedValue_type_diap = True





        super(Clorinesalts, self).save(*args, **kwargs)














        # if self.havedensity and self.density_avg and self.densitydead:
        #     self.resultMeas = 'плотность измерена ранее'
        #     if not self.kinematicviscosity:
        #         self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. Динамика не рассчитана. ' \
        #                                       'Измерьте динамику и заполните новую форму'
        #     if self.kinematicviscosity:
        #         self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
        #         self.abserror = mrerrow((Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
        #         self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
        # if not self.havedensity and not self.density_avg and not self.densitydead:
        #     if not (self.density1 and self.density2):
        #         self.SM_mass1 = self.piknometer_plus_SM_mass1 - self.piknometer_mass1
        #         self.SM_mass2 = self.piknometer_plus_SM_mass2 - self.piknometer_mass2
        #         self.density1 = self.SM_mass1 / self.piknometer_volume
        #         self.density2 = self.SM_mass2 / self.piknometer_volume
        #         if self.constit == 'да':
        #             self.kriteriy = Decimal(0.3)
        #         if self.constit == 'нет':
        #             self.kriteriy = Decimal(0.2)
        #         if self.constit == 'другое':
        #             self.kriteriy = Decimal(0.3)
        #         self.accMeasurement = get_acc_measurement(self.density1, self.density2)
        #         if self.accMeasurement < self.kriteriy:
        #             self.resultMeas = 'удовлетворительно'
        #             self.cause = ''
        #             self.density_avg = get_avg(self.density1, self.density2, 4)
        #             if not self.kinematicviscosity:
        #                 self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. Динамика не рассчитана. ' \
        #                                               'Измерьте динамику и заполните новую форму'
        #             if self.kinematicviscosity:
        #                 self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
        #                 self.abserror = mrerrow(
        #                     (Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
        #                 self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
        #         if self.accMeasurement > self.kriteriy:
        #             self.resultMeas = 'неудовлетворительно'
        #             self.cause = 'Δ > r'
        #     if self.density1 and self.density2:
        #         if self.constit == 'да':
        #             self.kriteriy = Decimal(0.3)
        #         if self.constit == 'нет':
        #             self.kriteriy = Decimal(0.2)
        #         if self.constit == 'другое':
        #             self.kriteriy = Decimal(0.3)
        #         self.accMeasurement = get_acc_measurement(self.density1, self.density2)
        #         if self.accMeasurement < self.kriteriy:
        #             self.resultMeas = 'удовлетворительно'
        #             self.cause = ''
        #             self.density_avg = get_avg(self.density1, self.density2, 4)
        #             if not self.kinematicviscosity:
        #                 self.resultWarningkinematic = 'Нет актуального значения кинематической вязкости. Динамика не рассчитана. ' \
        #                                               'Измерьте динамику и заполните новую форму'
        #             if self.kinematicviscosity:
        #                 self.dinamicviscosity_not_rouned = Decimal(self.kinematicviscosity) * self.density_avg
        #                 self.abserror = mrerrow(
        #                     (Decimal(self.relerror) * self.dinamicviscosity_not_rouned) / Decimal(100))
        #                 self.certifiedValue = numberDigits(self.dinamicviscosity_not_rouned, self.abserror)
        #         if self.accMeasurement > self.kriteriy:
        #             self.resultMeas = 'неудовлетворительно'
        #             self.cause = 'Δ > r'
        #     if self.name[0:2] == 'ВЖ':
        #         if int(self.name[8:-1]) <= 10:
        #             self.exp = 6
        #         if 1000 > int(self.name[8:-1]) > 10:
        #             self.exp = 12
        #         if int(self.name[8:-1]) >= 1000:
        #             self.exp = 24
        # if self.olddensity and self.density_avg:
        #     self.olddensity = self.olddensity.replace(',', '.')
        #     self.deltaolddensity = get_acc_measurement(Decimal(self.olddensity), self.density_avg)
        #     if self.deltaolddensity > Decimal(0.7):
        #         self.resultWarning = 'плотность отличается от предыдущей на > 0,7 %. Рекомендовано измерить повторно'
        # if not self.havedensity:
        #     self.date_exp = date.today() + timedelta(days=30 * self.exp)
        # # связь с конкретной партией
        # if self.name[0:2] == 'ВЖ':
        #     pk_VG = VG.objects.get(name=self.name[0:7])
        #     a = VGrange.objects.get_or_create(rangeindex=int(self.name[8:-1]), nameSM=pk_VG)
        #     b = a[0]
        #     LotVG.objects.get_or_create(lot=self.lot, nameVG=b)
        #     self.for_lot_and_name = LotVG.objects.get(lot=self.lot, nameVG=b)
        # super(Dinamicviscosity, self).save(*args, **kwargs)
        # # вносим АЗ в ЖАЗ
        # if self.name[0:2] == 'ВЖ' and self.fixation:
        #     a = CvDensityDinamicVG.objects.get_or_create(namelot=self.for_lot_and_name)
        #     note = a[0]
        #     note = CvDensityDinamicVG.objects.get(namelot=note.namelot)
        #     if self.temperature == 20:
        #         note.cvt20 = self.density_avg
        #         note.cvtdinamic20 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt20date = self.date
        #             note.cvt20exp = self.exp
        #             note.cvt20dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt20dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead20 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 25:
        #         note.cvt25 = self.density_avg
        #         note.cvtdinamic25 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt25date = self.date
        #             note.cvt25exp = self.exp
        #             note.cvt25dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt250dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead25 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 40:
        #         note.cvt40 = self.density_avg
        #         note.cvtdinamic40 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt40date = self.date
        #             note.cvt40exp = self.exp
        #             note.cvt40dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt40dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead40 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 50:
        #         note.cvt50 = self.density_avg
        #         note.cvtdinamic50 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt50date = self.date
        #             note.cvt50exp = self.exp
        #             note.cvt50dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt50dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead50 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 60:
        #         note.cvt60 = self.density_avg
        #         note.cvtdinamic60 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt60date = self.date
        #             note.cvt60exp = self.exp
        #             note.cvt60dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt60dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead60 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 80:
        #         note.cvt80 = self.density_avg
        #         note.cvtdinamic80 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt80date = self.date
        #             note.cvt80exp = self.exp
        #             note.cvt80dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt80dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead80 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 100:
        #         note.cvt100 = self.density_avg
        #         note.cvtdinamic100 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt100date = self.date
        #             note.cvt100exp = self.exp
        #             note.cvt100dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt100dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead100 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == 150:
        #         note.cvt150 = self.density_avg
        #         note.cvtdinamic150 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvt150date = self.date
        #             note.cvt150exp = self.exp
        #             note.cvt150dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvt150dead = self.densitydead
        #         note.kinematicviscosityfordinamicdead150 = self.kinematicviscositydead
        #         note.save()
        #     if self.temperature == -20:
        #         note.cvtminus20 = self.density_avg
        #         note.cvtdinamicminus20 = self.certifiedValue
        #         if not self.havedensity:
        #             note.cvtminus20date = self.date
        #             note.cvtminus20exp = self.exp
        #             note.cvtminus20dead = self.date + timedelta(days=30 * self.exp)
        #         if self.havedensity:
        #             note.cvtminus20dead = self.densitydead
        #         note.kinematicviscosityfordinamicdeadminus20 = self.kinematicviscositydead
        #         note.save()


    def __str__(self):
        return f' {self.name}  п.{self.lot};   {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('clorinesalts', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Хлористые соли:  аттестация'
        verbose_name_plural = 'Хлористые соли:  аттестация'


class CommentsClorinesalts(models.Model):
    """Стандартная модель для комментариев (меняем только название, адрес get_absolute_url, forNote)"""
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Clorinesalts, verbose_name='К странице аттестации', on_delete=models.PROTECT,
                                related_name='comments')
    author = models.ForeignKey(User, verbose_name='Наименование', on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.author.username} , {self.forNote.name},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('clorinesaltscomm', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']



