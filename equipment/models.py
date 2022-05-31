from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from decimal import *




CHOICES = (
        ('Э', 'В эксплуатации'),
        ('С', 'Списан'),
        ('Р', 'Резерв'),
        ('Д', 'Другое'),
    )

KATEGORY = (
        ('СИ', 'Средство измерения'),
        ('ИО', 'Испытательное оборудование'),
        ('ВО', 'Вспомогательное оборудование'),
        ('КСИ', 'Калибруемое средство измерения'),
        ('И', 'Индикатор'),
    )

class Manufacturer(models.Model):
    companyName = models.CharField('Производитель', max_length=100)
    companyAdress = models.CharField('Адрес', max_length=200, default='', blank=True)
    country = models.CharField('Страна', max_length=200, default='Россия', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

class Rooms(models.Model):
    roomnumber = models.CharField('Номер комнаты', max_length=10, default='')
    person = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.roomnumber

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

class ModificationsAndTypes(models.Model):
    modificname = models.CharField('Модификация прибора', max_length=100, default='', blank=True, null=True)
    typename = models.CharField('Тип прибора', max_length=100, default='', blank=True, null=True)
    def __str__(self):
        return f'Модификация {self.modificname} Тип {self.typename} '


    class Meta:
        verbose_name = 'Модификация и тип'
        verbose_name_plural = 'Модификации и типы'





class Equipment(models.Model):
    exnumber = models.CharField('Внутренний номер', max_length=100, default='', blank=True, null=True, unique=True)
    lot = models.CharField('Заводской номер', max_length=100, default='')
    yearmanuf = models.IntegerField('Год выпуска', default='', blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name='Производитель')
    status = models.CharField(max_length=300, choices=CHOICES, default='В эксплуатации', null=True, verbose_name='Статус')
    docs = models.TextField('Перечень документов и принадлежностей', max_length=1000, default='', blank=True, null=True)
    yearintoservice = models.IntegerField('Год ввода в эксплуатацию', default='0', blank=True, null=True)
    new = models.CharField('Новый или б/у', max_length=100, default='новый')
    invnumber = models.CharField('Инвентарный номер', max_length=100, default='', blank=True, null=True)
    kategory = models.CharField(max_length=300, choices=KATEGORY, default='Средство измерения', null=True, verbose_name='Категория')


    def __str__(self):
        return f'Вн. № {self.exnumber} Зав. № {self.lot}'


    class Meta:
        verbose_name = 'Прибор'
        verbose_name_plural = 'Приборы'

class Personchange(models.Model):
    person = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Ответственный за оборудование')
    date = models.DateField('Дата изменения ответственного', auto_now_add=True, db_index=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'Перемещено {self.date}'

    class Meta:
        verbose_name = 'Дата изменения ответственного'
        verbose_name_plural = 'Даты изменения ответственных'

class Roomschange(models.Model):
    roomnumber = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    date = models.DateField('Дата перемещения', auto_now_add=True, db_index=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Оборудование')


    def __str__(self):
        return f'Перемещено {self.date}'

    class Meta:
        verbose_name = 'Дата перемещения прибора'
        verbose_name_plural = 'Даты перемещения приборов'



class MeasurEquipmentCharakters(models.Model):
    name = models.CharField('Название прибора', max_length=100, default='')
    modtype = models.ForeignKey(ModificationsAndTypes, on_delete=models.PROTECT, verbose_name='Тип и модификация', default='', blank=True, null=True)
    reestr = models.CharField('Номер в Госреестре', max_length=1000, default='', blank=True, null=True)
    calinterval = models.IntegerField('МежМетрологический интервал, месяцев', default = 12, blank=True, null=True)
    measurydiapason = models.CharField('Диапазон измерений', max_length=1000, default='', blank=True, null=True)
    accuracity = models.CharField('Класс точности /(разряд/), погрешность и /(или/) неопределённость /(класс, разряд/)',
                              max_length=1000, default='', blank=True, null=True)


    def __str__(self):
        return f'госреестр: {self.reestr},  {self.name}  модификация/тип {self.modtype}'

    class Meta:
        verbose_name = 'Средство измерения описание типа'
        verbose_name_plural = 'Средства измерения описания типов'

class MeasurEquipment(models.Model):
    charakters = models.ForeignKey(MeasurEquipmentCharakters,  on_delete=models.PROTECT, verbose_name='Характеристики СИ', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Оборудование')

    def __str__(self):
        return f' {self.charakters.name}  Зав №{self.equipment.lot}  № реестр {self.charakters.reestr}'

    class Meta:
        verbose_name = 'Средство измерения'
        verbose_name_plural = 'Средства измерения'

















# class DateSelectorWidget(forms.MultiWidget):
#     def __init__(self, attrs=None):
#         days = [(day, day) for day in range(1, 32)]
#         months = [(month, month) for month in range(1, 13)]
#         years = [(year, year) for year in [2018, 2019, 2020]]
#         widgets = [
#             forms.Select(attrs=attrs, choices=days),
#             forms.Select(attrs=attrs, choices=months),
#             forms.Select(attrs=attrs, choices=years),
#         ]
#         super().__init__(widgets, attrs)
#
#     def decompress(self, value):
#         if isinstance(value, date):
#             return [value.day, value.month, value.year]
#         elif isinstance(value, str):
#             year, month, day = value.split('-')
#             return [day, month, year]
#         return [None, None, None]
#
#     def value_from_datadict(self, data, files, name):
#         day, month, year = super().value_from_datadict(data, files, name)
#         # DateField expects a single string that it can parse into a date.
#         return '{}-{}-{}'.format(year, month, day)
