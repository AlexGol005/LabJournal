from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import *

from jouChlorineOilProducts.models import LotCSN, CSN, CSNrange, CVclorinesaltsCSN
from jouPetroleumChlorineImpurityWater.models import LotSSTN, SSTN, SSTNrange, CVforSSTN
from jougascondensate.models import LotGKCS, GKCS, GKCSrange, CVclorinesaltsGKCS

from metods import get_avg, get_acc_measurement, get_abserror
from formuls import *
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
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=DOCUMENTS,  null=True,
                                 blank=True)
    date = models.DateField('Дата', blank=True)
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='performercs', blank=True)
    name = models.CharField('Наименование', max_length=100, choices=MATERIAL, default='СС-ТН-ПА-1',
                                 blank=True)
    index = models.CharField('Другое или индекс СО', max_length=100, null=True, blank=True)
    lot = models.CharField('Партия', max_length=90, null=True, blank=True)
    range = models.CharField('Диапазон содержания хлористых солей', max_length=3000, choices=CHOICES,
                               default= 'до 50 мг/л', null=True, blank=True)
    aim = models.CharField('Цель испытаний', max_length=100, choices=aimoptional,
                                  default=aimoptional[0][0],
                                  blank=True, null=True)
    numberexample = models.CharField('Номер(а) экземпляра', max_length=100, default=' ', null=True,  blank=True)
    seria = models.CharField('Номер серии измерений (для однородности)', max_length=100, default='0', null=True)


    x1 = models.DecimalField('X1', max_digits=8, decimal_places=4, null=True, blank=True)
    x2 = models.DecimalField('X2', max_digits=8, decimal_places=4, null=True, blank=True)
    x_avg = models.CharField('Xср',  max_length=100, null=True, blank=True)
    x_cv = models.CharField('Xаз',  max_length=100, null=True, blank=True)
    factconvergence = models.CharField('Расхождение между результатами Х1-Х2, мг/л', max_length=90, null=True, blank=True)
    cv_convergence = models.CharField('Расхождение между результатами Хср-Хаз, мг/л', max_length=90, null=True, blank=True)
    resultMeas = models.CharField('Результат измерений уд/неуд', max_length=100, default='неудовлетворительно',
                                  null=True, blank=True)
    cause = models.CharField('Причина', max_length=100, default='', null=True, blank=True)
    repr1 = models.CharField('Повторяемость, мг/л', max_length=90, null=True, blank=True)
    Rep2 = models.CharField('Воспроизводимость, мг/л', max_length=90, null=True, blank=True)
    CD1 = models.CharField('Критическая разность, мг/л', max_length=90, null=True, blank=True)
    crit_K = models.CharField('Критерий К, мг/л', max_length=90, null=True, blank=True)
    relerror = models.CharField('Погрешность относительная (описание типа)', max_length=90, null=True, blank=True)
    abserror = models.CharField('Погрешность абсолютная', max_length=90, null=True, blank=True)
    maincomment = models.CharField('Комментарии', max_length=6000, null=True, blank=True)
    equipment1 = models.CharField('Бюретка', max_length=500, choices=buroptional,
                                  default=buroptional[0][0],
                                  blank=True, null=True)
    room = models.ForeignKey(Rooms, verbose_name='Номер комнаты', null=True,
                                            on_delete=models.PROTECT,  blank=True)
    repr1comma = models.CharField('Повторяемость запятая, мг/л', max_length=90, null=True, blank=True)
    factconvergencecomma = models.CharField('Расхождение между результатами Х1-Х2, мг/л', max_length=90, null=True, blank=True)
  



    def save(self, *args, **kwargs):
        for i in range(5):
            if self.name == MATERIAL[i][0]:
                self.relerror = relerroroptional[i][0]
        self.room = Rooms.objects.get(roomnumber='474')
        self.ndocument = DOCUMENTS[0][0]
        # определяем сходимость, воспроизводимость и CD, соответствующие диапазону, сначала вычисляем среднее:
        x_avg = get_avg(self.x1, self.x2, 4)
        abserror1 = Decimal(x_avg) * Decimal(self.relerror) / Decimal(100)
        self.abserror = mrerrow(Decimal(abserror1))
        x_avg = Decimal(x_avg).quantize(Decimal('1.0'), ROUND_HALF_UP)
               
        self.x_avg = str(x_avg).replace('.',',') 
        for i in range(4):
               if self.range == CHOICES[i][0]:
                   self.repr1 = roptional[i][0]
                   self.Rep2 = Roptional[i][0]
                   self.CD1 = CDoptional[i][0]
                   sigma_pr = sigma_pr_optional[i][0]
                   uncertainty_measuremetod = get_ex_uncertainty_measuremetod(sigma_pr, self.Rep2)
                   self.crit_K = get_crit_K(self.abserror, uncertainty_measuremetod)
                          




        # сравниваем х1-х2 со сходимостью и комментируем результат измерений
        self.factconvergence = (self.x1 - self.x2).copy_abs().quantize(Decimal('1.00'), ROUND_HALF_UP)
        if self.factconvergence > Decimal(self.repr1):
            self.resultMeas = 'Неудовлетворительно'
            self.cause = '|Х1 - Х2| > r'
        if self.factconvergence <= Decimal(self.repr1):
            self.resultMeas = 'Удовлетворительно'
        if self.x_cv:
            self.cv_convergence = str((Decimal(self.x_avg) - Decimal(self.x_cv)).copy_abs().quantize(Decimal('1.00'), ROUND_HALF_UP))

        self.repr1comma = self.repr1.replace('.',',')
        self.factconvergencecomma = str(self.factconvergence).replace('.',',')
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
