from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from datetime import datetime
from django.utils.html import format_html
# from .models import Kalibration, Viscosimeters
from equipment.models import Equipment


class KalibrationViscosimetersForm(forms.ModelForm):
    konstant = forms.DecimalField(label='Установленная константа', max_digits=10, decimal_places=6,  required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'константа через точку'}))
    id_Viscosimeter = forms.ModelChoiceField(label='Номер вискозиметра',  required=True,
                                        queryset=Viscosimeters.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Kalibration
        fields = ['id_Viscosimeter', 'konstant']



