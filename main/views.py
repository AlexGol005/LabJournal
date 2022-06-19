from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404
from .models import AttestationJ, ProductionJ, CertifiedValueJ


class TextHelloView(View):
    #просто страница для примера, адрес hello
    def get(self, request: HttpRequest) -> HttpResponse:
        text = '<h1>Hello, World!!!</h1>'
        return HttpResponse(text)

class IndexView(View):
    # главная страница по основному адресу
   def get(self, request):
       return render(request, 'main/main.html')

# @login_required
class AttestationJView(View):
    # страница Журналы аттестации
   def get(self, request):
       objects = AttestationJ.objects.all()
       return render(request, 'main/attestationJ.html', {'objects': objects})


class ProductionJView(View):
    # страница Журналы приготовления

   def get(self, request):
       objects = ProductionJ.objects.all()
       return render(request, 'main/productionJ.html', {'objects': objects})


class CertifiedValueJView(View):
    # страница Журналы аттестованных значений
    def get(self, request):
        objects = CertifiedValueJ.objects.all()
        return render(request, 'main/certifiedvalueJ.html', {'objects': objects})

class EquipmentView(View):
    # страница оборудование
   def get(self, request):
       return render(request, 'main/equipment.html')




