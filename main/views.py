from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.shortcuts import get_object_or_404

from .forms import AttestationJForm, ProductionJForm
from .models import AttestationJ, ProductionJ, CertifiedValueJ


class TextHelloView(View):
    #пример
    def get(self, request: HttpRequest) -> HttpResponse:
        text = '<h1>Hello, World!!!</h1>'
        return HttpResponse(text)

class About(View):
    # о сайте
   def get(self, request):
       return render(request, 'main/about.html')

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


@login_required
def AttestationJRegView(request):
    """ выводит форму внесения журнала аттестации """
    if request.method == "POST":
        form = AttestationJForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            messages.success(request, f'Заявка принята. Сообщите о заявке разработчику по a.golovkina@petroanalytica.ru')
            return redirect('/attestationJ/')
    else:
        form = AttestationJForm()

    return render(
        request,
        'main/registrationAtt.html',
        {
            'form': form
        })

@login_required
def ProductionJRegView(request):
    """ выводит форму внесения журнала приготовления """
    if request.method == "POST":
        form = ProductionJForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            messages.success(request, f'Заявка принята. Сообщите о заявке разработчику по a.golovkina@petroanalytica.ru')
            return redirect('/productionJ/')
    else:
        form = ProductionJForm()

    return render(
        request,
        'main/registrationProd.html',
        {
            'form': form
        })




