from django.views.generic import ListView


class AllStrView(ListView):
    """ Представление, которое выводит все записи в журнале. """
    """стандартное"""

    def __init__(self, MODEL, URL, JOURNAL, *args):
        super().__init__(*args)
        self.URL = URL
        self.JOURNAL = JOURNAL
        self.MODEL = MODEL
    model = self.MODEL
    template_name = self.URL + '/journal.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(AllStrView, self).get_context_data(**kwargs)
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        return context
