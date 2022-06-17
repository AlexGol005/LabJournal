from django.db.models import Max
from django.views.generic import ListView

from dinamicviscosity.models import Dinamicviscosity
from jouViscosity.models import *
from kinematicviscosity.models import ViscosityMJL

NAME = 'Кинематика АЗ'
NAME2 = 'Плотность и динамика АЗ'

TABLENAME = 'Кинематическая вязкость ВЖ-ПА при популярных температурах (мм<sup>2</sup>/с)'
TABLENAME2 = 'Плотность ВЖ-ПА при популярных температурах (г/мл)'
TABLENAME3 = 'Кинематическая вязкость ВЖ-ПА при популярных температурах (Па*с)'
MODEL = LotVG


class AllKinematicviscosityView(ListView):
    """ Представление, которое выводит все последние измеренные значения кинматической вязкости """
    """полустандартное"""
    template_name = 'jouViscosity/kinematicviscosityvalues.html'
    context_object_name = 'objects'
    def get_queryset(self):
        get_id = ViscosityMJL.objects.filter(fixation=True).values('name', 'lot', 'temperature').\
            annotate(ac_id=Max('id')).values('name', 'lot', 'temperature', 'ac_id')
        list_ = list(get_id)
        set = []
        for n in list_:
            set.append(n.get('ac_id'))
        queryset = ViscosityMJL.objects.filter(id__in=set).select_related('for_lot_and_name')

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        return context


class AllDinamicviscosityView(ListView):
    """ Представление, которое выводит все последние измеренные значения плотности и динамики в двух табличках """
    """полустандартное"""
    template_name = 'jouViscosity/dinamicviscosityvalues.html'
    context_object_name = 'objects'
    def get_queryset(self):
        get_id = Dinamicviscosity.objects.filter(fixation=True).values('name', 'lot', 'temperature').\
            annotate(ac_id=Max('id')).values('name', 'lot', 'temperature', 'ac_id')
        list_ = list(get_id)
        set = []
        for n in list_:
            set.append(n.get('ac_id'))
        queryset = Dinamicviscosity.objects.filter(id__in=set).select_related('for_lot_and_name')
        return queryset


    def get_context_data(self, **kwargs):
        context = super(AllDinamicviscosityView, self).get_context_data(**kwargs)
        context['NAME2'] = NAME2
        context['TABLENAME2'] = TABLENAME2
        context['TABLENAME3'] = TABLENAME3
        return context

