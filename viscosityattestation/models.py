from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CalcManager(models.Manager): # Наш менеджер, который нам дает возможность менять поведение модели
    def get_query_set(self):
        result = super(CalcManager, self).get_query_set().extra(select={'total': "first+second"})
        #то место где надо задавать алгоритм по которому вычисляется поле total
        ViscosityMJL.plustimemin11 * 60
        return result


class ViscosityMJL(models.Model):
    # total = CalcManager()
    date = models.DateField('Дата', default=timezone.now)
    name = models.CharField('Наименование', max_length=100)
    lot = models.CharField('Партия', max_length=100)
    ndocumentoptional = (('ГОСТ 33', 'ГОСТ 33'),
                         ('МИ-01', 'МИ-01'),
                         ('оценка', 'оценка вязкости'))
    ndocument = models.CharField('Метод испытаний', max_length=100, choices=ndocumentoptional, default='МИ-01')
    temperature = models.DecimalField('Температура, ℃', max_digits=5, decimal_places=2)
    termostatition = models.BooleanField(verbose_name='Термостатировано не менее 20 минут', blank=False)
    temperatureCheck = models.BooleanField(verbose_name='Температура контролируется внешним поверенным термометром', blank=False)
    termometer = models.CharField('Внутренний номер термометра', max_length=10)
    ViscosimeterNumber1 = models.CharField('Заводской номер вискозиметра № 1', max_length=10)
    Konstant1 = models.FloatField('Константа вискозиметра № 1')
    ViscosimeterNumber2 = models.CharField('Заводской номер вискозиметра № 2', max_length=10)
    Konstant2 = models.FloatField('Константа вискозиметра № 2')
    plustimemin11 = models.DecimalField('Время истечения 11, + мин', max_digits=6, decimal_places=0)
    plustimesek11 = models.DecimalField('Время истечения 11, + cек', max_digits=5, decimal_places=2)
    plustimemin21 = models.DecimalField('Время истечения 21, + мин', max_digits=6, decimal_places=0)
    plustimesek21 = models.DecimalField('Время истечения 21, + cек', max_digits=5, decimal_places=2)
    plustimemin12 = models.DecimalField('Время истечения 12, + мин', max_digits=6, decimal_places=0)
    plustimesek12 = models.DecimalField('Время истечения 12, + cек', max_digits=5, decimal_places=2)
    plustimemin22 = models.DecimalField('Время истечения 22, + мин', max_digits=6, decimal_places=0)
    plustimesek22 = models.DecimalField('Время истечения 22, + cек', max_digits=5, decimal_places=2)
    kriteriy = models.CharField('Критерий приемлемости измерений', max_length=4, default='0,2')
    performer = models.ForeignKey(User, verbose_name='Исполнитель', on_delete=models.PROTECT)

    def __str__(self):
        return f' {self.name}  п.{self.lot};  {self.temperature} t ℃;   {self.date}'

    class Meta:
        verbose_name = 'Измерение кинематической вязкости'
        verbose_name_plural = 'Измерения кинематической вязкости'