from datetime import datetime, timedelta, date

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, TemplateView

from clorinesalts.forms import SearchForm
from dinamicviscosity.models import Dinamicviscosity
from jouChlorineOilProducts.models import CVclorinesaltsCSN
from jouViscosity.forms import SearchKinematicaForm
from jouViscosity.models import CvKinematicviscosityVG, CvDensityDinamicVG
from kinematicviscosity.models import ViscosityMJL

NAME = 'ХСН-ПА АЗ'

TABLENAME = 'Содержание хлористых солей ХСН-ПА (мг/л)'
MODEL = CVclorinesaltsCSN



class AllView(ListView):
    """ Представление, которое выводит все значения  из Журнала аттестованных значений"""
    """полустандартное"""
    template_name = 'jouChlorineOilProducts/clorinesaltsvalues.html'
    context_object_name = 'objects'
    def get_queryset(self):
        queryset = MODEL.objects.all.order_by('namelot__nameSM__rangeindex', 'namelot__lot')
        return queryset
    def get_context_data(self, **kwargs):
        context = super(AllView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchForm()
        return context

class SearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала АЗ кинематической вязкости. """
    """нестандартное"""

    template_name = 'jouChlorineOilProducts/clorinesaltsvalues.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        namedop = self.request.GET['namedop']
        lot = self.request.GET['lot']
        context = super(SearchResultView, self).get_context_data(**kwargs)
        if name and lot:
            objects = MODEL.objects.filter(namelot__nameSM__name=name, namelot__nameSM__rangeindex=namedop, namelot__lot=lot).order_by(
                'namelot__nameSM__rangeindex', 'namelot__lot')
            context['objects'] = objects
        if name and not lot:
            objects = MODEL.objects.filter(namelot__nameSM__name=name, namelot__nameSM__rangeindex=namedop
                                           ).order_by(
                'namelot__nameSM__rangeindex', 'namelot__lot')

            context['objects'] = objects
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        context['now'] = date.today()
        context['now_date_plusmonth'] = date.today() + timedelta(days=30)
        context['form'] = SearchForm(initial={'name': name, 'lot': lot})
        return context

# class DetailView(View):
#     """ выводит историю измерений кинематической вязкости для партии """
#     def get(self, request, path, int, str, *args, **kwargs):
#         try:
#             objects = ViscosityMJL.objects.filter(fixation=True).filter(name=path).filter(lot=int).filter(temperature=str)
#             name = ViscosityMJL.objects.filter(fixation=True, name=path, lot=int, temperature=str)[0]
#             template = 'jouChlorineOilProducts/detailkinematicviscosity.html'
#             context = {
#                 'objects': objects,
#                 'name': name
#             }
#             return render(request, template, context)
#         except IndexError:
#             template = 'jouChlorineOilProducts/olddetailkinematicviscosity.html'
#             objects = MODEL.objects.filter(namelot__nameVG__name=path, namelot__lot=int)
#             context = {
#                 'objects': objects,
#             }
#             return render(request, template, context)



