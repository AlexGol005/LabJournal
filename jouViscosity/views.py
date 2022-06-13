from django.db.models import Max
from django.views.generic import ListView

from jouViscosity.models import *
from kinematicviscosity.models import ViscosityMJL

NAME = 'Кинематика АЗ'
TABLENAME = 'Кинематическая вязкость ВЖ-ПА при популярных температурах (мм<sup>2</sup>/с)'
MODEL = LotVG


class AllKinematicviscosityView(ListView):
    """ Представление, которое выводит все последние измеренные значения кинматической вязкости """
    """стандартное"""
    template_name = 'jouViscosity/kinematicviscosityvalues.html'
    context_object_name = 'objects'
    ordering = ['nameVG__rangeindex', 'lot']
    def get_queryset(self):
        get_id_lastSM = ViscosityMJL.objects.select_related('for_lot_and_name').values(
            'for_lot_and_name').annotate(id_lastSM=Max('id')).values('id_lastSM')
        list_ = list(get_id_lastSM)
        set = []
        for n in list_:
            set.append(n.get('get_id_lastSM'))
        querySet  = ViscosityMJL.objects.select_related('for_lot_and_name').filter(id__in=set)
        return querySet

    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        return context
