from django.views.generic import ListView

def f(MODEL, URL):
    class AllStrView(ListView):
        """ Представление, которое выводит все записи в журнале. """
        """стандартное"""
        model = MODEL
        template_name = URL + '/journal.html'
        context_object_name = 'objects'
        ordering = ['-date']
        paginate_by = 8
    return AllStrView(MODEL, URL)