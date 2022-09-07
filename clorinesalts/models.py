from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from jouChlorineOilProducts.models import LotCSN, CSN, CSNrange, CVclorinesaltsCSN
from jouPetroleumChlorineImpurityWater.models import LotSSTN, SSTN, SSTNrange, CVforSSTN
from jougascondensate.models import LotGKCS, GKCS, GKCSrange, CVclorinesaltsGKCS

from metods import get_avg, get_acc_measurement, get_abserror
from formuls import mrerrow, numberDigits

MATERIAL = (('ХСН-ПА-1', 'ХСН-ПА-1'),
           ('ХСН-ПА-2', 'ХСН-ПА-2'),
           ('СС-ТН-ПА-1', 'СС-ТН-ПА-1'),
           ('ГК-ПА-2', 'ГК-ПА-2'),
           ('другое', 'другое'))

DOCUMENTS = (('ГОСТ 21534 (Метод А)', 'ГОСТ 21534 (Метод А)'),
             ('другое', 'другое'))

# RELERROR_XSN_1 = 5  # относительная погрешность ХС ХСН-ПА-1 из описания типа, %
# RELERROR_XSN_2 = 2  # относительная погрешность ХС ХСН-ПА-2 из описания типа, %
# RELERROR_SSTN = 1  # относительная погрешность ХС СС-ТН-ПА-1 из описания типа, %
# RELERROR_GK = 3  # относительная погрешность ХС ГК-ПА-2 из описания типа, %

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

TYPE = (('расчёт АЗ', 'расчёт АЗ'),
           ('Мониторинг стабильности', 'Мониторинг стабильности'),
           ('Внутрилабораторный контроль', 'Внутрилабораторный контроль'),
           ('Другое', 'Другое'))

EXP = 24  #срок годности АЗ хлористых солей в месяцах

# оригинальные модели для методов с титрованием

