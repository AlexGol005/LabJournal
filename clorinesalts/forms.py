import datetime
from decimal import Decimal

from django import forms


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from clorinesalts.models import Clorinesalts, CommentsClorinesalts, IndicatorDFK, TitrantHg, GetTitrHg, DOCUMENTS, \
    MATERIAL, CHOICES, SOLVENTS, BEHAVIOUR, ClorinesaltsCV, TYPE, CommentsClorinesaltsCV

MODEL = Clorinesalts
COMMENTMODEL = CommentsClorinesalts
MATERIAL1 = MATERIAL[0:-1]


class StrJournalCreationForm(forms.ModelForm):
    """форма для внесения записи об аттестации в журнал"""
    """поменять: fields"""

    type = forms.ChoiceField(label='Назначение измерений', required=True,
                                  choices=TYPE,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    ndocument = forms.ChoiceField(label='Метод испытаний', required=True,
                                  choices=DOCUMENTS,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.ChoiceField(label='Наименование пробы', required=True,
                             choices=MATERIAL,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    namedop = forms.CharField(label='Индекс СО (пример: Х или  100) или (если выбрали "другое") полное название СО', max_length=90,
                              required=False,
                              help_text='Для СС-ТН: Х, ХПВ иил ХПВС;'
                                        ' Для ХСН: индекс ГСО, например 10; '
                                        'Для ГК: Х; Если выбрано "Другое" то укажите полное название пробы',
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '100'}))
    lot = forms.CharField(label='Партия', max_length=100, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'Партия'}))

    order_cv_value_begin = forms.CharField(label='требуемый диапазон по заказу от, мг/л', max_length=90, required=False,
                                           help_text='для ХСН-ПА указывать не нужно',
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'от'}))
    order_cv_value_end = forms.CharField(label='требуемый диапазон по заказу до, мг/л', max_length=90, required=False,
                                         help_text='для ХСН-ПА указывать не нужно',
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'до'}))


    constit = forms.ChoiceField(label='Диапазон хлористых солей по ГОСТ, мг/л', required=True,
                                choices=CHOICES,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    projectconc = forms.CharField(label='Расчётное содержание, мг/л', max_length=90, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': '000.00'}))
    que = forms.IntegerField(label='Очередность отбора', initial=1,
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
                                   queryset=TitrantHg.objects.filter(availablity='В наличии'),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    backvolume = forms.DecimalField(label='Объём холостой пробы, мл', initial=Decimal('0.08'), max_digits=4,
                                    decimal_places=2,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'placeholder': '0.00'}))
    V1E1 = forms.DecimalField(label='Х1, экстр.1, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': '00.00'}))
    V1E2 = forms.DecimalField(label='Х1, экстр.2, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V1E3 = forms.DecimalField(label='Х1, экстр.3, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E1 = forms.DecimalField(label='Х2, экстр.1, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E2 = forms.DecimalField(label='Х2, экстр.2, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E3 = forms.DecimalField(label='Х2, экстр.3, мл', max_digits=4, decimal_places=2,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V1E4 = forms.DecimalField(label='Х1, экстр.4, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V1E5 = forms.DecimalField(label='Х1, экстр.5, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E4 = forms.DecimalField(label='Х2, экстр.4, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))
    V2E5 = forms.DecimalField(label='Х2, экстр.5, мл', max_digits=4, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '00.00'}))

    aV1E1 = forms.DecimalField(label='А для Х1, экстр.1', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                      'placeholder': '1'}))
    aV1E2 = forms.DecimalField(label='А для Х1, экстр.2', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))
    aV1E3 = forms.DecimalField(label='А для Х1, экстр.3', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': '1'}))
    aV2E1 = forms.DecimalField(label='А для Х2, экстр.1', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': '1'}))
    aV2E2 = forms.DecimalField(label='А для Х2, экстр.2', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '1'}))
    aV2E3 = forms.DecimalField(label='А для Х2, экстр.3', initial=Decimal('1'), max_digits=1, decimal_places=0,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': '1'}))
    aV1E4 = forms.DecimalField(label='А для Х1, экстр.4', max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))
    aV1E5 = forms.DecimalField(label='А для Х1, экстр.5',  max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))
    aV2E4 = forms.DecimalField(label='А для Х2, экстр.4',  max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': '1'}))
    aV2E5 = forms.DecimalField(label='А для Х2, экстр.5',  max_digits=1, decimal_places=0, required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': '1'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Row(
                Column('type', css_class='form-group col-md-6 mb-0'),
                Column('ndocument', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('namedop', css_class='form-group col-md-9 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('order_cv_value_begin', css_class='form-group col-md-6 mb-0'),
                Column('order_cv_value_end', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('lot', css_class='form-group col-md-4 mb-0'),
                Column('projectconc', css_class='form-group col-md-4 mb-0'),
                Column('que', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

            Row(

                Column('constit', css_class='form-group col-md-4 mb-0'),
                Column('truevolume', css_class='form-group col-md-8 mb-0'),

                css_class='form-row'
            ),
            Row(
                Column('solvent', css_class='form-group col-md-4 mb-0'),
                Column('behaviour', css_class='form-group col-md-4 mb-0'),
                Column('lotHg', css_class='form-group col-md-4 mb-0'),
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
                HTML('Воронка №1'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp'),
                HTML('Воронка №2'),
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
        fields = ['ndocument', 'type',
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
                  'order_cv_value_begin', 'order_cv_value_end'
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

