from django import forms
from django.contrib.auth.models import User

from .models import ViscosityMJL, CHOICES

class ViscosityMJLCreationForm(forms.ModelForm):
    name = forms.CharField(label='Наименование пробы', max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Наименование пробы'}
                                                  ))
    lot = forms.CharField(label='Партия', max_length=100, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Партия'}
                                                 ))
    temperature = forms.DecimalField(label='Температура, ℃', max_digits=5, decimal_places=2, required=True,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Температура'}
                                                            ))
    termostatition = forms.BooleanField(label='Термостатировано не менее 20 минут', required=True)
    temperatureCheck = forms.BooleanField(label='Температура контролируется внешним поверенным термометром',
                                            required=True)
    ViscosimeterNumber1 = forms.CharField(label='Заводской номер вискозиметра № 1', max_length=10,  required=True,
                                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': '№ первого вискозиметра'}
                                                                 ))
    Konstant1 = forms.DecimalField(label='Константа вискозиметра № 1', max_digits=20, decimal_places=10, required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Константа первого вискозиметра'}
                                                          ))
    ViscosimeterNumber2 = forms.CharField(label='Заводской номер вискозиметра № 2', max_length=10, required=True,
    widget = forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': '№ второго вискозиметра'}
                             ))
    Konstant2 = forms.DecimalField(label='Константа вискозиметра № 2', max_digits=20, decimal_places=10, required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Константа второго вискозиметра'}
                                                          ))
    plustimeminK1T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 1, минут',
                                         max_digits=3, decimal_places=0, required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К1, τ1, минуты'}
                                                                ))
    plustimesekK1T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 1, секунд',
                                         max_digits=5, decimal_places=2, required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К1, τ1, секунды'}
                                                                ))
    plustimeminK1T2 = forms.DecimalField(initial=0, label='Время истечения 2 из вискозиметра 1, минут',
                                         max_digits=3, decimal_places=0, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К1, τ1, минуты'}
                                                                ))
    plustimesekK1T2 = forms.DecimalField(initial=0.0,
                                         label='Время истечения 2 из вискозиметра 1, cекунд',
                                         max_digits=5, decimal_places=2, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К2, τ1, секунды'}
                                                                ))
    plustimeminK2T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 2, минут',
                                         max_digits=3, decimal_places=0, required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К1, τ1, минуты'}
                                                                ))
    plustimesekK2T1 = forms.DecimalField(label='Время истечения 1 из вискозиметра 2, секунд',
                                         max_digits=5, decimal_places=2, required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К2, τ1, секунды'}
                                                                ))
    plustimeminK2T2 = forms.DecimalField(initial=0, label='Время истечения 2 из вискозиметра 2, минут',
                                         max_digits=3, decimal_places=0, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К2, τ2, минуты'}
                                                                ))
    plustimesekK2T2 = forms.DecimalField(initial=0.0, label='Время истечения 2 из вискозиметра 2, секунд',
                                         max_digits=5, decimal_places=2, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'К2, τ2, секунды'}
                                                                ))
    constit = forms.ChoiceField(label='Состав пробы', widget=forms.RadioSelect,  choices=CHOICES, required=True)

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