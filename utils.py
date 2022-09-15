from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


class HeadView(View):
    """ Представление, которое выводит заглавную страницу журнала """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.URL = None
        self.JOURNAL = None

    def get(self, request):
        journal = self.JOURNAL
        url = self.URL
        note = journal.objects.get(for_url=url)
        return render(request, url + '/head.html', {'note': note, 'URL': url})

class CommentsView(View):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    """Стандартное"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = None
        self.URL = None
        self.template_name = None
        self.COMMENTMODEL = None
        self.MODEL = None
    def get(self, request, pk):
        note = self.COMMENTMODEL.objects.filter(forNote=pk)
        title = self.MODEL.objects.get(pk=pk)
        form = self.form
        URL = self.URL
        return render(request, 'main/comments.html', {'note': note, 'title': title, 'form': form, 'URL': URL})

    def post(self, request, pk, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.forNote = self.MODEL.objects.get(pk=pk)
            order.save()
            messages.success(request, f'Комментарий добавлен!')
            return redirect(order)