from django.shortcuts import render
from django.http import HttpResponse
from .models import ViscosityMJL

def viscositymeasurement(request):
    data = {'title': 'Определение кинематической вязкости',
            'table': ViscosityMJL.objects.all()
            }
    return render(request, 'viscosityattestation/JL.html', data)