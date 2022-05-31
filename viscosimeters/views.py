from django.shortcuts import render
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .models import *
from django.db.models import *

from .forms import KalibrationViscosimetersForm

@login_required
def KalibrationViscosimetersRegView(request):
    """ выводит форму внесения калибровки вискозиметров. """
    if request.method == "POST":
        form = KalibrationViscosimetersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f'Запись была успешно создана!')
            return redirect('/kalibrationviscosimetersreg/')
    else:
        form = KalibrationViscosimetersForm()

    return render(
        request,
        'viscosimeters/registration.html',
        {
            'form': form
        })

class ViscosimetersView(View):
    """ Представление, которое выводит все вискозиметры с константами. """
    def get(self, request):
        viscosimeters = Viscosimeters.objects.all()
        # viscosimeters = Viscosimeters.objects.annotate(idactualkonst=Max('kalibration__id')).values('kalibration__konstant', )
        data = {'viscosimeters': viscosimeters}


        return render(request, 'viscosimeters/viscosimetersKonstants.html', data)


class ViscosimeterTypeView(View):

    def get(self, request):
        ViscosimeterTypeObjects = Viscosimeters.objects.annotate(actualkonst=Max('kalibration__id'))

        return render(request, 'viscosimeters/viscosimeterType.html', {'ViscosimeterTypeObjects': ViscosimeterTypeObjects})

# class ViscosimetersKonstantsView(View):
#     '''должна выводить список вискозиметров с актуальными константами'''
#     def get(self, request):
#         ViscosimetersObjects = Viscosimeters.objects.order_by('viscosimeterType_id')
#         return render(request, 'viscosimeters/viscosimetersKonstants.html', {'ViscosimetersObjects': ViscosimetersObjects})


class ViscosimetersHeadView(View):
    """ выводит заглавную старницу вискозиметров """
    def get(self, request):
        return render(request, 'viscosimeters/head.html')

# рассмотреть этот вариант вьюшек
# from .forms import BbForm
# class BbCreateView(CreateView):
# template_name = 'bboard/create.html’
# form_class = BbForm
# success_url = ’/bboard/’
# def get_context_data(self, **kwargs):
# context = super().get_context_data(**kwargs)
# context[’rubrics’] = Rubric.objects.all()
# return context