class TitrantHg(models.Model):
    '''приготовление раствора титранта'''
    date = models.DateField('Дата', auto_now_add=True, blank=True)
    lot = models.IntegerField('Партия титранта нитрата ртути', null=True, blank=True, unique=True)
    performer = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='performerHg', blank=True)
    lotreakt1 = models.CharField('Партия и производитель нитрата ртути', max_length=90, null=True, blank=True)
    lotreakt2 = models.CharField('Партия и производитель дистиллированной воды', max_length=90, null=True, blank=True)
    lotreakt3 = models.CharField('Партия и производитель азотной кислоты', max_length=90, null=True, blank=True)
    massHgNO3 = models.DecimalField('Масса нитрата ртути', max_digits=3, decimal_places=2, null=True, blank=True)
    volumeH2O = models.DecimalField('Вместимость колбы, мл', max_digits=4, decimal_places=0, null=True, blank=True)
    volumeHNO3 = models.DecimalField('Объём раствора азотной кислоты, мл', max_digits=3, decimal_places=1, null=True, blank=True)
    availablity = models.CharField('Наличие', max_length=90, default='В наличии', null=True, blank=True)


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
            self.datedead = date.today() + timedelta(days=14)
            self.titr = Decimal(((self.titr1 + self.titr2 + self.titr3) / Decimal('3')).quantize(Decimal('1.0000'), ROUND_HALF_UP))
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
    type = models.CharField('Назначение измерений', max_length=300, choices=TYPE,
                               default= 'Расчёт АЗ', null=True, blank=True)
    for_lot_and_nameLotCSN = models.ForeignKey(LotCSN, verbose_name='Измерение для: СО и партия (ХСН)', on_delete=models.PROTECT,
                                         blank=True, null=True)
    for_lot_and_nameLotSSTN = models.ForeignKey(LotSSTN, verbose_name='Измерение для: СО и партия(СС-ТН)',
                                               on_delete=models.PROTECT,
                                               blank=True, null=True)
    for_lot_and_nameLotGKCS = models.ForeignKey(LotGKCS, verbose_name='Измерение для: СО и партия (ГК)',
                                                on_delete=models.PROTECT,
                                                blank=True, null=True)
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=DOCUMENTS, default='ГОСТ 21534 (Метод А)',
                                 blank=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performercs', blank=True)
    name = models.CharField('Наименование', max_length=100, choices=MATERIAL, default='ХСН-ПА-1',
                                 blank=True)
    namedop = models.CharField('Другое или индекс СО', max_length=100, null=True, blank=True)
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

    aV1E1 = models.DecimalField('А в1э1', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV1E2 = models.DecimalField('А в1э2', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV1E3 = models.DecimalField('А в1э3', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV1E4 = models.DecimalField('А в1э4', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV1E5 = models.DecimalField('А в1э5', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV2E1 = models.DecimalField('А в2э1', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV2E2 = models.DecimalField('А в2э2', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV2E3 = models.DecimalField('А в2э3', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV2E4 = models.DecimalField('А в2э4', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aV2E5 = models.DecimalField('А в2э5', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))

    x1 = models.DecimalField('X1', max_digits=7, decimal_places=3, null=True, blank=True)
    x2 = models.DecimalField('X2', max_digits=7, decimal_places=3, null=True, blank=True)
    x_avg = models.DecimalField('X2', max_digits=7, decimal_places=3, null=True, blank=True)
    factconvergence = models.CharField('Расхождение между результатами Х1-Х2, мг/л', max_length=90, null=True, blank=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)

    ndocreproducibility = models.CharField('Воспроизводимость, мг/л', max_length=90, null=True, blank=True)
    ndoccd = models.CharField('Критическая разность, мг/л', max_length=90, null=True, blank=True)

    order_cv_value_begin = models.CharField('Диапазон по заказу от, мг/л', max_length=90, null=True, blank=True)
    order_cv_value_end = models.CharField('Диапазон по заказу до, мг/л', max_length=90, null=True, blank=True)

    def save(self, *args, **kwargs):
        # связь с конкретной партией и  относительной погрешностью СО
        if self.name == 'СС-ТН-ПА-1':
            pk_SSTN = SSTN.objects.get(name=self.name)
            a = SSTNrange.objects.get_or_create(rangeindex=self.namedop, nameSM=pk_SSTN)
            b = a[0]
            LotSSTN.objects.get_or_create(lot=self.lot, nameSM=b)
            self.for_lot_and_nameLotSSTN = LotSSTN.objects.get(lot=self.lot, nameSM=b)
        if self.name == 'ХСН-ПА-1' or self.name == 'ХСН-ПА-2':
            pk_CSN = CSN.objects.get(name=self.name)
            a = CSNrange.objects.get_or_create(rangeindex=self.namedop, nameSM=pk_CSN)
            b = a[0]
            LotCSN.objects.get_or_create(lot=self.lot, nameSM=b)
            self.for_lot_and_nameLotCSN = LotCSN.objects.get(lot=self.lot, nameSM=b)
            # начало и конец диапазона
            self.order_cv_value_begin = self.for_lot_and_nameLotCSN.nameSM.typebegin
            self.order_cv_value_end = self.for_lot_and_nameLotCSN.nameSM.typeend
        if self.name == 'ГК-ПА-2':
            pk_GKCS = GKCS.objects.get(name=self.name)
            a = GKCSrange.objects.get_or_create(rangeindex=self.namedop, nameSM=pk_GKCS)
            b = a[0]
            LotGKCS.objects.get_or_create(lot=self.lot, nameSM=b)
            self.for_lot_and_nameLotGKCS = LotGKCS.objects.get(lot=self.lot, nameSM=b)
        if self.name == 'Другое':
            self.order_cv_value_begin = Decimal(0)
            self.order_cv_value_end = Decimal(0)
        # расчёты первичные
        clearvolume11 = self.V1E1 - self.backvolume
        clearvolume12 = self.V1E2 - self.backvolume
        clearvolume13 = self.V1E3 - self.backvolume
        clearvolume21 = self.V2E1 - self.backvolume
        clearvolume22 = self.V2E2 - self.backvolume
        clearvolume23 = self.V2E3 - self.backvolume

        if self.titerHg and self.titerHgdead >= date.today():
            cV1E1 = (clearvolume11 * self.titerHg * Decimal('1000') * self.aV1E1) / self.aliquotvolume
            cV1E2 = (clearvolume12 * self.titerHg * Decimal('1000') * self.aV1E2) / self.aliquotvolume
            cV1E3 = (clearvolume13 * self.titerHg * Decimal('1000') * self.aV1E3) / self.aliquotvolume
            cV2E1 = (clearvolume21 * self.titerHg * Decimal('1000') * self.aV2E1) / self.aliquotvolume
            cV2E2 = (clearvolume22 * self.titerHg * Decimal('1000') * self.aV2E2) / self.aliquotvolume
            cV2E3 = (clearvolume23 * self.titerHg * Decimal('1000') * self.aV2E3) / self.aliquotvolume
            self.x1 = cV1E1 + cV1E2 + cV1E3
            self.x2 = cV2E1 + cV2E2 + cV2E3
            if self.V1E4:
                clearvolume14 = self.V1E4 - self.backvolume
                cV1E4 = (clearvolume14 * self.titerHg * Decimal('1000') * self.aV1E1) / self.aliquotvolume
                self.x1 = self.x1 + cV1E4
            if self.V2E4:
                clearvolume24 = self.V2E4 - self.backvolume
                cV2E4 = (clearvolume24 * self.titerHg * Decimal('1000') * self.aV1E5) / self.aliquotvolume
                self.x2 = self.x2 + cV2E4
            if self.V1E5:
                clearvolume15 = self.V1E5 - self.backvolume
                cV1E5 = (clearvolume15 * self.titerHg * Decimal('1000') * self.aV1E5) / self.aliquotvolume
                self.x1 = self.x1 + cV1E5
            if self.V2E5:
                clearvolume25 = self.V2E5 - self.backvolume
                cV2E5 = (clearvolume25 * self.titerHg * Decimal('1000') * self.aV1E1) / self.aliquotvolume
                self.x2 = self.x2 + cV2E5
        if not self.titerHg or self.titerHgdead < date.today():
            self.resultMeas = 'Не установлен или просрочен титр раствора нитрата ртути'


        # определяем сходимость, воспроизводимость и CD, соответствующие диапазону, сначала вычисляем среднее:
        if self.x1:
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
            if Decimal(200) <= self.x_avg <= Decimal(1000):
                self.ndocconvergence = '25'
                self.ndocreproducibility = '50'
                self.ndoccd = '33'
            if Decimal(1000) < self.x_avg:
                self.ndocconvergence = str((self.x_avg * Decimal('0.04')).quantize(Decimal('1.00'), ROUND_HALF_UP))
                self.ndocreproducibility = str((self.x_avg * Decimal('0.04') * 2).quantize(Decimal('1.00'), ROUND_HALF_UP))


            # сравниваем х1-х2 со сходимостью и комментируем результат измерений
            self.factconvergence = (self.x1 - self.x2).copy_abs().quantize(Decimal('1.00'), ROUND_HALF_UP)
            if self.factconvergence > Decimal(self.ndocconvergence):
                self.resultMeas = 'Неудовлетворительно'
                self.cause = '|Х1 - Х2| > r'
            if self.factconvergence <= Decimal(self.ndocconvergence):
                self.resultMeas = 'Удовлетворительно'
        super(Clorinesalts, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.date}; {self.name}({self.namedop})  п.{self.lot}; Х1={self.x1} мг/л, Х2={self.x2} мг/л; Исполнитель: {self.performer} '

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('clorinesaltsstr', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Хлористые соли:  Расчёт АЗ'
        verbose_name_plural = 'Хлористые соли:  Расчёт АЗ'


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

class ClorinesaltsCV(models.Model):
    date = models.DateField('Дата', auto_now=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performercv', blank=True)
    clorinesalts = models.OneToOneField(Clorinesalts, verbose_name='расчёт АЗ к измерению', on_delete=models.PROTECT,
                                        related_name='clorinesalts',  null=True, blank=True)
    clorinesalts2 = models.ForeignKey(Clorinesalts, verbose_name='расчёт АЗ к измерению', on_delete=models.PROTECT,
                                         related_name='clorinesalts2', null=True, blank=True)
    countmeasur = models.BooleanField(verbose_name='Имеются все результаты для расчёта АЗ', default=False,
                                   null=True, blank=True)
    x_avg = models.DecimalField('Xсреднее', max_digits=18, decimal_places=4, null=True, blank=True)
    x_avg_new = models.DecimalField('Xсреднее', max_digits=7, decimal_places=3, null=True, blank=True)

    x_cd_warning = models.CharField('Если входят не все Х', max_length=300, default='', null=True, blank=True)
    x_cd_warning_new = models.CharField('Если по прежнему входят не все Х', max_length=300, default='', null=True, blank=True)

    x_dimension = models.DecimalField('(Xmax + Xmin)/2', max_digits=7, decimal_places=3, null=True, blank=True)

    abserror = models.CharField('Абсолютная  погрешность', null=True, blank=True, max_length=300)
    relerror = models.CharField('Относительная   погрешность', null=True, blank=True, max_length=300)

    typebegin = models.CharField('Описание типа от', null=True, blank=True, max_length=300)
    typeend = models.CharField('Описание типа до', null=True, blank=True, max_length=300)

    pricebegin = models.CharField('По прайсу или заказу от', null=True, blank=True, max_length=300)
    priceend = models.CharField('По прайсу или заказу до', null=True, blank=True, max_length=300)

    certifiedValue = models.CharField('Аттестованное значение', null=True,
                                      blank=True, max_length=300)


    certifiedValue_type_diap = models.BooleanField('АЗ входит в описание типа', blank=True, null=True)
    certifiedValue_price_diap = models.BooleanField('АЗ входит в описание диапазон по прайсу', blank=True, null=True)

    olddvalue = models.CharField('Предыдущее значение', max_length=300, null=True, default='', blank=True)
    deltaolddvalue = models.DecimalField('Оценка разницы с предыдущим значением ',
                                         max_digits=10, decimal_places=2, null=True, blank=True)
    old_delta_warning = models.CharField('Текст о разнице с предыдущим значением', max_length=300, default='', null=True, blank=True)
    price_warning = models.CharField('Текст о вхождении в прайс (диапазон)', max_length=300, default='', null=True, blank=True)
    type_warning = models.CharField('Текст о вхождении в описание типа', max_length=300, default='', null=True, blank=True)
    exp = models.IntegerField('Срок годности, месяцев',  blank=True, null=True)

    fixation = models.BooleanField(verbose_name='Внесен ли результат в Журнал аттестованных значений?', default=False,
                                   null=True, blank=True)
    def save(self, *args, **kwargs):
        self.exp = EXP
        # устанавливаем границы по заказу (прайсу)
        if self.clorinesalts.name[0:3] == 'ХСН':
            self.pricebegin = self.clorinesalts.for_lot_and_nameLotCSN.nameSM.pricebegin
            self.priceend = self.clorinesalts.for_lot_and_nameLotCSN.nameSM.priceend
        if self.clorinesalts.order_cv_value_end:
            self.priceend = self.clorinesalts.order_cv_value_end
        if self.clorinesalts.order_cv_value_begin:
            self.pricebegin = self.clorinesalts.order_cv_value_begin
        if not self.clorinesalts.order_cv_value_end and self.clorinesalts2.order_cv_value_end:
            self.priceend = self.clorinesalts.order_cv_value_end
        if not self.clorinesalts.order_cv_value_begin and self.clorinesalts.order_cv_value_begin:
            self.pricebegin = self.clorinesalts.order_cv_value_begin

        # находим х среднее из всех измерений
        if self.countmeasur:
            if self.clorinesalts and not self.clorinesalts2:
                x1 = self.clorinesalts.x1
                x2 = self.clorinesalts.x2
                self.x_avg = ((x1 + x2) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                self.x_cd_warning = 'Все результаты входят в CD'
                self.x_dimension = self.x_avg
            if self.clorinesalts and self.clorinesalts2:
                x1 = self.clorinesalts.x1
                x2 = self.clorinesalts.x2
                x3 = self.clorinesalts2.x1
                x4 = self.clorinesalts2.x2
                self.x_avg = ((x1 + x2 + x3 + x4) / Decimal(4)).quantize(Decimal('1.000'), ROUND_HALF_UP)
            # проверяем вхождение в CD и указываем причину
                kr1 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg - x1).copy_abs())
                kr2 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg - x2).copy_abs())
                kr3 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg - x3).copy_abs())
                kr4 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg - x4).copy_abs())
                if kr1 >=0 and kr2 >=0 and kr3 >=0 and kr4 >= 0:
                    self.x_cd_warning = 'Все результаты входят в CD'
                    xmax = max(x1, x2, x3, x4)
                    xmin = min(x1, x2, x3, x4)
                    self.x_dimension = ((xmax + xmin) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                if kr1 < 0 and kr2 >=0 and kr3 >=0 and kr4 >= 0:
                    self.x_cd_warning = 'x1 выброс по CD, расчёт по х2, х3, х4'
                    self.x_avg_new = ((x2 + x3 + x4) / Decimal(3)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    kr4 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x2).copy_abs())
                    kr5 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x3).copy_abs())
                    kr6 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x4).copy_abs())
                    if kr4 >= 0 and kr5 >= 0 and kr6 >= 0:
                        self.x_cd_warning_new = 'х2, х3, х4 входит в CD'
                        xmax = max(x2, x3, x4)
                        xmin = min(x2, x3, x4)
                        self.x_dimension = ((xmax + xmin) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    else:
                        self.x_cd_warning_new = 'Измерения не входят в CD, недостаточно измерений для расчёта АЗ'

                if kr1 >=0 and kr2 < 0 and kr3 >= 0 and kr4 >= 0:
                    self.x_cd_warning = 'x2 выброс по CD, расчёт по х1, х3, х4'
                    self.x_avg_new = ((x1 + x3 + x4) / Decimal(3)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    kr4 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x1).copy_abs())
                    kr5 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x3).copy_abs())
                    kr6 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x4).copy_abs())
                    if kr4 >= 0 and kr5 >= 0 and kr6 >= 0:
                        self.x_cd_warning_new = 'х1, х3, х4 входит в CD'
                        xmax = max(x1, x3, x4)
                        xmin = min(x1, x3, x4)
                        self.x_dimension = ((xmax + xmin) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    else:
                        self.x_cd_warning_new = 'Измерения не входят в CD, недостаточно измерений для расчёта АЗ'

                if kr1 >=0 and kr2 >= 0 and kr3 < 0 and kr4 >= 0:
                    self.x_cd_warning = 'x3 выброс по CD, расчёт по х1, х2, х4'
                    self.x_avg_new = ((x1 + x2 + x4) / Decimal(3)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    kr4 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x1).copy_abs())
                    kr5 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x2).copy_abs())
                    kr6 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x4).copy_abs())
                    if kr4 >= 0 and kr5 >= 0 and kr6 >= 0:
                        self.x_cd_warning_new = 'х1, х2, х4 входит в CD'
                        xmax = max(x1, x2, x4)
                        xmin = min(x1, x2, x4)
                        self.x_dimension = ((xmax + xmin) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    else:
                        self.x_cd_warning_new = 'Измерения не входят в CD, недостаточно измерений для расчёта АЗ'

                if kr1 >=0 and kr2 >=0 and kr3 >= 0 and kr4 < 0:
                    self.x_cd_warning = 'x4 выброс по CD, расчёт по х1, х2, х3'
                    self.x_avg_new_new = ((x1 + x2 + x3) / Decimal(3)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    kr4 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x1).copy_abs())
                    kr5 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x2).copy_abs())
                    kr6 = Decimal(self.clorinesalts.ndoccd) - ((self.x_avg_new - x3).copy_abs())
                    if kr4 >= 0 and kr5 >= 0 and kr6 >= 0:
                        self.x_cd_warning_new = 'х1, х2, х3 входит в CD'
                        xmax = max(x1, x2, x3)
                        xmin = min(x1, x2, x3)
                        self.x_dimension = ((xmax + xmin) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    else:
                        self.x_cd_warning_new = 'Измерения не входят в CD, недостаточно измерений для расчёта АЗ'

                if kr1 < 0 and kr2 >=0 and kr3 < 0 and kr4 >= 0:
                    self.x_cd_warning_new = 'x1 и х3 выброс по CD, расчёт по х2 и х4'
                    self.x_avg_new = ((x2 + x4) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    self.x_dimension = self.x_avg_new

                if kr1 >=0 and kr2 < 0 and kr3 < 0 and kr4 >= 0:
                    self.x_cd_warning_new = 'x2 и х3 выброс по CD, расчёт по х1 и х4'
                    self.x_avg_new = ((x1 + x4) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    self.x_dimension = self.x_avg_new

                if kr1 < 0 and kr2 >=0 and kr3 >= 0 and kr4 < 0:
                    self.x_cd_warning_new = 'x1 и х4 выброс по CD, расчёт по х2 и х3'
                    self.x_avg_new = ((x2 + x3) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    self.x_dimension = self.x_avg_new

                if kr1 >=0 and kr2 < 0 and kr3 >= 0 and kr4 < 0:
                    self.x_cd_warning_new = 'x2 и х4 выброс по CD, расчёт по х1 и х3'
                    self.x_avg_new = ((x1 + x3) / Decimal(2)).quantize(Decimal('1.000'), ROUND_HALF_UP)
                    self.x_dimension = self.x_avg_new

                if (kr1 < 0 and kr2 < 0 and kr3 < 0 and kr4 < 0) or\
                    (kr1 < 0 and kr2 < 0) or (kr3 < 0 and kr4 < 0):
                    self.x_cd_warning = 'Измерения не входят в CD, недостаточно измерений для расчёта АЗ'

            if self.x_dimension:
                if self.clorinesalts.name == 'ХСН-ПА-1' or self.clorinesalts.name == 'ХСН-ПА-2':
                    self.abserror = mrerrow(get_abserror(self.x_dimension,
                                                         Decimal(self.clorinesalts.for_lot_and_nameLotCSN.nameSM.nameSM.relerror)))
                    self.relerror = self.clorinesalts.for_lot_and_nameLotCSN.nameSM.nameSM.relerror
                    self.typebegin = self.clorinesalts.for_lot_and_nameLotCSN.nameSM.nameSM.typebegin
                    self.typeend = self.clorinesalts.for_lot_and_nameLotCSN.nameSM.nameSM.typeend
                if self.clorinesalts.name == 'СС-ТН-ПА-1':
                    self.abserror = mrerrow(get_abserror(self.x_dimension,
                                                         Decimal(self.clorinesalts.for_lot_and_nameLotSSTN.nameSM.nameSM.relerrorCS)))
                    self.relerror = self.clorinesalts.for_lot_and_nameLotSSTN.nameSM.nameSM.relerrorCS
                    self.typebegin = self.clorinesalts.for_lot_and_nameLotSSTN.nameSM.nameSM.typebeginCS
                    self.typeend = self.clorinesalts.for_lot_and_nameLotSSTN.nameSM.nameSM.typeendCS
                if self.clorinesalts.name == 'ГК-ПА-2':
                    self.abserror = mrerrow(get_abserror(self.x_dimension,
                                                         Decimal(self.clorinesalts.for_lot_and_nameLotGKCS.nameSM.nameSM.relerror)))
                    self.relerror = self.clorinesalts.for_lot_and_nameLotGKCS.nameSM.nameSM.relerror
                    self.typebegin = self.clorinesalts.for_lot_and_nameLotGKCS.nameSM.nameSM.typebegin
                    self.typeend = self.clorinesalts.for_lot_and_nameLotGKCS.nameSM.nameSM.typeend
                self.certifiedValue = numberDigits(self.x_dimension, self.abserror)


        # проверяем соответствие АЗ диапазону по прайсу и по описанию типа иразницу со старым
                if self.typebegin and self.typeend:
                    if Decimal(self.typebegin) <= self.certifiedValue <= Decimal(self.typeend):
                        self.type_warning = 'АЗ входит в диапазон по описанию типа'
                    if Decimal(self.typebegin) >= self.certifiedValue or self.certifiedValue >= Decimal(self.typeend):
                        self.type_warning = 'АЗ не входит в диапазон по описанию типа!'
                if not self.typebegin or not self.typeend:
                    self.type_warning = 'Не указан диапазон по описанию типа!'
                if self.pricebegin and self.priceend:
                    if Decimal(self.pricebegin) <= self.certifiedValue <= Decimal(self.priceend):
                        self.price_warning = 'АЗ входит в диапазон по заказу или прайсу'
                    if Decimal(self.pricebegin) >= self.certifiedValue or self.certifiedValue >= Decimal(self.priceend):
                        self.price_warning = 'АЗ не входит в диапазон по заказу или прайсу!'
                if not self.pricebegin or not self.priceend:
                    self.price_warning = 'Не указан ни диапазон по заказу, ни по прайсу'
                # вносим АЗ в ЖАЗ
                if self.clorinesalts.name[0:3] == 'ХСН' and self.fixation:
                    a = CVclorinesaltsCSN.objects.get_or_create(namelot=self.clorinesalts.for_lot_and_nameLotCSN)
                    note = a[0]
                    note.cv = self.certifiedValue
                    note.cvdate = self.date
                    note.cvexp = self.exp
                    note.cvdead = self.date + timedelta(days=30 * EXP)
                    note.save()
                if self.clorinesalts.name[0:2] == 'CC' and self.fixation:
                    a = CVforSSTN.objects.get_or_create(namelot=self.clorinesalts.for_lot_and_nameLotSSTN)
                    note = a[0]
                    note.cvCS = self.certifiedValue
                    note.cvdateCS = self.date
                    note.cvexpCS = self.exp
                    note.cvdeadCS = self.date + timedelta(days=30 * EXP)
                    note.save()
                if self.clorinesalts.name[0:2] == 'ГК' and self.fixation:
                    a = CVclorinesaltsGKCS.objects.get_or_create(namelot=self.clorinesalts.for_lot_and_nameLotGKCS)
                    note = a[0]
                    note.cv = self.certifiedValue
                    note.cvdate = self.date
                    note.cvexp = self.exp
                    note.cvdead = self.date + timedelta(days=30 * EXP)
                    note.save()


        super(ClorinesaltsCV, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.clorinesalts.name}({self.clorinesalts.namedop}) п.{self.clorinesalts.lot};   {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('clorinesaltsstrcv', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Хлористые соли:  расчёт АЗ'
        verbose_name_plural = 'Хлористые соли:  расчёт АЗ'


class CommentsClorinesaltsCV(models.Model):
    """Стандартная модель для комментариев (меняем только название, адрес get_absolute_url, forNote)"""
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    name = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(ClorinesaltsCV, verbose_name='К странице аттестации', on_delete=models.PROTECT,
                                related_name='comments')
    author = models.ForeignKey(User, verbose_name='Наименование', on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.author.username} , {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('clorinesaltscommcv', kwargs={'pk': self.forNote.pk})

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pk']