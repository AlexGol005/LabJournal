from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image




class AttestationJ(models.Model):
    date = models.DateField('Дата создания журнала', default=timezone.now)
    name = models.CharField('Наименование журнала', max_length=1000, default='')
    ndocument = models.CharField('Методы испытаний', max_length=100, default='')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ответственный за ведение журнала')
    for_url = models.CharField('Адрес журнала', max_length=100, default='')
    CM = models.TextField('Аттестуемые ГСО', blank=True, null=True)
    extra_info = models.TextField('Доп', blank=True, null=True)
    str_html = models.TextField('HTML код для страницы журнала', blank=True, null=True)
    formuls = models.TextField('Формулы для расчётов', blank=True, null=True)
    img = models.ImageField('Картинка для журнала', default='user_images/default.png', upload_to='user_images')


    def __str__(self):
        return f' {self.name}'

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 1000 or image.width > 1000:
            resize = (1000, 1000)
            image.thumbnail(resize)
            image.save(self.img.path)


    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта """
        return reverse(self.for_url)


    class Meta:
        verbose_name = 'Журнал аттестации'
        verbose_name_plural = 'Журналы аттестации'

class ProductionJ(models.Model):
    date = models.DateField('Дата создания журнала', default=timezone.now)
    name = models.CharField('Наименование журнала', max_length=1000, default='')
    ndocument = models.CharField('Методики приготовления', max_length=100, default='')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ответственный за ведение журнала')
    for_url = models.CharField('Адрес журнала', max_length=100, default='')  # todo URLField
    CM = models.TextField('Изготавливаемые СО', blank=True, null=True)
    extra_info = models.TextField('Доп', blank=True, null=True)
    str_html = models.TextField('HTML код для страницы журнала', blank=True, null=True)
    formuls = models.TextField('Формулы для расчётов', blank=True, null=True)
    img = models.ImageField('Картинка для журнала', default='user_images/default.png', upload_to='user_images')


    def __str__(self):
        return f' {self.name}'

    def save(self, *args, **kwargs):
        super().save()
        image = Image.open(self.img.path)
        if image.height > 1000 or image.width > 1000:
            resize = (1000, 1000)
            image.thumbnail(resize)
            image.save(self.img.path)


    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта """
        return reverse(self.for_url)


    class Meta:
        verbose_name = 'Журнал приготовления'
        verbose_name_plural = 'Журналы приготовления'

class CertifiedValueJ(models.Model):
    date = models.DateField('Дата создания журнала', default=timezone.now)
    name = models.CharField('Наименование журнала', max_length=100, default='')
    for_url = models.CharField('Адрес журнала', max_length=100, default='')
    CM = models.TextField('для СО', blank=True, null=True)
    extra_info = models.TextField('Доп', blank=True, null=True)


    def __str__(self):
        return f' {self.name}'


    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта """
        return reverse(self.for_url)


    class Meta:
        verbose_name = 'Журнал аттестованных значений'
        verbose_name_plural = 'Журналы аттестованных значений'

