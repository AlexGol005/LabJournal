from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.db.models import Q

# набор представлений одинаковых для всех журналов испытаний и приготовления
# основные
from equipment.models import MeteorologicalParameters


class Constants:
    URL = None
    JOURNAL = None
    template_name = None
    MODEL = None
    COMMENTMODEL = None
    form_class = None
    NAME = None
    journal = None
    SearchForm = None
    SearchDateForm = None
    paginate_by = 8


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
    model = MODEL
    context_object_name = 'objects'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super(AllStrView, self).get_context_data(**kwargs)
        context['journal'] = self.JOURNAL.objects.filter(for_url=self.URL)
        context['formSM'] = self.SearchForm
        context['formdate'] = self.SearchDateForm
        context['URL'] = self.URL
        return context


# для формирования протокола
class RoomsUpdateView(Constants, SuccessMessageMixin, UpdateView):
    """ выводит форму добавления помещения к измерению """
    def get_object(self, queryset=None):
        return get_object_or_404(self.MODEL, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(RoomsUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Добавить номер помещения где проводились измерения"
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.save()
        return redirect(f"/{self.journal}/{self.URL}/protocolbutton/{self.kwargs['pk']}")


class ProtocolbuttonView(Constants, TemplateView):
    """ Выводит кнопку для формирования протокола """
    def get_object(self): \
        return get_object_or_404(self.MODEL, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProtocolbuttonView, self).get_context_data(**kwargs)
        context['titlehead'] = "Протокол анализа"
        note = get_object_or_404(self.MODEL, pk=self.kwargs['pk'])
        context['note'] = note
        try:
            context['meteo'] = MeteorologicalParameters.objects.\
                get(Q(date__exact=note.date) & Q(roomnumber__exact=note.room))
        except:
            context['meteo'] = 1
        if note.room and note.equipment1:
            context['title'] = 'Есть все данные для формирования протокола'
        else:
            context['title'] = 'Добавьте данные для формирования протокола'
        return context


class ProtocolHeadView(Constants, UpdateView):
    """ выводит форму внесения для внесения допинформации для формирования протокола и кнопку для протокола """
    success_message = "Записано!"

    def get_object(self, queryset=None):
        return get_object_or_404(self.MODEL, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProtocolHeadView, self).get_context_data(**kwargs)
        context['title'] = "Добавить данные для протокола"
        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        try:
            MeteorologicalParameters.objects.get(Q(date__exact=order.date) & Q(roomnumber__exact=order.room))
            order.save()
            return redirect(f"/attestationJ/{self.URL}/protocolbutton/{self.kwargs['pk']}")
        except:
            return redirect('/equipment/meteoreg/')

# для поисков
class DateSearchResultView(Constants, TemplateView):
    """ Представление, которое выводит результаты поиска по датам на странице со всеми записями журнала. """
    """стандартное"""
    def get_context_data(self, **kwargs):
        context = super(DateSearchResultView, self).get_context_data(**kwargs)
        datestart = self.request.GET['datestart']
        datefinish = self.request.GET['datefinish']
        context['journal'] = self.JOURNAL.objects.filter(for_url=self.URL)
        context['formSM'] = self.SearchForm
        context['formdate'] = self.SearchDateForm(initial={'datestart': datestart, 'datefinish': datefinish})
        context['URL'] = self.URL
        try:
            objects = self.MODEL.objects.all().filter(date__range=(datestart, datefinish)).order_by('-pk')
            context['objects'] = objects
            return context
        except ValidationError:
            objects = self.MODEL.objects.filter(id=1)
            context['objects'] = objects
            context['Date'] = 'введите даты в формате'
            context['format'] = 'ГГГГ-ММ-ДД'
            return context


