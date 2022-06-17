from datetime import datetime, timedelta

from django.db.models import Max
from django.views.generic import ListView

from dinamicviscosity.models import Dinamicviscosity
from jouViscosity.models import *
from kinematicviscosity.models import ViscosityMJL

NAME = 'Кинематика АЗ'
NAME2 = 'Плотность и динамика АЗ'

TABLENAME = 'Кинематическая вязкость ВЖ-ПА (мм<sup>2</sup>/с)'
TABLENAME2 = 'Плотность ВЖ-ПА (г/мл)'
TABLENAME3 = 'Динамическая вязкость ВЖ-ПА  (Па*с)'
MODEL = LotVG
# now_date = datetime.now()



class AllKinematicviscosityView(ListView):
    """ Представление, которое выводит все последние измеренные значения кинматической вязкости """
    """полустандартное"""
    template_name = 'jouViscosity/kinematicviscosityvalues.html'
    context_object_name = 'objects'
    def get_queryset(self):
        queryset = CvKinematicviscosityVG.objects.all().order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        return queryset
    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['now_date'] = datetime.now()
        return context


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
        context['NAME'] = NAME2
        context['TABLENAME'] = TABLENAME2
        context['now_date'] = datetime.now()
        return context

