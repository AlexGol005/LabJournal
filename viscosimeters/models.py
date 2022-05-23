from django.db import models
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import now
from django.urls import reverse


class Manufacturer(models.Model):
    companyName = models.CharField('Производитель', max_length=100)

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Status(models.Model):
    status = models.CharField('Статус', max_length=100)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class ViscosimeterType(models.Model):
    pairNumber = models.CharField('Номер пары', max_length=100)
    diameter = models.CharField('Диаметр', max_length=5)
    viscosity1000 = models.CharField('Вязкость за 1000 сек, сСт', max_length=30)
    range = models.CharField('Область измерений, сСт', max_length=30)
    type = models.CharField('Тип', max_length=30, default='ВПЖ-1')
    intervalVerification = models.CharField('Межповерочный интервал', max_length=30, default='4 года')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'{self.diameter}'

    class Meta:
        verbose_name = 'Тип вискозиметра'
        verbose_name_plural = 'Типы вискозиметров'

class Viscosimeters(models.Model):
    serialNumber = models.CharField('Заводской номер', max_length=30)
    viscosimeterType = models.ForeignKey(ViscosimeterType,  verbose_name='Диаметр',
                                 on_delete=models.PROTECT)
    datePov = models.DateField('Дата  поверки', auto_now_add=True)
    datePovDedlain = models.DateField('Дата окончания поверки')
    Manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name='Статус', on_delete=models.CASCADE)


    def __str__(self):
        return f'№ {self.serialNumber}'

    def get_absolute_url(self):
        """ Создание юрл объекта для перенаправления из вьюшки создания объекта на страничку с созданным объектом """
        return reverse('Str', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Вискозиметр'
        verbose_name_plural = 'Вискозиметры'



class Kalibration(models.Model):
    dateKalib = models.DateField('Дата калибровки', auto_now_add=True)
    konstant = models.DecimalField('Установленная константа', max_digits=7, decimal_places=6, default='0')
    dateKalibNext = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id_Viscosimeter = models.ForeignKey(Viscosimeters, verbose_name='Номер вискозиметра', on_delete=models.CASCADE)

    def __str__(self):
        return f'Константа {self.konstant}'

    class Meta:
        verbose_name = 'Калибровка'
        verbose_name_plural = 'Калибровки'

#         как делать поле с выбором значений  - пример
# class Comment(models.Model):
#     """ Комментарии и оценки к статьям """
#     class Ratings(models.IntegerChoices):  # https://docs.djangoproject.com/en/4.0/ref/models/fields/#enumeration-types
#         WITHOUT_RATING = 0, _('Без оценки')
#         TERRIBLE = 1, _('Ужасно')
#         BADLY = 2, _('Плохо')
#         FINE = 3, _('Нормально')
#         GOOD = 4, _('Хорошо')
#         EXCELLENT = 5, _('Отлично')
#
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     # https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/#many-to-one-relationships
#     note = models.ForeignKey(Note, on_delete=models.CASCADE)  # todo related_name='comments'
#     rating = models.IntegerField(default=Ratings.WITHOUT_RATING, choices=Ratings.choices, verbose_name='Оценка')
#
#     def __str__(self):
#         # https://django.fun/docs/django/ru/3.1/ref/models/instances/#django.db.models.Model.get_FOO_display
#         return f'{self.get_rating_display()}: {self.author}'






