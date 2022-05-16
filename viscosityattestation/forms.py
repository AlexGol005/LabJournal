from django import forms

from .models import ViscosityMJL

class ViscosityMJLCreationForm(forms.ModelForm):
    name = forms.CharField(label='Наименование пробы', max_length=100, required=True)
    class Meta:
        model = ViscosityMJL
        fields = ['name']