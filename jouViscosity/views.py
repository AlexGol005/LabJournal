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
        get_id_t25 = ViscosityMJL.objects.filter(fixation=True).filter(temperature=25).select_related(
            'for_lot_and_name') \
            .values('for_lot_and_name'). \
            annotate(t25=Max('id')).values('t25')
        get_id_t40 = ViscosityMJL.objects.filter(fixation=True).filter(temperature=40).select_related(
            'for_lot_and_name') \
            .values('for_lot_and_name'). \
            annotate(t40=Max('id')).values('t40')
        get_id_t50 = ViscosityMJL.objects.filter(fixation=True).filter(temperature=50).select_related(
            'for_lot_and_name') \
            .values('for_lot_and_name'). \
            annotate(t50=Max('id')).values('t50')
        get_id_t80 = ViscosityMJL.objects.filter(fixation=True).filter(temperature=80).select_related(
            'for_lot_and_name') \
            .values('for_lot_and_name'). \
            annotate(t80=Max('id')).values('t80')
        get_id_t100 = ViscosityMJL.objects.filter(fixation=True).filter(temperature=100).select_related(
            'for_lot_and_name') \
            .values('for_lot_and_name'). \
            annotate(t100=Max('id')).values('t100')
        list20 = list(get_id_t20)
        list25 = list(get_id_t25)
        list40 = list(get_id_t40)
        list50 = list(get_id_t50)
        list80 = list(get_id_t80)
        list100 = list(get_id_t100)
        set = []
        for n in list20:
            set.append(n.get('t20'))
        for n in list25:
            set.append(n.get('t25'))
        for n in list40:
            set.append(n.get('t40'))
        for n in list50:
            set.append(n.get('t50'))
        for n in list80:
            set.append(n.get('t80'))
        for n in list100:
            set.append(n.get('t100'))
        #
        # get_id = LotVG.objects.prefetch_related("viscositymjl_set").values('nameVG__name', 'lot', 'viscositymjl__temperature').annotate(ac=Max('viscositymjl'))
        # list_ = list(get_id)
        # set = []
        # for n in list_:
        #     set.append(n.get('ac'))
        # queryset = LotVG.objects.prefetch_related("queryset1_set")
        # queryset = [{'name': 'ВЖ1 п 1', 'cv': 200, 'lot': 1, 'temperature': 20},
        #             {'name': 'ВЖ1 п 1', 'cv': '-', 'lot': 1, 'temperature': 25},
        #             {'name': 'ВЖ1 п 1', 'cv': 0, 'lot': 1, 'temperature': 40},
        #             {'name': 'ВЖ1 п 1', 'cv': 100, 'lot': 1, 'temperature': 50},
        #             {'name': 'ВЖ1 п 1', 'cv': 0, 'lot': 1, 'temperature': 80},
        #             {'name': 'ВЖ1 п 1', 'cv': 100, 'lot': 1, 'temperature': 100},
        #             {'name': 'ВЖ2', 'cv': 2000, 'lot': 1, 'temperature': 20},
        #             {'name': 'ВЖ2', 'cv': 500, 'lot': 1, 'temperature': 50},
        #             {'name': 'ВЖ3', 'cv': 5, 'lot': 1, 'temperature': 20}]
        # get_id = LotVG.objects.prefetch_related("viscositymjl_set").values('nameVG__name', 'lot', 'viscositymjl__temperature').annotate(ac=Max('viscositymjl'))
        # list_ = list(get_id)
        # set = []
        # for n in list_:
        #     set.append(n.get('ac'))
        queryset = ViscosityMJL.objects.filter(id__in=set).order_by('temperature')
        return queryset

# .annotate(ac=Max('viscositymjl_set'))
    # order_by('nameVG__rangeindex', 'lot')
    # filter(viscositymjl__fixation=True).
    # select_related('for_lot_and_name').filter(id__in=set)

    def get_context_data(self, **kwargs):
        context = super(AllKinematicviscosityView, self).get_context_data(**kwargs)
        context['NAME'] = NAME
        context['TABLENAME'] = TABLENAME
        return context
