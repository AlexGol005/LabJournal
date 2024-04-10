from django import forms
from django.db.models import  Q

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *
from .j_constants import *
from textconstants import *
from .constvisc import *

input_formats = (
    '%Y-%m-%d',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%d.%m.%Y',
)

MODEL = ViscosityMJL
COMMENTMODEL = Comments

class StrJournalCreationForm(forms.ModelForm):
    """форма для внесения записи в журнал"""
    """поменять: fields, initial"""
    ndocument = forms.ChoiceField(label='Метод испытаний', required=True,
                                  choices=ndocumentoptional,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    aim = forms.ChoiceField(label='Цель испытаний', required=True,
                                  choices=aimoptional,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(initial='ВЖ-2-ПА(100)', label='Наименование пробы', max_length=100, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Наименование пробы'}
                                                  ))
    numberexample = forms.CharField(initial=' - ', label='Номер(а) флакона', max_length=100, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Впишите если требуется'}
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
    ViscosimeterNumber1 = forms.ModelChoiceField(label='вискозиметр № 1', required=True,
                                  queryset=Viscosimeters.objects.filter(equipmentSM__equipment__status='Э'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    ViscosimeterNumber2 = forms.ModelChoiceField(label='вискозиметр № 2', required=False,
                                                 queryset=Viscosimeters.objects.filter(equipmentSM__equipment__status='Э'),
                                                 widget=forms.Select(attrs={'class': 'form-control'}))
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
    seria = forms.CharField(initial='0', label='Введите уникальный номер серии измерений, например вида: "№партииГГММДД" для формирования протокола измерения однородности. Для всех измерений серии номер должен быть одинаковый. Если это не серия измерений, то в этом поле должен быть указан "0"', 
                                    help_text='',
                                    max_length=100, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'По умолчанию сюда впишите ноль'}
                                                  ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Column('temperature', css_class='form-group col-md-2 mb-0'),
                Column('numberexample', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ndocument', css_class='form-group col-md-4 mb-0'),
                Column('aim', css_class='form-group col-md-4 mb-0'),
                Column('termostatition', css_class='form-group col-md-2 mb-0'),
                Column('temperatureCheck', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('constit', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ViscosimeterNumber1', css_class='form-group col-md-6 mb-0'),
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
                css_class='form-row'
            ),
            Row(
                Column('plustimeminK2T1', css_class='form-group col-md-2 mb-0'),
                Column('plustimesekK2T1', css_class='form-group col-md-2 mb-0'),
                Column('plustimeminK2T2', css_class='form-group col-md-2 mb-0'),
                Column('plustimesekK2T2', css_class='form-group col-md-2 mb-0'),

            ),
            Row(
                Column('seria', css_class='form-group col-md-12 mb-0'),
            ),
            Submit('submit', 'Внести запись в журнал')
        )

    class Meta:
        model = MODEL
        fields = ['name', 'lot', 'temperature', 'termostatition', 'temperatureCheck',
                  'constit',
                  'ViscosimeterNumber1',
                  'plustimeminK1T1', 'plustimesekK1T1',
                  'plustimeminK1T2', 'plustimesekK1T2',
                  'ViscosimeterNumber2',
                  'plustimeminK2T1', 'plustimesekK2T1',
                  'plustimeminK2T2', 'plustimesekK2T2', 'ndocument',
                  'aim', 'numberexample', 'seria'
                  ]


class StrJournalUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале: поле модели fixation для отправки записи в ЖАЗ"""
    """стандартная"""
    fixation = forms.BooleanField(label='АЗ', required=False)

    class Meta:
        model = MODEL
        fields = ['fixation']

class StrJournalProtocolUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале: поля модели оборудование для протокола"""
    """стандартная"""
    equipment1 = forms.ModelChoiceField(label='Секундомер', required=False,
                                        queryset=MeasurEquipment.objects.\
                                        filter(Q(charakters__name__contains='Секундомер')|\
                                               Q(charakters__name__contains='секундомер')),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    equipment2 = forms.ModelChoiceField(label='Вискозиметр1', required=False,
                                        queryset=MeasurEquipment.objects. \
                                        filter(Q(charakters__name__contains='Вискозиметр') | \
                                               Q(charakters__name__contains='вискозиметр')),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    equipment3 = forms.ModelChoiceField(label='Вискозиметр2', required=False,
                                        queryset=MeasurEquipment.objects. \
                                        filter(Q(charakters__name__contains='Вискозиметр') | \
                                               Q(charakters__name__contains='вискозиметр')),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    equipment4 = forms.ModelChoiceField(label='Термометр', required=False,
                                        queryset=MeasurEquipment.objects. \
                                        filter(Q(charakters__name__contains='Термометр') | \
                                               Q(charakters__name__contains='термометр')),
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MODEL
        fields = [
             'equipment1',
            'equipment2', 'equipment3',
            'equipment4',
        ]

class StrJournalProtocolRoomUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале: поля модели оборудование для протокола"""
    """стандартная"""
    room = forms.ModelChoiceField(label='Помещение', required=False,
                                        queryset=Rooms.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = MODEL
        fields = [
            'room'
        ]


class CommentCreationForm(forms.ModelForm):
    """форма для  комментариев"""
    """стандартная"""
    class Meta:
        model = COMMENTMODEL
        fields = ['name']
        widgets = {'name': forms.Textarea(attrs={'class': 'form-control',  'placeholder': 'введите текст комментария'})}


class SearchForm(forms.Form):
    "форма для поиска по полям журнала ГСО, партия, температура"
    "при копировании поменять поля на нужные"
    name = forms.CharField(label='Название', initial='ВЖ-2-ПА(100)',
                           help_text='введите название в форме: ВЖ-2-ПА(100)',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'ВЖ-2-ПА(100)'}))
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

class SearchSeriaForm(forms.Form):
    "форма для поиска по полям серии измерений"
    "при копировании поменять поля на нужные"
    seria = forms.CharField(label='Серия измерений',  required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('ыукшф', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ))



