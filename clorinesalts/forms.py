import datetime
from decimal import Decimal

from django import forms


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from clorinesalts.models import Clorinesalts, CommentsClorinesalts, IndicatorDFK, TitrantHg, GetTitrHg, DOCUMENTS, \
    MATERIAL, CHOICES, SOLVENTS, BEHAVIOUR, ClorinesaltsCV, TYPE, CommentsClorinesaltsCV
from .j_constants import *
from textconstants import *
from equipment.models import MeasurEquipment, Rooms

MODEL = Clorinesalts
COMMENTMODEL = CommentsClorinesalts
MATERIAL1 = MATERIAL[0:-1]



class StrJournalCreationForm(forms.ModelForm):
    """форма для внесения записи об аттестации в журнал"""
    """поменять: fields"""

    ndocument = forms.ChoiceField(label='Метод испытаний', required=True,
                                  choices=DOCUMENTS,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.ChoiceField(label='Наименование пробы', required=True,
                             choices=MATERIAL,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    index = forms.CharField(label='Индекс СО (пример: ХC или  100) или (если выбрали "другое") полное название СО', max_length=90,
                              required=False,
                              help_text='Для СС-ТН: Х, ХПВ иил ХПВС;'
                                        ' Для ХСН: индекс ГСО, например 10; '
                                        'Для ГК: Х; Если выбрано "Другое" то укажите полное название пробы',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '100'}))
    lot = forms.CharField(label='Партия', max_length=100, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Партия'}))
    range = forms.ChoiceField(label='Диапазон хлористых солей по ГОСТ, мг/л', required=True,
                                choices=CHOICES,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    seria = forms.CharField(initial='0', label='Введите уникальный номер серии измерений, например вида: "Индекс№партииМЭ" - "1506МЭ" для формирования протокола измерения однородности. Для всех измерений серии номер должен быть одинаковый. Если это не серия измерений, то в этом поле должен быть указан "0"', 
                                    help_text='',
                                    max_length=100, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'По умолчанию сюда впишите ноль'}
                                                  ))
    aim = forms.ChoiceField(label='Цель испытаний', required=True,
                                  choices=aimoptional,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    numberexample = forms.CharField(initial=' - ', label='Номер(а) флакона', max_length=100, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Впишите если требуется'}
                                                  ))   
    x1 = forms.DecimalField(label='X1, мг/л',
                                         max_digits=10, decimal_places=5, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'X1, мг/л'}
                                                                ))
    x2 = forms.DecimalField(label='X2, мг/л',
                                         max_digits=10, decimal_places=5, required=False,
                                         widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': 'X2, мг/л'}
                                                                ))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('index', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('lot', css_class='form-group col-md-3 mb-0'),
                Column('range', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('numberexample', css_class='form-group col-md-3 mb-0'),
                Column('aim', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('x1', css_class='form-group col-md-6 mb-0'),
                Column('x2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                HTML('Номер серии измерений (для протокола по однородности'),
                css_class='form-row'
            ),

            Row(
                Column('seria', css_class='form-group col-md-10 mb-0'),
                css_class='form-row'
            ),


  


            Submit('submit', 'Внести запись в журнал'))

    class Meta:
        model = MODEL
        fields = ['index', 'numberexample',
                  'name', 'lot', 'aim',
                  'range', 'x1', 'x2',
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

class CommentCVCreationForm(forms.ModelForm):
    """форма для  комментариев к расчёту АЗ"""

    name = forms.CharField(label='Комментировать', max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст комментария'}))

    class Meta:
        model = CommentsClorinesaltsCV
        fields = ['name']


class SearchForm(forms.Form):
    """форма для поиска по полям журнала ГСО, партия"""
    """при копировании поменять поля на нужные"""
    name = forms.ChoiceField(label='Наименование', required=True,
                             choices=MATERIAL1,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    namedop = forms.CharField(label='Индекс', initial='100',
                              help_text='Для СС-ТН: Х, ХПВ или ХПВС;'
                                        ' Для ХСН: индекс ГСО, например 10;',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '100'}))
    lot = forms.CharField(label='Партия', initial='10', required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('namedop', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Submit('submit', 'Найти', css_class='btn  btn-info col-md-2 mb-3 mt-4 ml-4'),
                css_class='form-row'
            ))




# оригинальные формы для титрования


class DPKForm(forms.ModelForm):
    """форма для приготовления раствора индикатора"""
    lotreakt1 = forms.CharField(label='Партия и производитель ДФК', initial='Ленреактив, п. 1 (чда)',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    lotreakt2 = forms.CharField(label='Партия и производитель спирта', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    mass = forms.DecimalField(label='Масса ДФК', initial='1.00', max_digits=3, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '0.00'}))
    volume = forms.DecimalField(label='Объём спирта, мл', initial='100', max_digits=3, decimal_places=0,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '000'}))

    class Meta:
        model = IndicatorDFK
        fields = ['lotreakt1', 'lotreakt2', 'mass', 'volume']


class TitrantHgForm(forms.ModelForm):
    """форма для приготовления раствора титранта"""
    lotreakt1 = forms.CharField(label='Нитрат ртути: партия', initial='Ленреактив, п. 1', required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    lotreakt2 = forms.CharField(label='Вода: партия', initial='Корвет-Нева, п. 1', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    lotreakt3 = forms.CharField(label='Азотная кислота: партия', initial='Ленреактив, п. 1', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    massHgNO3 = forms.DecimalField(label='Нитрат ртути, г', initial='1.67', max_digits=3, decimal_places=2,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': '0.00'}))
    volumeHNO3 = forms.DecimalField(label='Азотная кислота р-р, мл', initial='1', max_digits=3, decimal_places=1,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': '1'}))

    volumeH2O = forms.DecimalField(label='Вместимость колбы, мл', initial='1000', max_digits=4, decimal_places=0,
                                   widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': '1000'}))

    class Meta:
        model = TitrantHg
        fields = ['lotreakt1', 'lotreakt2', 'lotreakt3', 'massHgNO3', 'volumeHNO3', 'volumeH2O']


class GetTitrHgForm(forms.ModelForm):
    """форма для расчёта и внесения титра"""
    lot = forms.ModelChoiceField(label='Партия Hg(NO3)2', required=True,
                                 queryset=TitrantHg.objects.filter(availablity='В наличии'),
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    backvolume = forms.DecimalField(label='Объём холостой пробы, мл', initial='0.08', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '0.00'}))
    volumeNaCl = forms.DecimalField(label='Объём 0,01М NaCl для каждой пробы, мл', initial='10',
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': '10'}))

    volumeHGNO1 = forms.DecimalField(label='Объём Hg(NO3)2 (V1), мл',  max_digits=4, decimal_places=2,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': '00.00'}))
    volumeHGNO2 = forms.DecimalField(label='Объём Hg(NO3)2 (V2), мл', max_digits=4, decimal_places=2,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': '00.00'}))
    volumeHGNO3 = forms.DecimalField(label='Объём Hg(NO3)2 (V3), мл', max_digits=4, decimal_places=2,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': '00.00'}))

    class Meta:
        model = GetTitrHg
        fields = ['lot', 'backvolume', 'volumeNaCl', 'volumeHGNO1', 'volumeHGNO2', 'volumeHGNO3']


class ClorinesaltsCVUpdateForm(forms.ModelForm):
    """форма для расчёта АЗ"""

    clorinesalts2 = forms.ModelChoiceField(label='Выберите измерение вторым исполнителем (если требуется)', required=False,
                                  queryset=Clorinesalts.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    countmeasur = forms.BooleanField(label='Есть все результаты измерений для расчёта АЗ')

    class Meta:
        model = ClorinesaltsCV
        fields = ['clorinesalts2', 'countmeasur']

class ClorinesaltsCVUpdateFixationForm(forms.ModelForm):
    """форма для внесения АЗ"""

    fixation = forms.BooleanField(label='АЗ')


    class Meta:
        model = ClorinesaltsCV
        fields = ['fixation']


class StrTitrantHgUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале приготовления титранта по наличию: поле модели fixation """
    """стандартная"""
    availablity = forms.ChoiceField(label='Наличие', required=True,
                                choices=(('В наличии', 'В наличии'), ('Нет в наличии', 'Нет в наличии')),
                                widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = TitrantHg
        fields = ['availablity']

