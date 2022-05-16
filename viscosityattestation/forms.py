from django import forms
from django.contrib.auth.models import User

from .models import ViscosityMJL

class ViscosityMJLCreationForm(forms.ModelForm):
    name = forms.CharField(label='Наименование пробы', max_length=100, required=True)
    lot = forms.CharField(label='Партия', max_length=100, required=True)
    temperature = forms.DecimalField(label='Температура, ℃', max_digits=5, decimal_places=2, required=True)
    termostatition = forms.BooleanField(label='Термостатировано не менее 20 минут', required=True)
    temperatureCheck = forms.BooleanField(label='Температура контролируется внешним поверенным термометром',
                                            required=True)
    termometer = forms.CharField(label='Внутренний номер термометра', max_length=10,  required=True)
    ViscosimeterNumber1 = forms.CharField(label='Заводской номер вискозиметра № 1', max_length=10,  required=True)
    Konstant1 = forms.DecimalField(label='Константа вискозиметра № 1', max_digits=20, decimal_places=10, required=True)
    ViscosimeterNumber2 = forms.CharField(label='Заводской номер вискозиметра № 2', max_length=10, required=True)
    Konstant2 = forms.DecimalField(label='Константа вискозиметра № 2', max_digits=20, decimal_places=10, required=True)
    plustimemin11 = forms.DecimalField(label='Время истечения 11, + мин', max_digits=6, decimal_places=0, required=True)
    plustimesek11 = forms.DecimalField(label='Время истечения 11, + cек', max_digits=5, decimal_places=2, required=True)
    plustimemin12 = forms.DecimalField(label='Время истечения 12, + мин', max_digits=6, decimal_places=0, required=True)
    plustimesek12 = forms.DecimalField(label='Время истечения 12, + cек', max_digits=5, decimal_places=2, required=True)
    plustimemin21 = forms.DecimalField(label='Время истечения 21, + мин', max_digits=6, decimal_places=0, required=True)
    plustimesek21 = forms.DecimalField(label='Время истечения 21, + cек', max_digits=5, decimal_places=2, required=True)
    plustimemin22 = forms.DecimalField(label='Время истечения 22, + мин', max_digits=6, decimal_places=0, required=True)
    plustimesek22 = forms.DecimalField(label='Время истечения 22, + cек', max_digits=5, decimal_places=2, required=True)
    # performer = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        model = ViscosityMJL
        exclude = ["date", "performer"]
        fields = ['name', 'lot', 'temperature', 'termostatition', 'temperatureCheck', 'termometer',
                  'ViscosimeterNumber1', 'Konstant1', 'ViscosimeterNumber2', 'Konstant2',
                  'plustimemin11', 'plustimesek11',
                  'plustimemin12', 'plustimesek12',
                  'plustimemin21', 'plustimesek21',
                  'plustimemin22', 'plustimesek22']