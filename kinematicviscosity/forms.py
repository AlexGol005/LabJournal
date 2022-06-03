from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


from django.utils.html import format_html
from .models import ViscosityMJL, CHOICES, CommentsKinematicviscosity




class ViscosityMJLCreationForm(forms.ModelForm):
    name = forms.CharField(initial='ВЖ-2-ПА(100)', label='Наименование пробы', max_length=100, required=True,
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
    Konstant1 = forms.DecimalField(label='Константа вискозиметра № 1', max_digits=20, decimal_places=6, required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Константа через точку'}
                                                          ))
    ViscosimeterNumber2 = forms.CharField(label='Заводской номер вискозиметра № 2', max_length=10, required=False,
    widget = forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder': '№ второго вискозиметра'}
                             ))
    Konstant2 = forms.DecimalField(label='Константа вискозиметра № 2', max_digits=20, decimal_places=6, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Константа через точку'}
                                                          ))
    plustimeminK1T1 = forms.DecimalField(label='τ1, минуты',
                                         max_digits=3, decimal_places=0, required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'мм'}
                                                                ))
    plustimesekK1T1 = forms.DecimalField(label='τ1, секунды',
                                         max_digits=5, decimal_places=2, required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'сс.сс'}
                                                                ))
    plustimeminK1T2 = forms.DecimalField(label='τ2, минуты',
                                         max_digits=3, decimal_places=0, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'мм'}
                                                                ))
    plustimesekK1T2 = forms.DecimalField(
                                         label='τ1, секунды',
                                         max_digits=5, decimal_places=2, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'сс.сс'}
                                                                ))
    plustimeminK2T1 = forms.DecimalField(label='τ1, минуты',
                                         max_digits=3, decimal_places=0, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'мм'}
                                                                ))
    plustimesekK2T1 = forms.DecimalField(label='τ1, секунды',
                                         max_digits=5, decimal_places=2, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'сс.сс'}
                                                                ))
    plustimeminK2T2 = forms.DecimalField(label='τ2, минуты',
                                         max_digits=3, decimal_places=0, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'мм'}
                                                                ))
    plustimesekK2T2 = forms.DecimalField(label='τ2, секунды',
                                         max_digits=5, decimal_places=2, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'сс.сс'}
                                                                ))
    constit = forms.ChoiceField(label='Состав пробы', widget=forms.RadioSelect,  choices=CHOICES, required=True)
    oldCertifiedValue = forms.CharField(label='Предыдущее аттестованное значение', required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'АЗ через точку'}
                                                                ))



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-4 mb-0'),
                Column('temperature', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'termostatition',
            'temperatureCheck',

            Row(
                Column('constit', css_class='form-group col-md-6 mb-0'),
                Column('oldCertifiedValue', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ViscosimeterNumber1', css_class='form-group col-md-6 mb-0'),
                Column('Konstant1', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('plustimeminK1T1', css_class='form-group col-md-2 mb-0'),
                Column('plustimesekK1T1', css_class='form-group col-md-2 mb-0'),
                Column('plustimeminK1T2', css_class='form-group col-md-2 mb-0'),
                Column('plustimesekK1T2', css_class='form-group col-md-2 mb-0'),

            ),
            Row(
                Column('ViscosimeterNumber2', css_class='form-group col-md-6 mb-0'),
                Column('Konstant2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('plustimeminK2T1', css_class='form-group col-md-2 mb-0'),
                Column('plustimesekK2T1', css_class='form-group col-md-2 mb-0'),
                Column('plustimeminK2T2', css_class='form-group col-md-2 mb-0'),
                Column('plustimesekK2T2', css_class='form-group col-md-2 mb-0'),

            ),
            Submit('submit', 'Внести запись в журнал')
        )



    class Meta:
        model = ViscosityMJL
        fields = ['name', 'lot', 'temperature', 'termostatition', 'temperatureCheck',
                  'constit', 'oldCertifiedValue',
                  'ViscosimeterNumber1', 'Konstant1',
                  'plustimeminK1T1', 'plustimesekK1T1',
                  'plustimeminK1T2', 'plustimesekK1T2',
                  'ViscosimeterNumber2', 'Konstant2',
                  'plustimeminK2T1', 'plustimesekK2T1',
                  'plustimeminK2T2', 'plustimesekK2T2']

class CommentCreationForm(forms.ModelForm):
    name = forms.CharField(label='Комментировать', max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                                       'placeholder': 'введите текст комментария'}
                                                                ))



    class Meta:
        model = CommentsKinematicviscosity
        fields = ['name']


class ViscosityMJLUdateForm(forms.ModelForm):
    fixation = forms.BooleanField(label='АЗ',  required=False)



    class Meta:
        model = ViscosityMJL
        fields = ['fixation']


class SearchForm(forms.Form):
    query = forms.CharField()

