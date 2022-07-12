from django.views.generic import ListView

from equipment.models import MeasurEquipment

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
        return context

