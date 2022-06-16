import datetime
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from viscosimeters.models import Viscosimeters
from .models import CHOICES, CommentsKinematicviscosity, ndocumentoptional, ViscosityMJL

MODEL = ViscosityMJL
COMMENTMODEL = CommentsKinematicviscosity


class StrJournalCreationForm(forms.ModelForm):
    """форма для внесения записи в журнал"""
    """поменять: fields, initial"""
    ndocument = forms.ChoiceField(label='Метод испытаний', required=True,
                                  choices=ndocumentoptional,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
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
    ViscosimeterNumber1 = forms.ModelChoiceField(label='номер 1', required=True,
                                  queryset=Viscosimeters.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    # ViscosimeterNumber1 = forms.CharField(label='Заводской номер вискозиметра № 1', max_length=10, required=True,
    #                                       widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                     'placeholder': '№ первого вискозиметра'}
    #                                                              ))
    # Konstant1 = forms.DecimalField(label='Константа вискозиметра № 1', max_digits=20, decimal_places=6, required=False,
    #                                widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                              'placeholder': 'Константа через точку'}
    #                                                       ))
    ViscosimeterNumber2 = forms.CharField(label='Заводской номер вискозиметра № 2', max_length=10, required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control',
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
    constit = forms.ChoiceField(label='Состав пробы', widget=forms.RadioSelect, choices=CHOICES, required=True)
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
            Row(
                Column('ndocument', css_class='form-group col-md-4 mb-0'),
                Column('termostatition', css_class='form-group col-md-4 mb-0'),
                Column('temperatureCheck', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('constit', css_class='form-group col-md-6 mb-0'),
                Column('oldCertifiedValue', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ViscosimeterNumber1', css_class='form-group col-md-6 mb-0'),
                # Column('Konstant1', css_class='form-group col-md-6 mb-0'),
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
        model = MODEL
        fields = ['name', 'lot', 'temperature', 'termostatition', 'temperatureCheck',
                  'constit', 'oldCertifiedValue',
                  'ViscosimeterNumber1',
                  'plustimeminK1T1', 'plustimesekK1T1',
                  'plustimeminK1T2', 'plustimesekK1T2',
                  'ViscosimeterNumber2', 'Konstant2',
                  'plustimeminK2T1', 'plustimesekK2T1',
                  'plustimeminK2T2', 'plustimesekK2T2', 'ndocument',
                  # 'Konstant1'
                  ]


class StrJournalUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале: поле модели fixation для отправки записи в ЖАЗ"""
    """стандартная"""
    fixation = forms.BooleanField(label='АЗ', required=False)

    class Meta:
        model = MODEL
        fields = ['fixation']


class CommentCreationForm(forms.ModelForm):
    """форма для  комментариев"""
    """стандартная"""
    name = forms.CharField(label='Комментировать', max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст комментария'}))

    class Meta:
        model = COMMENTMODEL
        fields = ['name']


class SearchForm(forms.Form):
    "форма для поиска по полям журнала ГСО, партия, температура"
    "при копировании поменять поля на нужные"
    name = forms.CharField(label='Название', initial='ВЖ-2-ПА(100)')
    lot = forms.CharField(label='Партия', initial='1', required=False)
    temperature = forms.CharField(label='Температура', initial='20', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Column('temperature', css_class='form-group col-md-3 mb-0'),
                Submit('submit', 'Найти', css_class='btn  btn-info col-md-2 mb-3 mt-4 ml-4'),
                css_class='form-row'
            ))


class SearchDateForm(forms.Form):
    "форма для поиска записей по датам"
    "стандартная"
    datestart = forms.DateField(label='От', initial=datetime.date.today,
                                    widget=forms.DateInput(attrs={'placeholder': datetime.date.today}))
    datefinish = forms.DateField(label='До', initial=datetime.date.today,
                                     widget=forms.DateInput(attrs={'placeholder': datetime.date.today}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(Column('datestart', css_class='form-group col-md-9 mb-1 ml-4')),
                Row(Column('datefinish', css_class='form-group col-md-9 mb-1 ml-4')),
                Row(Submit('submit', 'Найти', css_class='btn  btn-info col-md-9 mb-3 mt-4 ml-4')))

