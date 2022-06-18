from datetime import datetime, timedelta, date


from django.db.models import Max
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView

from dinamicviscosity.models import Dinamicviscosity
from jouViscosity.forms import SearchKinematicaForm
from jouViscosity.models import *
from kinematicviscosity.models import ViscosityMJL

NAME = 'Кинематика АЗ'
NAME2 = 'Плотность и динамика АЗ'

TABLENAME = 'Кинематическая вязкость ВЖ-ПА (мм<sup>2</sup>/с)'
TABLENAME2 = 'Плотность ВЖ-ПА (г/мл)'
TABLENAME3 = 'Динамическая вязкость ВЖ-ПА  (Па*с)'
MODEL = CvKinematicviscosityVG
# now_date = datetime.now()



class AllKinematicviscosityView(ListView):
    """ Представление, которое выводит все значения кинматической вязкости из Журнала аттестованных значений"""
    """полустандартное"""
    template_name = 'jouViscosity/kinematicviscosityvalues.html'
    context_object_name = 'objects'
    def get_queryset(self):
        queryset = MODEL.objects.all().order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        return queryset
    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm()
        return context

class SearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала. """
    """нестандартное"""

    template_name = 'jouViscosity/kinematicviscosityvalues.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        if name and lot:
            objects = MODEL.objects.all().filter(id=lot)  #todo фильтр
            context['objects'] = objects
        # if name and not lot:
        #     objects = MODEL.objects.all().get(id=34)
        #     # order_by('namelot__nameVG__rangeindex', 'namelot__lot') #todo фильтр
        #     context['objects'] = objects
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm(initial={'name': name, 'lot': lot})
        return context

class DetailKinematicView(View):
    # выводит историю измерений кинематической вязкости для партии
   def get(self, request):
       object = ViscosityMJL.objects.all()
       template = 'jouViscosity/detailkinematicviscosity.html'
       context = {
           'object': object
       }
       return render(request, template, context)


class AllDinamicviscosityView(ListView):
    """ Представление, которое выводит все последние измеренные значения плотности"""
    """полустандартное"""
    template_name = 'jouViscosity/dinamicviscosityvalues.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = CvDensityVG.objects.all().order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllDinamicviscosityView, self).get_context_data(**kwargs)
        context['NAME2'] = NAME2
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        return context



