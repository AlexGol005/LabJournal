from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest

from .models import ViscosimeterType

class ViscosimeterTypeView(View):

    def get(self, request):
        data = {'viscosimeterType': ViscosimeterType.objects.all()}
        return render(request, 'viscosimeters/viscosimeterType.html', data)

