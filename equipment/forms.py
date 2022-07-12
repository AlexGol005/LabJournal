import datetime
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


from equipment.models import MeasurEquipment


class SearchMEForm(forms.Form):
    "форма для поиска по полям списка СИ"
    "при копировании поменять поля на нужные"
    name = forms.CharField(label='Название', required=False,
                           help_text='введите название частично или полностью',
                           widget=forms.TextInput(attrs={'class': 'form-control' }))
    exnumber = forms.CharField(label='Внут. №', initial='В005', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'В005'}))
    lot = forms.CharField(label='Заводской №', initial='160716002', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '160716002'}))
    datedead = forms.CharField(label='Поверка истекает после', initial='2022-07-12', required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2022-07-12'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-5 mb-0'),
                Column('exnumber', css_class='form-group col-md-1 mb-0'),
                Column('lot', css_class='form-group col-md-2 mb-0'),
                Column('datedead', css_class='form-group col-md-2 mb-0'),
                Row(Submit('submit', 'Найти', css_class='btn  btn-info col-md-9 mb-3 mt-4 ml-4'))))

