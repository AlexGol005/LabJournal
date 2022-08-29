from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from decimal import *

from django.urls import reverse

CHOICES = (
        ('Э', 'Эксплуатация'),
        ('РЕ', 'Ремонт'),
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

NOTETYPE = (
        ('Техническое обслуживание', 'Техническое обслуживание'),
        ('Неисправность', 'Неисправность'),
        ('Ремонт', 'Ремонт'),
        ('Другое', 'Другое'),
    )

CHOICESVERIFIC = (
        ('Поверен', 'Поверен'),
        ('Признан непригодным', 'Признан непригодным'),
        ('Спорный', 'Спорный'),
    )

CHOICESATT = (
        ('Аттестован', 'Аттестован'),
        ('Признан непригодным', 'Признан непригодным'),
        ('Спорный', 'Спорный'),
    )

CHOICESPLACE = (
        ('У поверителя', 'У поверителя'),
        ('В ПА', 'В ПА'),
    )

class Manufacturer(models.Model):
    companyName = models.CharField('Производитель', max_length=100, unique=True)
    companyAdress = models.CharField('Адрес', max_length=200, default='', blank=True)
    country = models.CharField('Страна', max_length=200, default='Россия', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)
    telnumberhelp = models.CharField('Телефон техподдержки для вопросов по оборудованию', max_length=200, default='', blank=True)

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

class Verificators(models.Model):
    companyName = models.CharField('Поверитель', max_length=100, unique=True)
    companyAdress = models.CharField('Адрес', max_length=200, default='-', blank=True)
    telnumber = models.CharField('Телефон', max_length=200, default='-', blank=True)
    email = models.CharField('email', max_length=200, default='-', blank=True)
    note = models.CharField('Примечание', max_length=10000, default='-', blank=True)

    def __str__(self):
        return f'{self.companyName}, {self.companyAdress}, {self.email}, {self.telnumber}'

    class Meta:
        verbose_name = 'Поверитель организация'
        verbose_name_plural = 'Поверители организации'

class VerificatorPerson(models.Model):
    company = models.ForeignKey(Verificators, on_delete=models.PROTECT, verbose_name='Компания',
                                related_name='Verificators_company', blank=True, null=True)
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField('ИМЯ', max_length=100, blank=True, null=True, default=' ')
    departament = models.CharField('отдел', max_length=100, blank=True, null=True)
    dop = models.CharField('Примечание', max_length=200, blank=True, null=True)
    telnumber = models.CharField('Телефон', max_length=200, default='', blank=True)
    email = models.CharField('email', max_length=200, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поверитель сотрудник'
        verbose_name_plural = 'Поверители сотрудники'

class Rooms(models.Model):
    roomnumber = models.CharField('Номер комнаты', max_length=10, default='', unique=True)
    person = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.roomnumber

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Equipment(models.Model):
    exnumber = models.CharField('Внутренний номер', max_length=100, default='', blank=True, null=True, unique=True)
    lot = models.CharField('Заводской номер', max_length=100, default='')
    yearmanuf = models.IntegerField('Год выпуска', default='', blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name='Производитель')
    status = models.CharField(max_length=300, choices=CHOICES, default='В эксплуатации', null=True,
                              verbose_name='Статус')
    yearintoservice = models.IntegerField('Год ввода в эксплуатацию', default='0', blank=True, null=True)
    new = models.CharField('Новый или б/у', max_length=100, default='новый')
    invnumber = models.CharField('Инвентарный номер', max_length=100, default='', blank=True, null=True)
    kategory = models.CharField(max_length=300, choices=KATEGORY, default='Средство измерения', null=True,
                                verbose_name='Категория')
    imginstruction1 = models.ImageField('Паспорт', upload_to='user_images', blank=True, null=True,
                                        default='user_images/default1.png')
    imginstruction2 = models.ImageField('Внутренняя инструкция', upload_to='user_images', blank=True, null=True,
                                        default='user_images/default1.png')
    imginstruction3 = models.ImageField('Право владения', upload_to='user_images', blank=True, null=True,
                                        default='user_images/default1.png')
    individuality = models.TextField('Индивидуальные особенности прибора',  blank=True, null=True)
    video = models.CharField('Ссылка на видео', max_length=1000,  blank=True, null=True)
    notemaster = models.TextField('Примечание ответственного за прибор',  blank=True, null=True)
    price = models.DecimalField('Стоимость', max_digits=100, decimal_places=2, null=True, blank=True)



    def __str__(self):
        return f'Вн. № {self.exnumber}    Зав. № {self.lot} '

    def save(self, *args, **kwargs):
        super().save()
        if self.imginstruction1:
            image1 = Image.open(self.imginstruction1.path)
            if image1.height > 1000 or image1.width > 1000:
                resize = (1000, 1000)
                image1.thumbnail(resize)
                image1.save(self.imginstruction1.path)
        if self.imginstruction2:
            image2 = Image.open(self.imginstruction2.path)
            if image2.height > 1000 or image2.width > 1000:
                resize = (1000, 1000)
                image2.thumbnail(resize)
                image2.save(self.imginstruction2.path)
        if self.imginstruction3:
            image3 = Image.open(self.imginstruction3.path)
            if image3.height > 1000 or image3.width > 1000:
                resize = (1000, 1000)
                image3.thumbnail(resize)
                image3.save(self.imginstruction3.path)


    # def get_absolute_url(self):
    #     """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
    #     return reverse('measureequipmentpk', kwargs={'str': self.exnumber})

    class Meta:
        verbose_name = 'Прибор'
        verbose_name_plural = 'Приборы'

class Personchange(models.Model):
    person = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Ответственный за оборудование')
    date = models.DateField('Дата изменения ответственного', auto_now_add=True, db_index=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f'{self.equipment.exnumber} Изменён ответственный {self.date}'

    class Meta:
        verbose_name = 'Дата изменения ответственного'
        verbose_name_plural = 'Даты изменения ответственных'

class Roomschange(models.Model):
    roomnumber = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    date = models.DateField('Дата перемещения', auto_now_add=True, db_index=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Оборудование')

    def __str__(self):
        return f'{self.equipment.exnumber} Перемещено {self.date} '

    class Meta:
        verbose_name = 'Дата перемещения прибора'
        verbose_name_plural = 'Даты перемещения приборов'


class DocsCons(models.Model):
    date = models.CharField('Дата появления',  max_length=1000, default='', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Оборудование')
    docs = models.TextField('Документ или принадлежность (1 или несколько)', max_length=1000, default='', blank=True, null=True)
    source = models.CharField('Откуда появился', max_length=1000, default='От поставщика', blank=True, null=True)
    note = models.CharField('Примечание', max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.equipment.exnumber} '

    class Meta:
        verbose_name = 'Комплект к прибору'
        verbose_name_plural = 'Комплекты к приборам'


class MeasurEquipmentCharakters(models.Model):
    name = models.CharField('Название прибора', max_length=100, default='')
    reestr = models.CharField('Номер в Госреестре', max_length=1000, default='', blank=True, null=True)
    calinterval = models.IntegerField('МежМетрологический интервал, месяцев', default=12, blank=True, null=True)
    modificname = models.CharField('Модификация прибора', max_length=100, default='', blank=True, null=True)
    typename = models.CharField('Тип прибора', max_length=100, default='', blank=True, null=True)
    measurydiapason = models.CharField('Диапазон измерений', max_length=1000, default='', blank=True, null=True)
    accuracity = models.CharField('Класс точности /(разряд/), погрешность и /(или/) неопределённость /(класс, разряд/)',
                              max_length=1000, default='', blank=True, null=True)
    aim = models.CharField('Назначение', max_length=90, blank=True, null=True)


    def __str__(self):
        return f'госреестр: {self.reestr},  {self.name}  {self.modificname}'

    class Meta:
        verbose_name = 'Средство измерения описание типа'
        verbose_name_plural = 'Средства измерения описания типов'
        unique_together = ('reestr', 'modificname', 'typename', 'name')

class TestingEquipmentCharakters(models.Model):
    name = models.CharField('Название прибора', max_length=100, default='')
    calinterval = models.IntegerField('МежМетрологический интервал, месяцев', default=12, blank=True, null=True)
    modificname = models.CharField('Модификация прибора', max_length=100, default='', blank=True, null=True)
    typename = models.CharField('Тип прибора', max_length=100, default='', blank=True, null=True)
    measurydiapason = models.CharField('Основные технические характеристики', max_length=1000,  blank=True, null=True)
    aim = models.CharField('Наименование видов испытаний и/или определяемых характеристик (параметров) продукции',
                           max_length=500, blank=True, null=True)
    aim2 = models.CharField('Наименование испытуемых групп объектов',
                            max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.name}  {self.modificname}'

    class Meta:
        verbose_name = 'Испытательное оборудование, характеристики'
        verbose_name_plural = 'СИспытательное оборудование, характеристики'
        unique_together = ('name', 'modificname', 'typename')

class MeasurEquipment(models.Model):
    charakters = models.ForeignKey(MeasurEquipmentCharakters,  on_delete=models.PROTECT,
                                   verbose_name='Характеристики СИ', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True,
                                  verbose_name='Оборудование')
    ecard = models.CharField('Назначение', max_length=90, blank=True, null=True)
    aim = models.CharField('Назначение', max_length=90, blank=True, null=True)

    def __str__(self):
        return f'Вн № {self.equipment.exnumber}  {self.charakters.name}  Зав № {self.equipment.lot}  № реестр {self.charakters.reestr}'

    class Meta:
        verbose_name = 'Средство измерения'
        verbose_name_plural = 'Средства измерения'
        unique_together = ('charakters', 'equipment')
        ordering = ['charakters__name']

class TestingEquipment(models.Model):
    charakters = models.ForeignKey(TestingEquipmentCharakters,  on_delete=models.PROTECT,
                                   verbose_name='Характеристики ИО', blank=True, null=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, blank=True, null=True,
                                  verbose_name='Оборудование')


    def __str__(self):
        return f'Вн № {self.equipment.exnumber}  {self.charakters.name}  Зав № {self.equipment.lot} '

    class Meta:
        verbose_name = 'Испытательное оборудование'
        verbose_name_plural = 'Испытательное оборудование'

class Verificationequipment(models.Model):
    equipmentSM = models.ForeignKey(MeasurEquipment, verbose_name='СИ',
                                    on_delete=models.PROTECT, related_name='equipmentSM_ver', blank=True, null=True)
    date = models.DateField('Дата поверки')
    datedead = models.DateField('Дата окончания поверки')
    dateorder = models.DateField('Дата заказа следующей поверки', blank=True, null=True)
    arshin = models.TextField('Ссылка на сведения о поверке в Аршин', blank=True, null=True)
    certnumber = models.CharField('Номер свидетельства о поверке', max_length=90, blank=True, null=True)
    certnumbershort = models.CharField('Краткий номер свидетельства о поверке', max_length=90, blank=True, null=True)
    price = models.DecimalField('Стоимость данной поверки', max_digits=100, decimal_places=2, null=True, blank=True)
    img = models.ImageField('Сертификат', upload_to='user_images', blank=True, null=True)
    statusver = models.CharField(max_length=300, choices=CHOICESVERIFIC, default='Поверен', null=True,
                              verbose_name='Статус')
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT,
                                          verbose_name='Поверитель', blank=True, null=True)

    verificatorperson = models.ForeignKey(VerificatorPerson, on_delete=models.PROTECT,
                                    verbose_name='Поверитель имя', blank=True, null=True)

    place = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                              verbose_name='Место поверки')
    note = models.CharField('Примечание', max_length=900, blank=True, null=True)

    def __str__(self):
        return f'Поверка {self.equipmentSM.charakters.name} вн № {self.equipmentSM.equipment.exnumber}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('measureequipmentver', kwargs={'str': self.equipmentSM.equipment.exnumber})

    def save(self, *args, **kwargs):
        super().save()
        if self.img:
            image = Image.open(self.img.path)
            if image.height > 500 or image.width > 500:
                resize = (500, 500)
                image.thumbnail(resize)
                image.save(self.img.path)

    class Meta:
        verbose_name = 'Поверка прибора'
        verbose_name_plural = 'Поверки приборов'


class Attestationequipment(models.Model):
    equipmentSM = models.ForeignKey(TestingEquipment, verbose_name='ИО',
                                    on_delete=models.PROTECT, related_name='equipmentSM_att', blank=True, null=True)
    date = models.DateField('Дата аттестации')
    datedead = models.DateField('Дата окончания аттестации')
    dateorder = models.DateField('Дата заказа следующей аттестации')
    certnumber = models.CharField('Номер аттестата', max_length=90, blank=True, null=True)
    certnumbershort = models.CharField('Краткий номер свидетельства о аттестата', max_length=90, blank=True, null=True)
    price = models.DecimalField('Стоимость данной аттестации', max_digits=100, decimal_places=2, null=True, blank=True)
    img = models.ImageField('Аттестат', upload_to='user_images', blank=True, null=True)
    statusver = models.CharField(max_length=300, choices=CHOICESATT, default='Аттестован', null=True,
                              verbose_name='Статус')
    verificator = models.ForeignKey(Verificators, on_delete=models.PROTECT,
                                          verbose_name='Поверитель', blank=True, null=True)

    verificatorperson = models.ForeignKey(VerificatorPerson, on_delete=models.PROTECT,
                                    verbose_name='Поверитель имя', blank=True, null=True)

    place = models.CharField(max_length=300, choices=CHOICESPLACE, default='У поверителя', null=True,
                              verbose_name='Место аттестации')
    note = models.CharField('Примечание', max_length=900, blank=True, null=True)

    def __str__(self):
        return f'Поверка {self.equipmentSM.charakters.name} вн № {self.equipmentSM.equipment.exnumber}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('testingequipmentatt', kwargs={'str': self.equipmentSM.equipment.exnumber})

    def save(self, *args, **kwargs):
        super().save()
        if self.img:
            image = Image.open(self.img.path)
            if image.height > 500 or image.width > 500:
                resize = (500, 500)
                image.thumbnail(resize)
                image.save(self.img.path)

    class Meta:
        verbose_name = 'Аттестация прибора'
        verbose_name_plural = 'Аттестации приборов'


class CommentsEquipment(models.Model):
    """стандартнрый класс для комментариев, поменять только get_absolute_url"""
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    note = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Equipment, verbose_name='К прибору', on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=90, blank=True, null=True)
    type = models.CharField('Тип записи', max_length=90, blank=True, null=True, choices=NOTETYPE)
    img = models.ImageField('Фото', upload_to='user_images', blank=True, null=True, default='user_images/default.png')


    def __str__(self):
        return f' {self.author} , {self.forNote.exnumber},  {self.date}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('measureequipmentcomm', kwargs={'str': self.forNote.exnumber})

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 1000 or image.width > 1000:
            resize = (1000, 1000)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Запись о приборе'
        verbose_name_plural = 'Записи о приборах'
        ordering = ['-pk']


class CommentsVerificationequipment(models.Model):
    """комментарии к поверке """
    date = models.DateField('Дата', auto_now_add=True, db_index=True)
    note = models.TextField('Содержание', max_length=1000, default='')
    forNote = models.ForeignKey(Equipment, verbose_name='К прибору', on_delete=models.CASCADE)
    author = models.CharField('Автор', max_length=90, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('measureequipmentver', kwargs={'str': self.forNote.exnumber})

    class Meta:
        verbose_name = 'Комментарий к поверке'
        verbose_name_plural = 'Комментарии к поверкам'

class MeteorologicalParameters(models.Model):
    """метеорологические параметры в помещении """
    date = models.DateField('Дата')
    roomnumber = models.ForeignKey(Rooms, on_delete=models.PROTECT)
    pressure = models.CharField('Давление, кПа', max_length=90, blank=True, null=True)
    temperature = models.CharField('Температура, °С', max_length=90, blank=True, null=True)
    humidity = models.CharField('Влажность, %', max_length=90, blank=True, null=True)

    class Meta:
        verbose_name = 'Условия в помещении'
        verbose_name_plural = 'Условия в помещениях'


class CompanyCard(models.Model):
    """Карточка Петроаналитики """
    name = models.CharField('Название', max_length=90, blank=True, null=True)
    sertificat9001 = models.CharField('Сертификат 9001', max_length=500, blank=True, null=True)
    affirmationproduction = models.CharField('Утверждаю начальник производства', max_length=90, blank=True, null=True)
    affirmationcompanyboss = models.CharField('Утверждаю генеральный директор', max_length=90, blank=True, null=True)
    adress = models.CharField('Юридический адрес', max_length=500, blank=True, null=True)
    prohibitet = models.TextField('Запрет на тираж протокола',  blank=True, null=True)
    imglogoadress = models.ImageField('Картинка логотип с адресом', upload_to='user_images', blank=True, null=True,
                                        default='user_images/default.png')


    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     super().save()
    #     if self.imglogoadress:
    #         image1 = Image.open(self.imglogoadress.path)
    #         if image1.height > 100 or image1.width > 100:
    #             resize = (200, 200)
    #             image1.thumbnail(resize)
    #             image1.save(self.imglogoadress.path)

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточка'





















