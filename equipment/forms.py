import datetime
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


from equipment.models import MeasurEquipment, CommentsEquipment, NOTETYPE, Equipment, CHOICES, Verificators, \
    VerificatorPerson, Verificationequipment, CHOICESVERIFIC, CHOICESPLACE, CommentsVerificationequipment


class SearchMEForm(forms.Form):
    "форма для поиска по полям списка СИ"
    name = forms.CharField(label='Название', required=False,
                           help_text='введите название частично или полностью',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    exnumber = forms.CharField(label='Внут. №', required=False,
                               help_text='вн. № полн.',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    lot = forms.CharField(label='Заводской №', required=False,
                          help_text='заводской № полностью',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    dateser = forms.CharField(label='Поверка истекает после', required=False,
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
        fields = ['type', 'note', 'img', 'author']

class EquipmentCreateForm(forms.ModelForm):
    """форма для обновления разрешенных полей оборудования ответственному за оборудование"""
    status = forms.ChoiceField(label='Выберите статус прибора (если требуется изменить статус)', required=False,
                                  choices=CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    individuality = forms.CharField(label='Индивидуальные особенности прибора', max_length=10000, required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    notemaster = forms.CharField(label='Примечание (или временное предостережение)', max_length=10000, required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))
    imginstruction2 = forms.ImageField(label='Внутренняя инструкция загрузить фото',  widget=forms.FileInput,
                                       required=False,)
    video = forms.CharField(label='Видео к прибору', max_length=10000, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'добавьте ссылку на видео'}))
    # exnumber = models.CharField('Внутренний номер', max_length=100, default='', blank=True, null=True, unique=True)
    # exnumber = forms.CharField(label='Внутренний номер', max_length=10000,
    #                            help_text='уникальный, шаблон А001',
    #                        widget=forms.Textarea(attrs={'class': 'form-control',
    #                                                     'placeholder': 'А001'}))
    # lot = models.CharField('Заводской номер', max_length=100, default='')
    # yearmanuf = models.IntegerField('Год выпуска', default='', blank=True, null=True)
    # manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT, verbose_name='Производитель')
    # status = models.CharField(max_length=300, choices=CHOICES, default='В эксплуатации', null=True,
    #                           verbose_name='Статус')
    # yearintoservice = models.IntegerField('Год ввода в эксплуатацию', default='0', blank=True, null=True)
    # new = models.CharField('Новый или б/у', max_length=100, default='новый')
    # invnumber = models.CharField('Инвентарный номер', max_length=100, default='', blank=True, null=True)
    # kategory = models.CharField(max_length=300, choices=KATEGORY, default='Средство измерения', null=True,
    #                             verbose_name='Категория')
    # imginstruction1 = models.ImageField('Паспорт', upload_to='user_images', blank=True, null=True,
    #                                     default='user_images/default.png')
    # imginstruction2 = models.ImageField('Внутренняя инструкция', upload_to='user_images', blank=True, null=True,
    #                                     default='user_images/default.png')
    # imginstruction3 = models.ImageField('Право владения', upload_to='user_images', blank=True, null=True,
    #                                     default='user_images/default.png')
    # individuality = models.TextField('Индивидуальные особенности прибора', blank=True, null=True)
    # video = models.CharField('Ссылка на видео', max_length=1000, blank=True, null=True)
    # notemaster = models.TextField('Примечание ответственного за прибор', blank=True, null=True)


    class Meta:
        model = Equipment
        fields = ['status', 'individuality', 'notemaster', 'imginstruction2', 'video']


class EquipmentUpdateForm(forms.ModelForm):
    """форма для обновления разрешенных полей оборудования ответственному за оборудование"""
    status = forms.ChoiceField(label='Выберите статус прибора (если требуется изменить статус)', required=False,
                                  choices=CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    individuality = forms.CharField(label='Индивидуальные особенности прибора', max_length=10000, required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    notemaster = forms.CharField(label='Примечание (или временное предостережение)', max_length=10000, required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control'}))
    imginstruction2 = forms.ImageField(label='Внутренняя инструкция загрузить фото',  widget=forms.FileInput,
                                       required=False,)
    video = forms.CharField(label='Видео к прибору', max_length=10000, required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'добавьте ссылку на видео'}))


    class Meta:
        model = Equipment
        fields = ['status', 'individuality', 'notemaster', 'imginstruction2', 'video']


class VerificationRegForm(forms.ModelForm):
    """форма для  внесения сведений о поверке"""

    date = forms.DateField(label='Дата поверки',
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
    arshin = forms.CharField(label='Ссылка на сведения о поверке в Аршин', max_length=10000, required=False,
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


    class Meta:
        model = Verificationequipment
        fields = ['date', 'datedead', 'dateorder', 'arshin', 'certnumber',
                  'price', 'statusver',  'verificator', 'verificatorperson',
                  'place', 'note'
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

