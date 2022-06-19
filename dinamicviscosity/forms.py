import datetime
from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Dinamicviscosity, CHOICES, CommentsDinamicviscosity, DOCUMENTS, DENSITYE


MODEL = Dinamicviscosity
COMMENTMODEL = CommentsDinamicviscosity


class StrJournalCreationForm(forms.ModelForm):
    """форма для внесения записи в журнал"""
    """поменять: fields"""
    ndocument = forms.ChoiceField(label='Метод испытаний', required=True,
                                  choices=DOCUMENTS,
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

    constit = forms.ChoiceField(label='Состав пробы', widget=forms.RadioSelect, choices=CHOICES, required=True)

    olddensity = forms.CharField(label='Предыдущее аттестованное значение плотности, г/мл', required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'АЗ через точку'}
                                                        ))
    performerdensity = forms.ModelChoiceField(label='Плотность измерил', required=False,
                                              queryset=User.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-control'}))

    density1 = forms.DecimalField(label='плотность 1, г/мл (если измеряли денсиметром)', max_digits=7, decimal_places=5,
                                  required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'плотность 1 через точку'}
                                                         ))
    density2 = forms.DecimalField(label='плотность 2, г/мл (если измеряли денсиметром)', max_digits=7, decimal_places=5,
                                  required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'плотность 2 через точку'}
                                                         ))
    piknometer_volume = forms.DecimalField(label='Объём пикнометра, мл', max_digits=7, decimal_places=4, required=False,
                                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Объём пикнометра через точку'}
                                                                  ))
    piknometer_mass1 = forms.DecimalField(label='Масса пикнометра 1, г', max_digits=7, decimal_places=4, required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': '0.0000'}
                                                                 ))
    piknometer_mass2 = forms.DecimalField(label='Масса пикнометра 2, г', max_digits=7, decimal_places=4, required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': '0.0000'}
                                                                 ))
    piknometer_plus_SM_mass1 = forms.DecimalField(label='Масса пикнометра + СО 1, г', max_digits=7, decimal_places=4,
                                                  required=False,
                                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': '0.0000'}
                                                                         ))
    piknometer_plus_SM_mass2 = forms.DecimalField(label='Масса пикнометра + СО 2, г', max_digits=7, decimal_places=4,
                                                  required=False,
                                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'placeholder': '0.0000'}
                                                                         ))

    equipment = forms.ChoiceField(label='Способ измерения плотности', choices=DENSITYE,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    kinematicviscosity = forms.FloatField(label='Кинемат. вязк. при T измерений', required=False,
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
                # Column('kinematicviscosity', css_class='form-group col-md-6 mb-0'),
                Column('ndocument', css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            ),

            Row(
                Column('constit', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('density1', css_class='form-group col-md-6 mb-0'),
                Column('density2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('equipment', css_class='form-group col-md-6 mb-0'),
                Column('performerdensity', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('piknometer_volume', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('piknometer_mass1', css_class='form-group col-md-6 mb-0'),
                Column('piknometer_mass2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('piknometer_plus_SM_mass1', css_class='form-group col-md-6 mb-0'),
                Column('piknometer_plus_SM_mass2', css_class='form-group col-md-6 mb-0'),
            ),

            Submit('submit', 'Внести запись в журнал')
        )

    class Meta:
        model = MODEL
        fields = ['ndocument',
                  'name', 'lot', 'temperature',
                  'constit',
                  'density1', 'density2',
                   'performerdensity',
                  'piknometer_volume',
                  'piknometer_mass1', 'piknometer_mass2',
                  'equipment', 'piknometer_plus_SM_mass1', 'piknometer_plus_SM_mass2',
                  # 'olddensity',
                  ]


class StrJournalUdateForm(forms.ModelForm):
    """форма для  обновления записи в журнале: поле модели fixation для отправки записи в ЖАЗ"""
    """стандартная"""
    fixation = forms.BooleanField(label='АЗ', required=False)

    class Meta:
        model = MODEL
        fields = ['fixation']


class StrKinematicaForm(forms.ModelForm):
    """форма для  добавления кинематики в разработке"""
    """уникальная"""

    kinematicviscosity = forms.FloatField(label='Кинемат. вязк. при T измерений', required=False,
                                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'АЗ через точку'}
                                                                 ))
    class Meta:
        model = MODEL
        fields = ['kinematicviscosity']


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
