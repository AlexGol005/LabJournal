from datetime import timedelta, date

import xlwt
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView

from dinamicviscosity.models import Dinamicviscosity
from jouViscosity.forms import SearchKinematicaForm
from jouViscosity.models import CvKinematicviscosityVG, CvDensityDinamicVG
from kinematicviscosity.models import ViscosityMJL

NAME = 'ВЖ-ПА АЗ'
NAME2 = 'Плотность и динамика АЗ'

TABLENAME = 'Кинематическая вязкость ВЖ-2-ПА (мм<sup>2</sup>/с)'
TABLENAME2 = 'Плотность/Динамическая вязкость  ВЖ-2-ПА (г/мл)/(Па*с)'
MODEL = CvKinematicviscosityVG
MODEL2 = CvDensityDinamicVG


class AllKinematicviscosityView(ListView):
    """ Представление, которое выводит все значения кинматической вязкости из Журнала аттестованных значений"""
    """полустандартное"""
    template_name = 'jouViscosity/kinematicviscosityvalues.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = MODEL.objects.filter(namelot__nameVG__nameSM__name='ВЖ-2-ПА').exclude(namelot__availability=False).\
            order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        objects2 = MODEL2.objects.exclude(namelot__availability=False).order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        objects3 = MODEL.objects.exclude(namelot__nameVG__nameSM__name='ВЖ-2-ПА').exclude(namelot__availability=False).\
            order_by('namelot__nameVG__nameSM__name', 'namelot__nameVG__rangeindex', 'namelot__lot')

        context['objects2'] = objects2
        context['objects3'] = objects3
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm()
        return context


class SearchKinematicResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала АЗ
    кинематической вязкости. """
    """нестандартное"""

    template_name = 'jouViscosity/kinematicviscosityvalues.html'

    def get_context_data(self, **kwargs):
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        context = super(SearchKinematicResultView, self).get_context_data(**kwargs)
        if name and lot:
            objects = MODEL.objects.filter(namelot__nameVG__nameSM__name='ВЖ-2-ПА').\
                filter(namelot__nameVG__name=name, namelot__lot=lot).order_by(
                'namelot__nameVG__rangeindex', 'namelot__lot')
            objects2 = MODEL2.objects.filter(namelot__nameVG__name=name, namelot__lot=lot).order_by(
                'namelot__nameVG__rangeindex', 'namelot__lot')
            objects3 = MODEL.objects.exclude(namelot__nameVG__nameSM__name='ВЖ-2-ПА').\
                filter(namelot__nameVG__name=name, namelot__lot=lot).order_by(
                'namelot__nameVG__rangeindex', 'namelot__lot')
            context['objects'] = objects
            context['objects2'] = objects2
            context['objects3'] = objects3
        if name and not lot:
            objects = MODEL.objects.filter(namelot__nameVG__nameSM__name='ВЖ-2-ПА').\
                filter(namelot__nameVG__name=name).\
                order_by('namelot__nameVG__rangeindex',  'namelot__lot')

            objects2 = MODEL2.objects.filter(namelot__nameVG__name=name).\
                order_by('namelot__nameVG__rangeindex', 'namelot__lot')

            objects3 = MODEL.objects.exclude(namelot__nameVG__nameSM__name='ВЖ-2-ПА').\
                filter(namelot__nameVG__name=name).order_by('namelot__nameVG__rangeindex', 'namelot__lot')

            context['objects'] = objects
            context['objects2'] = objects2
            context['objects3'] = objects3
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm(initial={'name': name, 'lot': lot})
        return context


class DetailKinematicView(View):
    """ выводит историю измерений кинематической вязкости для партии """
    def get(self, request, path, int, str, *args, **kwargs):
        try:
            objects = ViscosityMJL.objects.filter(fixation=True).filter(name=path).\
                filter(lot=int).filter(temperature=str)
            name = ViscosityMJL.objects.filter(fixation=True, name=path, lot=int, temperature=str)[0]
            template = 'jouViscosity/detailkinematicviscosity.html'
            context = {
                'objects': objects,
                'name': name
            }
            return render(request, template, context)
        except IndexError:
            template = 'jouViscosity/olddetailkinematicviscosity.html'
            objects = MODEL.objects.filter(namelot__nameVG__name=path, namelot__lot=int)
            context = {
                'objects': objects,
            }
            return render(request, template, context)


class AllDinamicviscosityView(ListView):
    """ Представление, которое выводит все значения динамической вязкости и плотности
    из Журнала аттестованных значений"""
    """полустандартное"""
    template_name = 'jouViscosity/dinamicviscosityvalues.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = MODEL.objects.all().order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AllDinamicviscosityView, self).get_context_data(**kwargs)
        objects2 = MODEL2.objects.all().order_by('namelot__nameVG__rangeindex', 'namelot__lot')
        context['objects2'] = objects2
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm()
        return context


class SearchDinamicResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала АЗ динамической
     вязкости. """
    """нестандартное"""

    template_name = 'jouViscosity/dinamicviscosityvalues.html'

    def get_context_data(self, **kwargs):
        context = super(SearchDinamicResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        context = super(SearchDinamicResultView, self).get_context_data(**kwargs)
        if name and lot:
            objects = MODEL.objects.filter(namelot__nameVG__name=name, namelot__lot=lot).order_by(
                'namelot__nameVG__rangeindex', 'namelot__lot')
            objects2 = MODEL2.objects.filter(namelot__nameVG__name=name, namelot__lot=lot).order_by(
                'namelot__nameVG__rangeindex', 'namelot__lot')
            context['objects'] = objects
            context['objects2'] = objects2
        if name and not lot:
            objects = MODEL.objects.filter(namelot__nameVG__name=name).\
                order_by('namelot__nameVG__rangeindex', 'namelot__lot')

            objects2 = MODEL2.objects.filter(namelot__nameVG__name=name).\
                order_by('namelot__nameVG__rangeindex', 'namelot__lot')

            context['objects'] = objects
            context['objects2'] = objects2
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['TABLENAME2'] = TABLENAME2
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchKinematicaForm(initial={'name': name, 'lot': lot})
        return context


class DetailDinamicView(View):
    """ выводит историю измерений плотности и динамической  вязкости для партии"""
    def get(self, request, path, int, str, *args, **kwargs):
        try:
            objects = Dinamicviscosity.objects.filter(fixation=True).filter(name=path).filter(lot=int).\
                filter(temperature=str)
            name = Dinamicviscosity.objects.filter(fixation=True, name=path, lot=int, temperature=str)[0]
            template = 'jouViscosity/detaildinamicviscosity.html'
            context = {
                'objects': objects,
                'name': name
            }
            return render(request, template, context)
        except IndexError:
            template = 'jouViscosity/olddetaildinamicviscosity.html'
            objects = MODEL2.objects.filter(namelot__nameVG__name=path, namelot__lot=int)
            context = {
                'objects': objects,
            }
            return render(request, template, context)

