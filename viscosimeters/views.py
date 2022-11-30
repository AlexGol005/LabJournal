from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.db import connection
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView

from django.db.models import Max
from viscosimeters.models import*
from .forms import KalibrationViscosimetersForm


# class KalibrationViscosimetersRegView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
#     """ выводит форму внесения для внесения допинформации для формирования протокола и кнопку для протокола """
#     template_name = 'equipment/reg.html'
#     success_url = '/kalibrationviscosimetersreg/'
#     form_class = KalibrationViscosimetersForm
#
#     def form_valid(self, form):
#         order = form.save(commit=False)
#         order.performer = User.objects.get(username=self.request.user)
#         order.save()
#         return super().form_valid(form)

    # name = form.cleaned_data.get('id_Viscosimeter')
    # konstant = form.cleaned_data.get('konstant')
    # success_message = f'Константа {konstant} вискозиметра {name} внесена!'




@login_required
def KalibrationViscosimetersRegView(request):
    """ выводит форму внесения калибровки вискозиметров. """
    if request.method == "POST":
        form = KalibrationViscosimetersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()

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
        get_id_actualconstant = Kalibration.objects.select_related('id_Viscosimeter').values('id_Viscosimeter').\
            annotate(id_actualkonstant=Max('id')).values('id_actualkonstant')
        list_ = list(get_id_actualconstant)
        set = []
        for n in list_:
            set.append(n.get('id_actualkonstant'))
        viscosimeters = Kalibration.objects.select_related('id_Viscosimeter').filter(id__in=set).order_by('id_Viscosimeter__viscosimeterType__diameter').\
            exclude(id_Viscosimeter__equipmentSM__equipment__status__exact='Cп.')

        data = {'viscosimeters': viscosimeters}


        return render(request, 'viscosimeters/viscosimetersKonstants.html', data)



class ViscosimetersHeadView(TemplateView):
    """ выводит заглавную старницу вискозиметров """
    template_name = 'viscosimeters/head.html'




