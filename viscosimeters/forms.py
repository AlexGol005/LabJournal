from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from datetime import datetime
from django.utils.html import format_html
from .models import Viscosimeters, Status, Manufacturer, ViscosimeterType





class ViscosimetersCreationForm(forms.ModelForm):
    serialNumber = forms.CharField(label='Заводской номер', max_length=30,  required=True,
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Заводской номер'}
                                                            ))
    konstant = forms.DecimalField(label='Константа', max_digits=10, decimal_places=6,
                                  widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'placeholder': 'Константа'}
                                                            ))
    diameter = forms.ModelChoiceField(label='Диаметр', queryset=ViscosimeterType.objects.all())
    # viscosity1000 = forms.ModelChoiceField(ViscosimeterType.objects.all(), label='вязкость/1000')
    dateCal = forms.DateField(label='Дата калибровки',  widget=forms.SelectDateWidget())
    datePov = forms.DateField(label='Дата поверки',  widget=forms.SelectDateWidget())
    datePovDedlain = forms.DateField(label='Дата окончания поверки', widget=forms.SelectDateWidget())
    companyName = forms.ModelChoiceField(label='Производитель', queryset=Manufacturer.objects.all())
    # range = forms.ModelChoiceField(ViscosimeterType.objects.all(),  label='Область измерений, сСт')
    status = forms.ModelChoiceField(Status.objects.all(), label='Статус')



    class Meta:
        model = Viscosimeters
        fields = '__all__'
