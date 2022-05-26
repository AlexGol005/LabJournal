from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User




class AttestationJ(models.Model):
    date = models.DateField('Дата cсоздания журнала', default=timezone.now)
    name = models.CharField('Наименование журнала', max_length=100, default='')
    ndocument = models.CharField('Методы испытаний', max_length=100, default='')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ответственный за ведение журнала')
    for_url = models.CharField('Адрес журнала', max_length=100, default='')  # todo URLField


    def __str__(self):
        return f' {self.name}'


    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта """
        return reverse(self.for_url)


    class Meta:
        verbose_name = 'Журнал аттестации'
        verbose_name_plural = 'Журналы аттестации'

