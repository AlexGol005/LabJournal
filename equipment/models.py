from django.db import models
from PIL import  Image
from django.contrib.auth.models import User
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
    companyName = models.CharField('Производитель', max_length=100, unique=True)
    companyAdress = models.CharField('Адрес', max_length=200, default='', blank=True)
    country = models.CharField('Страна', max_length=200, default='Россия', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

class Verificators(models.Model):
    companyName = models.CharField('Поверитель', max_length=100, unique=True)
    companyAdress = models.CharField('Адрес', max_length=200, default='', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = 'Поверитель'
        verbose_name_plural = 'Поверители'

class VerificatorPerson(models.Model):
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField('ИМЯ', max_length=100, blank=True, null=True, default='Неизвестно')
    departament = models.CharField('отдел', max_length=100, blank=True, null=True)
    dop = models.CharField('Примечание', max_length=200, blank=True, null=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поверитель'
        verbose_name_plural = 'Поверители'

class Rooms(models.Model):
    roomnumber = models.CharField('Номер комнаты', max_length=10, default='', unique=True)
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
    imginstruction1 = models.ImageField('Паспорт', upload_to='user_images', blank=True)
    imginstruction2 = models.ImageField('Внутренняя инструкция', upload_to='user_images', blank=True)
    imginstruction3 = models.ImageField('Право владения', upload_to='user_images', blank=True)
    individuality = models.TextField('Индивидуальные особенности прибора',  blank=True, null=True)


    def __str__(self):
        return f'Вн. № {self.exnumber}    Зав. № {self.lot}'

    def save(self, *args, **kwargs):
        super().save()
        image1 = Image.open(self.imginstruction1.path)
        image2 = Image.open(self.imginstruction2.path)
        image3 = Image.open(self.imginstruction3.path)
        if image1.height > 500 or image1.width > 500:
            resize = (500, 500)
            image1.thumbnail(resize)
        if image2.height > 500 or image2.width > 500:
            resize = (500, 500)
            image2.thumbnail(resize)
        if image3.height > 500 or image3.width > 500:
            resize = (500, 500)
            image3.thumbnail(resize)
            image1.save(self.imginstruction1.path)
            image2.save(self.imginstruction2.path)
            image3.save(self.imginstruction2.path)


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
    reestr = models.CharField('Номер в Госреестре', max_length=1000, default='', blank=True, null=True, unique=True)
    calinterval = models.IntegerField('МежМетрологический интервал, месяцев', default=12, blank=True, null=True)
    measurydiapason = models.CharField('Диапазон измерений', max_length=1000, default='', blank=True, null=True)
    accuracity = models.CharField('Класс точности /(разряд/), погрешность и /(или/) неопределённость /(класс, разряд/)',
                              max_length=1000, default='', blank=True, null=True)


    def __str__(self):
        return f'госреестр: {self.reestr},  {self.name}  {self.modtype}'

    class Meta:
        verbose_name = 'Средство измерения описание типа'
        verbose_name_plural = 'Средства измерения описания типов'

class MeasurEquipment(models.Model):
    charakters = models.ForeignKey(MeasurEquipmentCharakters,  on_delete=models.PROTECT, verbose_name='Характеристики СИ', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Оборудование')

    def __str__(self):
        return f'Вн № {self.equipment.exnumber}  {self.charakters.name}  Зав № {self.equipment.lot}  № реестр {self.charakters.reestr}'

    class Meta:
        verbose_name = 'Средство измерения'
        verbose_name_plural = 'Средства измерения'

class VerificationEquipment(models.Model):
    equipmentSM = models.ForeignKey(MeasurEquipment, verbose_name='СИ',
                                    on_delete=models.PROTECT, related_name='equipmentSM_ver', blank=True, null=True)
    date = models.DateField('Дата поверки')
    datedead = models.DateField('Дата окончания поверки')
    dateorder = models.DateField('Дата заказа следующей поверки')
    arshin = models.TextField('Ссылка на сведения о поверке в Аршин', blank=True, null=True)
    certnumber = models.CharField('Номер сертификата о поверке', max_length=90, blank=True, null=True)
    certnumbershort = models.CharField('Краткий номер сертификата о поверке', max_length=90, blank=True, null=True)
    price = models.DecimalField('Стоимость данной поверки', max_digits=100, decimal_places=2, null=True, blank=True)
    img = models.ImageField('Сертификат', upload_to='user_images', blank=True)
    statusver = models.CharField('Статус поверки', max_length=90, blank=True, null=True)
    statusmoney = models.CharField('Статус оплаты', max_length=90, blank=True, null=True)
    verificatorperson = models.ForeignKey(VerificatorPerson, on_delete=models.PROTECT,
                                          verbose_name='Поверитель Имя', blank=True, null=True)
    type = models.CharField('На месте/выездная', max_length=90, blank=True, null=True)

    def __str__(self):
        return f'Поверка {self.equipmentSM.charakters.name} вн № {self.equipmentSM.equipment.exnumber}'

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 500 or image.width > 500:
            resize = (500, 500)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Поверка прибора'
        verbose_name_plural = 'Поверки приборов'


class NotesEquipment(models.Model):
    note = models.TextField('Запись о неисправности, модификации или ремонте', blank=True, null=True)
    person = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True,
                                  verbose_name='Оборудование')


















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
