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
    def get_queryset(self):
        get_id_t20 = ViscosityMJL.objects.filter(fixation=True).filter(temperature=20).select_related('for_lot_and_name')\
            .values('for_lot_and_name'). \
            annotate(t20=Max('id')).values('t20')
        list_ = list(get_id_t20)
        set = []
        for n in list_:
            set.append(n.get('t20'))
        queryset = ViscosityMJL.objects.select_related('for_lot_and_name').filter(id__in=set).\
            order_by('for_lot_and_name__nameVG__rangeindex', 'lot')
        return queryset

    # select_related('for_lot_and_name').filter(id__in=set)

    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        return context
