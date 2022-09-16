from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, UpdateView, ListView

# набор представлений одинаковых для всех журналов испытаний и приготовления

class Constants:
    URL = None
    JOURNAL = None
    template_name = None
    MODEL = None
    COMMENTMODEL = None
    form_class = None
    NAME = None


class HeadView(Constants, TemplateView):
    """ Выводит заглавную страницу журнала """
    def get_context_data(self, **kwargs):
        context = super(HeadView, self).get_context_data(**kwargs)
        context['note'] = self.JOURNAL.objects.get(for_url=self.URL)
        context['URL'] = self.URL
        return context


class StrJournalView(Constants, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """ выводит отдельную запись и форму добавления в ЖАЗ """

    def get_object(self, queryset=None):
        return get_object_or_404(self.MODEL, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StrJournalView, self).get_context_data(**kwargs)
        context['note'] = get_object_or_404(self.MODEL, pk=self.kwargs['pk'])
        context['NAME'] = self.NAME
        context['URL'] = self.URL
        precounter = self.COMMENTMODEL.objects.filter(forNote=self.kwargs['pk']).count()
        counter = True if precounter > 0 else False
        context['counter'] = counter
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.author = User.objects.get(username=self.request.user)
        if self.MODEL.objects.get(id=self.kwargs['pk']).performer == self.request.user:
            order.save()
            return super().form_valid(form)
        else:
            messages.success(self.request,
                             f'АЗ не подтверждено! Подтвердить АЗ может только исполнитель данного измерения!')
            return redirect(order)


class CommentsView(Constants, SuccessMessageMixin, CreateView):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    template_name = 'main/comments.html'
    success_message = "Комментарий добавлен!"

    def get_context_data(self, **kwargs):
        context = super(CommentsView, self).get_context_data(**kwargs)
        context['title'] = self.MODEL.objects.get(pk=self.kwargs['pk'])
        context['note'] = self.COMMENTMODEL.objects.filter(forNote=self.kwargs['pk'])
        context['URL'] = self.URL
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.author = User.objects.get(username=self.request.user)
        order.forNote = self.MODEL.objects.get(pk=self.kwargs['pk'])
        order.save()
        return super().form_valid(form)


class RegView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """ Представление, которое выводит форму регистрации в журнале. """
    template_name = None
    form_class = None
    success_message = " "

    def form_valid(self, form):
        order = form.save(commit=False)
        order.performer = User.objects.get(username=self.request.user)
        order.save()
        return super().form_valid(form)


class AllStrView(Constants, ListView):
    """ Представление, которое выводит все записи в журнале. """
    """стандартное"""
    MODEL = None
    SearchForm = None
    SearchDateForm = None
    model = MODEL
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(AllStrView, self).get_context_data(**kwargs)
        context['journal'] = self.JOURNAL.objects.filter(for_url=self.URL)
        context['formSM'] = self.SearchForm
        context['formdate'] = self.SearchDateForm
        context['URL'] = self.URL
        return context

