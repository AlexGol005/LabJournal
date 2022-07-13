from datetime import datetime, timedelta
from django.db.models import Max, Q
from django.db.models.functions import Upper
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import upper
from django.views import View
from django.views.generic import ListView, TemplateView

from equipment.forms import SearchMEForm
from equipment.models import MeasurEquipment, Verificationequipment

URL = 'equipment'

class MeasurEquipmentView(ListView):
    """ Выводит список средств измерений """
    model = MeasurEquipment
    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters__name']
    paginate_by = 12


    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

class SearchResultMeasurEquipmentView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку средств измерений """

    template_name = URL + '/measureequipment.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultMeasurEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']
        dateser = self.request.GET['dateser']
        if dateser:
            delt = datetime.now() - timedelta(days=60 * 24 * 7)

        get_id_actual = Verificationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))

        if name and not lot and not exnumber and not dateser:
            objects = MeasurEquipment.objects.\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber and not dateser:
            objects = MeasurEquipment.objects.\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and not lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot).\
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and exnumber:
            objects = MeasurEquipment.objects. \
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects

        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber, 'dateser': dateser})
        context['URL'] = URL
        return context


class StrMeasurEquipmentView(View):
    """ выводит отдельную запись и форму добавления в ЖАЗ """
    """Стандартная"""

    def get(self, request, pk):
        obj = get_object_or_404(MeasurEquipment, pk=pk)
        # form = StrJournalUdateForm()
        # try:
        #     counter = COMMENTMODEL.objects.filter(forNote=note.id)
        # except ObjectDoesNotExist:
        #     counter = None
        return render(request, URL + '/equipmentstr.html',
                      {'obj': obj})

    # def post(self, request, pk, *args, **kwargs):
    #     if MODEL.objects.get(id=pk).performer == request.user:
    #         form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
    #         if form.is_valid():
    #             order = form.save(commit=False)
    #             order.save()
    #             return redirect(order)
    #     else:
    #         form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
    #         order = form.save(commit=False)
    #         messages.success(request, f'АЗ не подтверждено! Подтвердить АЗ может только исполнитель данного измерения!')
    #         return redirect(order)