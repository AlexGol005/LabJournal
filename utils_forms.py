import datetime
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

input_formats = (
    '%Y-%m-%d',
    '%m/%d/%Y',
    '%m/%d/%y',
    '%d.%m.%Y',
)


class SearchDateForm(forms.Form):
    """форма для поиска записей по датам"""
    datestart = forms.DateField(label='От', initial=datetime.date.today,
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control', 'placeholder': ''}))
    datefinish = forms.DateField(label='До', initial=datetime.date.today,
                                 widget=forms.DateInput(attrs={'placeholder': datetime.date.today}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Row(Column('datestart', css_class='form-group col-md-9 mb-1 ml-4')),
                Row(Column('datefinish', css_class='form-group col-md-9 mb-1 ml-4')),
                Row(Submit('submit', 'Найти', css_class='btn  btn-info col-md-9 mb-3 mt-4 ml-4')))
