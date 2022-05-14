from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest

from .models import ViscosimeterType

# def ViscosimeterTypeView(request):
#     ViscosimeterTypeObjects = ViscosimeterType.objects.all()
#     return render(request, 'viscosimeters/viscosimeterType.html', {'ViscosimeterTypeObjects': ViscosimeterTypeObjects})


class ViscosimeterTypeView(View):

    def get(self, request):
        ViscosimeterTypeObjects = ViscosimeterType.objects.all()
        return render(request, 'viscosimeters/viscosimeterType.html', {'ViscosimeterTypeObjects': ViscosimeterTypeObjects})


