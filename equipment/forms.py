import datetime
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django.contrib.auth.models import User
from django.forms import ModelForm

from equipment.models import MeasurEquipment, CommentsEquipment, NOTETYPE, Equipment, CHOICES, Verificators, \
    VerificatorPerson, Verificationequipment, CHOICESVERIFIC, CHOICESPLACE, CommentsVerificationequipment, Manufacturer, \
    KATEGORY, MeasurEquipmentCharakters, Personchange, Roomschange, Rooms, DocsCons, MeteorologicalParameters


class SearchMEForm(forms.Form):
    "форма для поиска по полям списка СИ и ИО"
    name = forms.CharField(label='Название', required=False,
                           help_text='введите название частично или полностью',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    exnumber = forms.CharField(label='Внут. №', required=False,
                               help_text='вн. № полн.',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    lot = forms.CharField(label='Заводской №', required=False,
                          help_text='заводской № полностью',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateser = forms.CharField(label='Поверка/атт-я истекает после', required=False,
                               help_text='дата в формате ГГГГ-ММ-ДД',
                          widget=forms.TextInput(attrs={'class': 'form-control'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('exnumber', css_class='form-group col-md-1 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Column('dateser', css_class='form-group col-md-3 mb-0'),
                Row(Submit('submit', 'Найти', css_class='btn  btn-info col-md-9 mb-3 mt-4 ml-4'))))

class NoteCreationForm(forms.ModelForm):
    """форма для  записей об оборудовании"""
    date = forms.DateField(label='Дата', required=False, initial=datetime.date.today(),
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                               '%Y-%m-%d',
                               '%m/%d/%Y',
                               '%m/%d/%y',
                               '%d.%m.%Y',
                           ))
    type = forms.ChoiceField(label='Выберите тип события', required=True,
                                  choices=NOTETYPE,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Внести запись о приборе', max_length=10000,
                           widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'placeholder': 'введите текст записи о приборе'}))
    img = forms.ImageField(label='Загрузить фото прибора или документа', required=False,
                           widget=forms.FileInput)
    author = forms.CharField(label='Автор записи', required=False,  max_length=100,
                              help_text='впишите автора если вы не авторизованы',
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CommentsEquipment
        fields = ['date', 'type', 'note', 'img', 'author']

class EquipmentCreateForm(forms.ModelForm):
    """форма для внесения ЛО"""
    exnumber = forms.CharField(label='Внутренний номер', max_length=10000, initial='А',
                               help_text='уникальный, напишите буквенную часть номера (заглавная кириллица)',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': 'А'}))
    lot = forms.CharField(label='Заводской номер', max_length=10000,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    yearmanuf = forms.CharField(label='Год выпуска', max_length=10000, initial=datetime.date.today().year,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    manufacturer = forms.ModelChoiceField(label='Производитель',
                                         queryset=Manufacturer.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(label='Статус', initial='Эксплуатация',
                               choices=CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    yearintoservice = forms.CharField(label='Год ввода в эксплуатацию', max_length=10000, initial=datetime.date.today().year,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    new = forms.ChoiceField(label='Новый или б/у', initial='новый',
                               choices=(
                                        ('новый', 'новый'),
                                        ('б/у', 'б/у')),
                               widget=forms.Select(attrs={'class': 'form-control'}))
    invnumber = forms.CharField(label='Инвентарный номер', max_length=10000, initial='б/н',  required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    kategory = forms.ChoiceField(label='Категория', initial='Средство измерения',
                               choices=KATEGORY,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    imginstruction1 = forms.ImageField(label='Паспорт', widget=forms.FileInput, required=False)
    imginstruction2 = forms.ImageField(label='Внутренняя инструкция', widget=forms.FileInput,
                                       required=False)
    imginstruction3 = forms.ImageField(label='Право владения', widget=forms.FileInput, required=False)
    individuality = forms.CharField(label='Индивидуальные особенности прибора', max_length=10000, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    notemaster = forms.CharField(label='Примечание (или временное предостережение)', max_length=10000, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    video = forms.CharField(label='Видео к прибору', max_length=10000, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'добавьте ссылку на видео'}))


    class Meta:
        model = Equipment
        fields = [
            'exnumber', 'lot', 'yearmanuf', 'manufacturer', 'status',
            'yearintoservice', 'new', 'invnumber', 'kategory', 'individuality', 'notemaster',
            'imginstruction2', 'imginstruction1',
            'imginstruction3', 'video'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('kategory', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('exnumber', css_class='form-group col-md-4 mb-0'),
                Column('lot', css_class='form-group col-md-4 mb-0'),
                Column('invnumber', css_class='form-group col-md-4 mb-0')),
            Row(
                Column('yearmanuf', css_class='form-group col-md-4 mb-0'),
                Column('manufacturer', css_class='form-group col-md-4 mb-0'),
                Column('new', css_class='form-group col-md-4 mb-0')),
            Row(
                Column('status', css_class='form-group col-md-6 mb-0'),
                Column('yearintoservice', css_class='form-group col-md-6 mb-0')),
            Row(
                Column('imginstruction1', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('imginstruction2', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('imginstruction3', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('individuality', css_class='form-group col-md-12 mb-0')),

            Row(Submit('submit', 'Записать', css_class='btn  btn-info col-md-11 mb-3 mt-4 ml-4')))



class EquipmentUpdateForm(forms.ModelForm):
    """форма для обновления разрешенных полей оборудования ответственному за оборудование"""
    status = forms.ChoiceField(label='Выберите статус прибора (если требуется изменить статус)', required=False,
                                  choices=CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    individuality = forms.CharField(label='Индивидуальные особенности прибора', max_length=10000, required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    notemaster = forms.CharField(label='Примечание (или временное предостережение)', max_length=10000, required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))
    imginstruction1 = forms.ImageField(label='Паспорт', widget=forms.FileInput, required=False)
    imginstruction2 = forms.ImageField(label='Внутренняя инструкция загрузить фото', widget=forms.FileInput,
                                       required=False)
    imginstruction3 = forms.ImageField(label='Право владения', widget=forms.FileInput, required=False)
    video = forms.CharField(label='Видео к прибору', max_length=10000, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'добавьте ссылку на видео'}))
    invnumber = forms.CharField(label='Инвентарный номер', max_length=10000, initial='б/н', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Equipment
        fields = [
            'status', 'individuality', 'notemaster', 'imginstruction1',
            'imginstruction2', 'imginstruction3',
                  'video', 'invnumber']

class ManufacturerCreateForm(forms.ModelForm):
    """форма для внесения производителя"""
    companyName = forms.CharField(label='Название компании', max_length=10000,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Страна', max_length=10000, initial = 'Россия',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyAdress = forms.CharField(label='Адрес', max_length=10000,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    telnumber = forms.CharField(label='Телефон общий', max_length=10000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    telnumberhelp = forms.CharField(label='Телефон техподдержки для вопросов по приборам', required=False,
                                    max_length=10000,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Manufacturer
        fields = [
            'companyName', 'country', 'companyAdress', 'telnumber',
            'telnumberhelp'
                  ]

class VerificationRegForm(forms.ModelForm):
    """форма для  внесения сведений о поверке"""


    date = forms.DateField(label='Дата поверки', required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': ''}),
        input_formats=(
            '%Y-%m-%d',  # '2006-10-25'
            '%m/%d/%Y',  # '10/25/2006'
            '%m/%d/%y',
            '%d.%m.%Y',
        ))
    datedead = forms.DateField(label='Дата окончания поверки', required=False,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                               '%Y-%m-%d',  # '2006-10-25'
                               '%m/%d/%Y',  # '10/25/2006'
                               '%m/%d/%y',
                               '%d.%m.%Y',
                           ))
    dateorder = forms.DateField(label='Дата заказа поверки', required=False,
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                               '%Y-%m-%d',  # '2006-10-25'
                               '%m/%d/%Y',  # '10/25/2006'
                               '%m/%d/%y',
                               '%d.%m.%Y',
                           ))
    arshin = forms.CharField(label='Ссылка на сведения о поверке в Аршин', max_length=10000,
                             required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    certnumber = forms.CharField(label='№ свидетельства о поверке', max_length=10000, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(label='Стоимость данной поверки', max_digits=10, decimal_places=2, required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': '0000.00'}))
    statusver = forms.ChoiceField(label='Результат поверки',
                               choices=CHOICESVERIFIC,
                               widget=forms.Select(attrs={'class': 'form-control'}))

    verificator = forms.ModelChoiceField(label='Организация-поверитель', required=False,
                                         queryset=Verificators.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}))
    verificatorperson = forms.ModelChoiceField(label='Имя поверителя', required=False,
                                         queryset=VerificatorPerson.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    place = forms.ChoiceField(label='Место поверки',
                             choices=CHOICESPLACE,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Примечание', max_length=10000, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    img = forms.ImageField(label='Сертификат', widget=forms.FileInput, required=False)
    year = forms.CharField(label='Год поверки', max_length=10000, required=False,
                             help_text='Укажите год если не указываете точные даты поверки',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateordernew = forms.DateField(label='Дата заказа замены', required=False,
                                   help_text='Укажите, если поверка не выгодна',
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control', 'placeholder': ''}),
                                input_formats=(
                                    '%Y-%m-%d',
                                    '%m/%d/%Y',
                                    '%m/%d/%y',
                                    '%d.%m.%Y',
                                ))


    class Meta:
        model = Verificationequipment
        fields = ['date', 'datedead', 'dateorder', 'arshin', 'certnumber',
                  'price', 'statusver',  'verificator', 'verificatorperson',
                  'place', 'note', 'year',
                  'dateordernew'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-4 mb-0'),
                Column('datedead', css_class='form-group col-md-4 mb-0'),
                Column('dateorder', css_class='form-group col-md-4 mb-0'),
                ),
            Row(
                Column('arshin', css_class='form-group col-md-12 mb-0')),
            Row(
                Column('certnumber', css_class='form-group col-md-4 mb-0'),
                Column('statusver', css_class='form-group col-md-4 mb-0'),
                Column('price', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('verificator', css_class='form-group col-md-4 mb-0'),
                Column('verificatorperson', css_class='form-group col-md-4 mb-0'),
                Column('place', css_class='form-group col-md-4 mb-0'),
            ),
            Row(
                Column('note', css_class='form-group col-md-12 mb-1')),
            Row(
                Column('img', css_class='form-group col-md-4 mb-1'),
                Column('dateordernew', css_class='form-group col-md-4 mb-1'),
                Column('year', css_class='form-group col-md-4 mb-1')),
            Submit('submit', 'Внести'))



class CommentsVerificationCreationForm(forms.ModelForm):
    """форма для комментария к истории поверки"""
    note = forms.CharField(label='Обновить комментарий отвественного', max_length=10000000,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))

    class Meta:
        model = CommentsVerificationequipment
        fields = ['note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('note', css_class='form-group col-md-10 mb-0'),
                Row(Submit('submit', 'Обновить', css_class='btn  btn-info col-md-10 mb-3 mt-4 ml-4'))))

class VerificatorsCreationForm(forms.ModelForm):
    """форма для внесения компании поверителя"""
    companyName = forms.CharField(label='Название организации', max_length=10000000,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    companyAdress = forms.CharField(label='Адрес', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    telnumber = forms.CharField(label='Телефон', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    email = forms.CharField(label='email', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    note = forms.CharField(label='Примечание', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))

    class Meta:
        model = Verificators
        fields = [
            'companyName',
            'companyAdress', 'telnumber',
            'email', 'note'
                  ]


class VerificatorPersonCreationForm(forms.ModelForm):
    """форма для внесения сотрудника поверителя"""
    company = forms.ModelChoiceField(label='Организация', required=False,
                                                         queryset=Verificators.objects.all(),
                                                         widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label='ФИО', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    departament = forms.CharField(label='Отдел', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    telnumber = forms.CharField(label='Телефон', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    email = forms.CharField(label='email', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    dop = forms.CharField(label='Примечание', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))


    class Meta:
        model = VerificatorPerson
        fields = [
            'company',
            'name', 'departament',
            'telnumber', 'email',
            'dop'
                  ]

class MeasurEquipmentCharaktersCreateForm(forms.ModelForm):
    """форма для внесения госреестра"""
    reestr = forms.CharField(label='Номер в Госреестре', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': ''}))
    name = forms.CharField(label='Название прибора', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    typename = forms.CharField(label='Тип', max_length=10000000, required=False, initial='нет типа',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': ''}))
    modificname = forms.CharField(label='Модификация', max_length=10000000, required=False, initial='нет модификации',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    calinterval = forms.CharField(label='Межповерочный интервал, месяцев', max_length=10000000, required=False,
                                  initial='12',
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': ''}))
    measurydiapason = forms.CharField(label='Диапазон измерений', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    accuracity = forms.CharField(label='Класс точности /(разряд/), погрешность и /(или/) '
                                       'неопределённость /(класс, разряд/)', max_length=10000000, required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))
    aim = forms.CharField(label='Назначение ЛО', max_length=10000000, required=False,
                          initial='Измерение массы стандартных образцов и реактивов',
                          widget=forms.TextInput(attrs={'class': 'form-control',
                                                        'placeholder': ''}))


    class Meta:
        model = MeasurEquipmentCharakters
        fields = [
            'reestr',
            'name',
            'typename',
            'modificname',
             'calinterval',
            'measurydiapason', 'accuracity',
            'aim'
                  ]

class MeasurEquipmentCreateForm(forms.ModelForm):
    """форма для внесения СИ"""
    charakters = forms.ModelChoiceField(label='Госреестр', required=False,
                                                         queryset=MeasurEquipmentCharakters.objects.all().order_by('name'),
                                                         widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = MeasurEquipment
        fields = [
            'charakters',
                  ]

class PersonchangeForm(forms.ModelForm):
    """форма для смены ответственного за ЛО"""
    person = forms.ModelChoiceField(label='Ответственный за ЛО',
                                                         queryset=User.objects.all(),
                                                         widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Personchange
        fields = [
            'person'
                  ]

class RoomschangeForm(forms.ModelForm):
    """форма для смены Размещения ЛО"""
    roomnumber = forms.ModelChoiceField(label='Номер комнаты',
                                                         queryset=Rooms.objects.all(),
                                                         widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Roomschange
        fields = [
            'roomnumber'
                  ]

class RoomsCreateForm(forms.ModelForm):
    """форма для внесения комнаты"""
    roomnumber = forms.CharField(label='Номер комнаты', widget=forms.TextInput(attrs={'class': 'form-control'}))
    person = forms.ModelChoiceField(label='Ответственный за комнату', required=False,
                                    queryset=User.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Rooms
        fields = [
            'roomnumber', 'person'
                  ]

class DocsConsCreateForm(forms.ModelForm):
    """форма для внесения документа или принадлежности"""
    date = forms.CharField(label='Дата',  initial=datetime.date.today().year,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    docs = forms.CharField(label='Наименование документа/принадлежности', initial='Паспорт',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    source = forms.CharField(label='Источник', initial='От поставщика',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Примечание', required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = DocsCons
        fields = [
            'date',
            'docs', 'source',
            'note'
                  ]


class MeteorologicalParametersRegForm(ModelForm):
    """форма для внесения условий окружающей среды в помещении"""
    date = forms.DateField(label='Дата',
                           widget=forms.DateInput(
                               attrs={'class': 'form-control', 'placeholder': ''}),
                           input_formats=(
                               '%Y-%m-%d',
                               '%m/%d/%Y',
                               '%m/%d/%y',
                               '%d.%m.%Y',
                           ))
    roomnumber = forms.ModelChoiceField(label='Помещение',
                                    queryset=Rooms.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    pressure = forms.CharField(label='Давление, кПа', required=False, initial='102.0',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    temperature = forms.CharField(label='Температура, °С',  required=False, initial='20.0',
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    humidity = forms.CharField(label='Влажность, %', required=False, initial='50',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MeteorologicalParameters
        fields = [
            'date',
            'roomnumber', 'pressure',
            'temperature', 'humidity'
                  ]
