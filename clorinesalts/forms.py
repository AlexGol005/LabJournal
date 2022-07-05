import datetime
from decimal import Decimal

from django import forms


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from clorinesalts.models import Clorinesalts, CommentsClorinesalts, IndicatorDFK, TitrantHg, GetTitrHg, DOCUMENTS, \
    MATERIAL, CHOICES, SOLVENTS, BEHAVIOUR

MODEL = Clorinesalts
COMMENTMODEL = CommentsClorinesalts


class StrJournalCreationForm(forms.ModelForm):
    """форма для внесения записи об аттестации в журнал"""
    """поменять: fields"""

    ndocument = forms.ChoiceField(label='Метод испытаний', required=True,
                                  choices=DOCUMENTS,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.ChoiceField(label='Наименование пробы', required=True,
                             choices=MATERIAL,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    namedop = forms.CharField(label='Индекс СО или (если выбрали "другое") полное название СО', max_length=90,
                              required=False,
                              help_text='Для СС-ТН: Х, ХПВ иил ХПВС;'
                                        ' Для ХСН: индекс ГСО, например 10; '
                                        'Для ГК: Х; Если выбрано "Другое" то укажите полное название пробы',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '100'}))
    lot = forms.CharField(label='Партия', max_length=100, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Партия'}))
    constit = forms.ChoiceField(label='Диапазон хлористых солей, мг/л', required=True,
                                choices=CHOICES,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    projectconc = forms.CharField(label='Расчётное содержание хлористых солей, мг/л)', max_length=90, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '000.00'}))
    que = forms.IntegerField(label='Очередность отбора пробы', initial=1,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': '000.00'}))
    solvent = forms.ChoiceField(label='Растворитель', required=True,
                                choices=SOLVENTS,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    truevolume = forms.BooleanField(label='Для каждой экстракции: горячей воды на экстракцию '
                                          '100 мл, промывка  + 35 мл, промывка фильтра + 15 мл',
                                    required=True)

    behaviour = forms.ChoiceField(label='Поведение пробы', required=True,
                                  choices=BEHAVIOUR,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    aliquotvolume = forms.DecimalField(label='Аликвота пробы, мл', max_digits=3, decimal_places=0)
    solventvolume = forms.DecimalField(label='Объём растворителя, мл', max_digits=3, decimal_places=0)
    lotHg = forms.ModelChoiceField(label='Партия Hg(NO3)2', required=True,
                                   queryset=TitrantHg.objects.filter(availablity=True),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    backvolume = forms.DecimalField(label='Объём холостой пробы, мл', initial=Decimal('0.08'), max_digits=4,
                                    decimal_places=2,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': '0.00'}))
    V1E1 = forms.DecimalField(label='V11, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': '00.00'}))
    V1E2 = forms.DecimalField(label='V12, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V1E3 = forms.DecimalField(label='V13, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E1 = forms.DecimalField(label='V21, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E2 = forms.DecimalField(label='V22, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E3 = forms.DecimalField(label='V23, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V1E4 = forms.DecimalField(label='V14, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V1E5 = forms.DecimalField(label='V15, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E4 = forms.DecimalField(label='V24, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E5 = forms.DecimalField(label='V25, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))

    aV1E1 = forms.DecimalField(label='А11', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': '1'}))
    aV1E2 = forms.DecimalField(label='А12', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))
    aV1E3 = forms.DecimalField(label='А13', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': '1'}))
    aV2E1 = forms.DecimalField(label='А21', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': '1'}))
    aV2E2 = forms.DecimalField(label='А22', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '1'}))
    aV2E3 = forms.DecimalField(label='А23', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '1'}))
    aV1E4 = forms.DecimalField(label='А14', max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))
    aV1E5 = forms.DecimalField(label='А15',  max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))
    aV2E4 = forms.DecimalField(label='А24',  max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': '1'}))
    aV2E5 = forms.DecimalField(label='А25',  max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-4 mb-0'),
                Column('ndocument', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),

            Row(
                Column('namedop', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),

            Row(

                Column('constit', css_class='form-group col-md-4 mb-0'),
                Column('projectconc', css_class='form-group col-md-4 mb-0'),
                Column('que', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('solvent', css_class='form-group col-md-4 mb-0'),
                Column('behaviour', css_class='form-group col-md-4 mb-0'),
                Column('lotHg', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('truevolume', css_class='form-group col-md-18 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('aliquotvolume', css_class='form-group col-md-4 mb-0'),
                Column('solventvolume', css_class='form-group col-md-4 mb-0'),
                Column('backvolume', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                css_class='form-row'
            ),

            Row(
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('Воронка № 1'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('Воронка № 2'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                css_class='form-row'
            ),
            Row(
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                css_class='form-row'
            ),

            Row(
                Column('V1E1', css_class='form-group col-md-3 mb-0'),
                Column('aV1E1', css_class='form-group col-md-3 mb-0'),
                Column('V2E1', css_class='form-group col-md-3 mb-0'),
                Column('aV2E1', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('V1E2', css_class='form-group col-md-3 mb-0'),
                Column('aV1E2', css_class='form-group col-md-3 mb-0'),
                Column('V2E2', css_class='form-group col-md-3 mb-0'),
                Column('aV2E2', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('V1E3', css_class='form-group col-md-3 mb-0'),
                Column('aV1E3', css_class='form-group col-md-3 mb-0'),
                Column('V2E3', css_class='form-group col-md-3 mb-0'),
                Column('aV2E3', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('V1E4', css_class='form-group col-md-3 mb-0'),
                Column('aV1E4', css_class='form-group col-md-3 mb-0'),
                Column('V2E4', css_class='form-group col-md-3 mb-0'),
                Column('aV2E4', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('V1E5', css_class='form-group col-md-3 mb-0'),
                Column('aV1E5', css_class='form-group col-md-3 mb-0'),
                Column('V2E5', css_class='form-group col-md-3 mb-0'),
                Column('aV2E5', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),

            Submit('submit', 'Внести запись в журнал'))

    class Meta:
        model = MODEL
        fields = ['ndocument',
                  'name', 'lot', 'namedop',
                  'constit',
                  'projectconc', 'que',
                  'solvent',
                  'truevolume',
                  'behaviour', 'aliquotvolume',
                  'solventvolume', 'lotHg', 'backvolume',
                  'V1E1', 'V1E2', 'V1E3',
                  'V2E1', 'V2E2', 'V2E3',
                  'V2E4', 'V2E5', 'V1E4', 'V1E5',
                  'aV1E1', 'aV1E2', 'aV1E3',
                  'aV2E1', 'aV2E2', 'aV2E3',
                  'aV2E4', 'aV2E5', 'aV1E4', 'aV1E5',
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
    """форма для поиска по полям журнала ГСО, партия, температура"""
    """при копировании поменять поля на нужные"""
    name = forms.CharField(label='Название', initial='ВЖ-2-ПА(100)')
    lot = forms.CharField(label='Партия', initial='1', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Submit('submit', 'Найти', css_class='btn  btn-info col-md-2 mb-3 mt-4 ml-4'),
                css_class='form-row'
            ))


class SearchDateForm(forms.Form):
    """форма для поиска записей по датам"""
    """стандартная"""
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
                                 queryset=TitrantHg.objects.filter(availablity=True),
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

class ClorinesaltsCVForm(forms.ModelForm):
    """форма для расчёта и внесения АЗ"""

