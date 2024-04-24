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
from .j_constants import *
from textconstants import *
from equipment.models import MeasurEquipment, Rooms





# RELERROR_XSN_1 = 5  # относительная погрешность ХС ХСН-ПА-1 из описания типа, %
# RELERROR_XSN_2 = 2  # относительная погрешность ХС ХСН-ПА-2 из описания типа, %
# RELERROR_SSTN = 1  # относительная погрешность ХС СС-ТН-ПА-1 из описания типа, %
# RELERROR_GK = 3  # относительная погрешность ХС ГК-ПА-2 из описания типа, %



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
    # type = models.CharField('Назначение измерений', max_length=300, choices=TYPE,
                                # default= 'Расчёт АЗ', null=True, blank=True)
    # for_lot_and_nameLotCSN = models.ForeignKey(LotCSN, verbose_name='Измерение для: СО и партия (ХСН)', on_delete=models.PROTECT,
                                          # blank=True, null=True)
    # for_lot_and_nameLotSSTN = models.ForeignKey(LotSSTN, verbose_name='Измерение для: СО и партия(СС-ТН)',
                                                # on_delete=models.PROTECT,
                                               #  blank=True, null=True)
    # for_lot_and_nameLotGKCS = models.ForeignKey(LotGKCS, verbose_name='Измерение для: СО и партия (ГК)',
                                                # on_delete=models.PROTECT,
                                                # blank=True, null=True)
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=DOCUMENTS, default='ГОСТ 21534 (Метод А)',
                                 blank=True)
    date = models.DateField('Дата', auto_now_add=True, db_index=True, blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performercs', blank=True)
    name = models.CharField('Наименование', max_length=100, choices=MATERIAL, default='СС-ТН-ПА-1',
                                 blank=True)
    index = models.CharField('Другое или индекс СО', max_length=100, null=True, blank=True)
    lot = models.CharField('Партия', max_length=90, null=True, blank=True)
    range = models.CharField('Диапазон содержания хлористых солей', max_length=3000, choices=CHOICES,
                               default= 'до 50 мг/л', null=True, blank=True)
    # projectconc = models.CharField('Расчётное содержание хлористых солей', max_length=300, null=True, blank=True)
    # que = models.IntegerField('Очередность отбора пробы', blank=True, null=True, default=1)
    # solvent = models.CharField('Растворитель', max_length=90, choices=SOLVENTS, default='орто-ксилол',
                               # blank=True)
    # truevolume = models.BooleanField('Для каждой экстракции: горячей воды на экстракцию 100 мл, промывка  + 35 мл, промывка фильтра + 15 мл')
    # behaviour = models.CharField('Поведение пробы', max_length=100, choices=BEHAVIOUR, default='Расслаивается')

    # exp = models.IntegerField('Срок годности измерения, месяцев', blank=True, null=True, default=24)
    # date_exp = models.DateField('Измерение годно до', blank=True, null=True)
    r = models.CharField('Повторяемость, мг/дм3', max_length=90, null=True, blank=True)

    # aliquotvolume = models.DecimalField('Аликвота пробы, мл', max_digits=3, decimal_places=0, null=True, blank=True)
    # solventvolume = models.DecimalField('Объём растворителя, мл', max_digits=3, decimal_places=0, null=True, blank=True)

    # lotHg = models.CharField('Партия раствора нитрата ртути', max_length=90, null=True, blank=True)
    # titerHg = models.DecimalField('Титр нитрата ртути, мг/см3', max_digits=5, decimal_places=4, null=True, blank=True)
    # Hgdate = models.DateField('Дата изготовления нитрата ртути', null=True, blank=True)
    # titerHgdate = models.DateField('Дата установки титра', null=True, blank=True)
    # titerHgdead = models.DateField('Титр годен до', null=True, blank=True)

    # dfkdate = models.DateField('Дата изготовления дифенилкарбазида', null=True, blank=True)
    # dfkdead = models.DateField('Дифенилкарбазид  годен до', null=True, blank=True)

    # backvolume = models.DecimalField('Объём холостой пробы, мл', max_digits=4, decimal_places=2,
                                                # null=True, blank=True)
    # V1E1 = models.DecimalField('Воронка1, экстракт1', max_digits=4, decimal_places=2, null=True, blank=True)
    # V1E2 = models.DecimalField('Воронка1, экстракт2', max_digits=4, decimal_places=2, null=True, blank=True)
    # V1E3 = models.DecimalField('Воронка1, экстракт3', max_digits=4, decimal_places=2, null=True, blank=True)
    # V1E4 = models.DecimalField('Воронка1, экстракт4', max_digits=4, decimal_places=2, null=True, blank=True)
    # V1E5 = models.DecimalField('Воронка1, экстракт5', max_digits=4, decimal_places=2, null=True, blank=True)
    # V2E1 = models.DecimalField('Воронка2, экстракт1', max_digits=4, decimal_places=2, null=True, blank=True)
    # V2E2 = models.DecimalField('Воронка2, экстракт2', max_digits=4, decimal_places=2, null=True, blank=True)
    # V2E3 = models.DecimalField('Воронка2, экстракт3', max_digits=4, decimal_places=2, null=True, blank=True)
    # V2E4 = models.DecimalField('Воронка2, экстракт4', max_digits=4, decimal_places=2, null=True, blank=True)
    # V2E5 = models.DecimalField('Воронка2, экстракт5', max_digits=4, decimal_places=2, null=True, blank=True)

    # aV1E1 = models.DecimalField('А в1э1', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV1E2 = models.DecimalField('А в1э2', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV1E3 = models.DecimalField('А в1э3', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV1E4 = models.DecimalField('А в1э4', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV1E5 = models.DecimalField('А в1э5', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV2E1 = models.DecimalField('А в2э1', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV2E2 = models.DecimalField('А в2э2', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV2E3 = models.DecimalField('А в2э3', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV2E4 = models.DecimalField('А в2э4', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    # aV2E5 = models.DecimalField('А в2э5', max_digits=2, decimal_places=1, null=True, blank=True, default=Decimal('1'))
    aim = models.CharField('Цель испытаний', max_length=100, choices=aimoptional,
                                  default=aimoptional[0][0],
                                  blank=True, null=True)
    numberexample = models.CharField('Номер(а) экземпляра', max_length=100, default=' ', null=True,  blank=True)
    seria = models.CharField('Номер серии измерений (для однородности)', max_length=100, default='0', null=True)


    x1 = models.DecimalField('X1', max_digits=7, decimal_places=3, null=True, blank=True)
    x2 = models.DecimalField('X2', max_digits=7, decimal_places=3, null=True, blank=True)
    x_avg = models.DecimalField('X2', max_digits=7, decimal_places=3, null=True, blank=True)
    factconvergence = models.CharField('Расхождение между результатами Х1-Х2, мг/л', max_length=90, null=True, blank=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    r1 = models.CharField('Повторяемость, мг/л', max_length=90, null=True, blank=True)
    R1 = models.CharField('Воспроизводимость, мг/л', max_length=90, null=True, blank=True)
    CD1 = models.CharField('Критическая разность, мг/л', max_length=90, null=True, blank=True)
    relerror = models.CharField('Погрешность относительная (описание типа)', max_length=90, null=True, blank=True)
    maincomment = models.CharField('Комментарии', max_length=6000, null=True, blank=True)

    # order_cv_value_begin = models.CharField('Диапазон по заказу от, мг/л', max_length=90, null=True, blank=True)
    # order_cv_value_end = models.CharField('Диапазон по заказу до, мг/л', max_length=90, null=True, blank=True)
    equipment1 = models.CharField('Бюретка', max_length=500, choices=buroptional,
                                  default=buroptional[0][0],
                                  blank=True, null=True)
    room = models.ForeignKey(Rooms, verbose_name='Номер комнаты', null=True,
                                            on_delete=models.PROTECT,  blank=True)



    def save(self, *args, **kwargs):
        for i in range(5):
            if self.name == CHOICES[i][0]:
                          self.relerror = relerroroptional[i]
        self.room = Rooms.objects.get(roomnumber='474')
        # определяем сходимость, воспроизводимость и CD, соответствующие диапазону, сначала вычисляем среднее:
        x_avg = get_avg(self.x1, self.x2, 4)
        abserror = Decimal(x_avg) * Decimal(self.relerror) / Decimal(100)
        abserror = mrerrow(abserror)
        self.x_avg = numberDigits(x_avg, abserror)
        for i in range(4):
               if self.range == CHOICES[i][0]:
                   self.r1 = roptional[i][0]
                   self.R1 = Roptional[i][0]
                   self.CD1 = CDoptional[i][0]



        # сравниваем х1-х2 со сходимостью и комментируем результат измерений
        self.factconvergence = (self.x1 - self.x2).copy_abs().quantize(Decimal('1.00'), ROUND_HALF_UP)
        if self.factconvergence > Decimal(self.r):
            self.resultMeas = 'Неудовлетворительно'
            self.cause = '|Х1 - Х2| > r'
        if self.factconvergence <= Decimal(self.r):
            self.resultMeas = 'Удовлетворительно'
        super(Clorinesalts, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.date}; {self.name}({self.index})  п.{self.lot}; Х1={self.x1} мг/л, Х2={self.x2} мг/л; Исполнитель: {self.performer} '

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('clorinesaltsstr', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Хлористые соли:  Журнал проведения испытаний'
        verbose_name_plural = 'Хлористые соли:  Журнал проведения испытаний'


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
    pass

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
