from django import forms
from django.contrib.auth.models import User

from .models import ViscosityMJL, CHOICES

class ViscosityMJLCreationForm(forms.ModelForm):
    name = forms.CharField(label='Наименование пробы', max_length=100, required=True)
    lot = forms.CharField(label='Партия', max_length=100, required=True)
    temperature = forms.DecimalField(label='Температура, ℃', max_digits=5, decimal_places=2, required=True)
    termostatition = forms.BooleanField(label='Термостатировано не менее 20 минут', required=True)
    temperatureCheck = forms.BooleanField(label='Температура контролируется внешним поверенным термометром',
                                            required=True)
    ViscosimeterNumber1 = forms.CharField(label='Заводской номер вискозиметра № 1', max_length=10,  required=True)
    Konstant1 = forms.DecimalField(label='Константа вискозиметра № 1', max_digits=20, decimal_places=10, required=True)
    ViscosimeterNumber2 = forms.CharField(label='Заводской номер вискозиметра № 2', max_length=10, required=True)
    Konstant2 = forms.DecimalField(label='Константа вискозиметра № 2', max_digits=20, decimal_places=10, required=True)
    plustimeminK1T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 1, минут',
                                         max_digits=3, decimal_places=0, required=True)
    plustimesekK1T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 1, секунд',
                                         max_digits=5, decimal_places=2, required=True)
    plustimeminK1T2 = forms.DecimalField(initial=0, label='Время истечения 2 из вискозиметра 1, минут',
                                         max_digits=3, decimal_places=0, required=False)
    plustimesekK1T2 = forms.DecimalField(initial=0.0,
                                         label='Время истечения 2 из вискозиметра 1, cекунд',
                                         max_digits=5, decimal_places=2, required=False)
    plustimeminK2T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 2, минут',
                                         max_digits=3, decimal_places=0, required=True)
    plustimesekK2T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 2, секунд',
                                         max_digits=5, decimal_places=2, required=True)
    plustimeminK2T2 = forms.DecimalField(initial=0, label='Время истечения 2 из вискозиметра 2, минут',
                                         max_digits=3, decimal_places=0, required=False)
    plustimesekK2T2 = forms.DecimalField(initial=0.0, label='Время истечения 2 из вискозиметра 2, секунд',
                                         max_digits=5, decimal_places=2, required=False)
    constit = forms.ChoiceField(label='Состав пробы', choices=CHOICES)

    class Meta:
        model = ViscosityMJL
        fields = ['name', 'lot', 'temperature', 'termostatition', 'temperatureCheck',
                  'constit',
                  'ViscosimeterNumber1', 'Konstant1',
                  'plustimeminK1T1', 'plustimesekK1T1',
                  'plustimeminK1T2', 'plustimesekK1T2',
                  'ViscosimeterNumber2', 'Konstant2',
                  'plustimeminK2T1', 'plustimesekK2T1',
                  'plustimeminK2T2', 'plustimesekK2T2']