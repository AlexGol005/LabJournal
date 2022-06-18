from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class SearchKinematicaForm(forms.Form):
    "форма для поиска по полям ЖАЗ кинематики, партия"
    "при копировании поменять поля на нужные"
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



