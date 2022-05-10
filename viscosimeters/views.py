from django.shortcuts import render
from django.http import HttpResponse

def viscosimeters_list(request):
    return HttpResponse('<h3>Список вискозиметров</h3>')
