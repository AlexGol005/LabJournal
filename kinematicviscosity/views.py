# все стандратно кроме поиска по полям, импорта моделей и констант
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from main.models import AttestationJ
from viscosimeters.models import Kalibration
from .models import ViscosityMJL, CommentsKinematicviscosity
from .forms import StrJournalCreationForm, StrJournalUdateForm, CommentCreationForm, SearchForm, SearchDateForm

JOURNAL = AttestationJ
MODEL = ViscosityMJL
COMMENTMODEL = CommentsKinematicviscosity
URL = 'kinematicviscosity'
NAME = 'кинематика'


class HeadView(View):
    """ Представление, которое выводит заглавную страницу журнала """
    """ Стандартное """

    def get(self, request):
        note = JOURNAL.objects.all().filter(for_url=URL)
        return render(request, URL + '/head.html', {'note': note, 'URL': URL})


class StrJournalView(View):
    """ выводит отдельную запись и форму добавления в ЖАЗ """
    """Стандартная"""

    def get(self, request, pk):
        note = get_object_or_404(MODEL, pk=pk)
        form = StrJournalUdateForm()
        try:
            counter = COMMENTMODEL.objects.filter(forNote=note.id)
        except ObjectDoesNotExist:
            counter = None
        return render(request, URL + '/str.html',
                      {'note': note, 'form': form, 'URL': URL, 'NAME': NAME, 'counter': counter})

    def post(self, request, pk, *args, **kwargs):
        if MODEL.objects.get(id=pk).performer == request.user:
            form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect(order)
        else:
            form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
            order = form.save(commit=False)
            messages.success(request, f'АЗ не подтверждено! Подтвердить АЗ может только исполнитель данного измерения!')
            return redirect(order)



@login_required
def RegNoteJournalView(request):
    """ Представление, которое выводит форму регистрации в журнале. """
    """Стандартное, но со вставкой по поводу констант"""
    if request.method == "POST":
        form = StrJournalCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            """вставка начало"""
            get_id_actualconstant1 = Kalibration.objects.select_related('id_Viscosimeter'). \
                filter(id_Viscosimeter__exact=order.ViscosimeterNumber1). \
                values('id_Viscosimeter').annotate(id_actualkonstant=Max('id')).values('id_actualkonstant')
            list_ = list(get_id_actualconstant1)
            set = list_[0].get('id_actualkonstant')
            aktualKalibration1 = Kalibration.objects.get(id=set)
            get_id_actualconstant2 = Kalibration.objects.select_related('id_Viscosimeter'). \
                filter(id_Viscosimeter__exact=order.ViscosimeterNumber2). \
                values('id_Viscosimeter').annotate(id_actualkonstant=Max('id')).values('id_actualkonstant')
            list_ = list(get_id_actualconstant2)
            set = list_[0].get('id_actualkonstant')
            aktualKalibration2 = Kalibration.objects.get(id=set)
            order.Konstant1 = aktualKalibration1.konstant
            order.Konstant2 = aktualKalibration2.konstant
            """вставка окончание"""
            order.save()
            messages.success(request, f'Запись внесена, подтвердите АЗ!')
            return redirect(order)
    else:
        form = StrJournalCreationForm()
    return render(request, URL + '/registration.html', {'form': form, 'URL': URL})


class CommentsView(View):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    """Стандартное"""
    form_class = CommentCreationForm
    initial = {'key': 'value'}
    template_name = URL + '/comments.html'

    def get(self, request, pk):
        note = COMMENTMODEL.objects.filter(forNote=pk)
        title = MODEL.objects.get(pk=pk)
        form = CommentCreationForm()
        return render(request, 'main/comments.html', {'note': note, 'title': title, 'form': form, 'URL': URL})

    def post(self, request, pk, *args, **kwargs):
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.forNote = MODEL.objects.get(pk=pk)
            order.save()
            messages.success(request, f'Комментарий добавлен!')
            return redirect(order)


class AllStrView(ListView):
    """ Представление, которое выводит все записи в журнале. """
    """стандартное"""
    model = MODEL
    template_name = URL + '/journal.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super(AllStrView, self).get_context_data(**kwargs)
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm()
        context['formdate'] = SearchDateForm()
        context['URL'] = URL
        return context

class SearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала. """
    """нестандартное"""

    template_name = URL + '/journal.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        temperature = self.request.GET['temperature']
        if name and lot and temperature:
            objects = MODEL.objects.filter(name=name).filter(lot=lot).filter(temperature=temperature).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and lot and not temperature:
            objects = MODEL.objects.filter(name=name).filter(lot=lot).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and not lot and not temperature:
            objects = MODEL.objects.filter(name=name).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        if name and temperature and not lot:
            objects = MODEL.objects.filter(name=name).filter(temperature=temperature).filter(fixation=True).order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm(initial={'name': name, 'lot': lot, 'temperature': temperature})
        context['formdate'] = SearchDateForm()
        context['URL'] = URL
        return context

class DateSearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска по датам на странице со всеми записями журнала. """
    """стандартное"""

    template_name = URL + '/journal.html'

    def get_context_data(self, **kwargs):
        context = super(DateSearchResultView, self).get_context_data(**kwargs)
        datestart = self.request.GET['datestart']
        datefinish = self.request.GET['datefinish']
        try:
            objects = MODEL.objects.all().filter(date__range=(datestart, datefinish)).order_by('-pk')
            context['objects'] = objects
            context['journal'] = JOURNAL.objects.filter(for_url=URL)
            context['formSM'] = SearchForm()
            context['formdate'] = SearchDateForm(initial={'datestart': datestart, 'datefinish': datefinish})
            context['URL'] = URL
            return context
        except ValidationError:
            objects = MODEL.objects.filter(id=1)
            context['objects'] = objects
            context['journal'] = JOURNAL.objects.filter(for_url=URL)
            context['formSM'] = SearchForm()
            context['formdate'] = SearchDateForm(initial={'datestart': datestart, 'datefinish': datefinish})
            context['URL'] = URL
            context['Date'] = 'введите даты в формате'
            context['format'] = 'ГГГГ-ММ-ДД'
            return context

def filterview(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр """
    """Стандартная"""
    journal = JOURNAL.objects.filter(for_url=URL)
    objects = MODEL.objects.all()
    formSM = SearchForm()
    formdate = SearchDateForm()
    if pk == 1:
        now = datetime.now() - timedelta(minutes=60 * 24 * 7)
        objects = objects.filter(date__gte=now).order_by('-pk')
    elif pk == 2:
        now = datetime.now()
        objects = objects.filter(date__gte=now).order_by('-pk')
    elif pk == 3:
        objects = objects.order_by('-pk')
    elif pk == 4:
        objects = objects.filter(fixation__exact=True).order_by('-pk')
    elif pk == 5:
        objects = objects.filter(performer=request.user).order_by('-pk')
    elif pk == 6:
        objects = objects.filter(performer=request.user).filter(fixation__exact=True).order_by('-pk')
    elif pk == 7:
        objects = objects.filter(performer=request.user).filter(fixation__exact=True).filter(
            date__gte=datetime.now()).order_by('-pk')
    return render(request, URL + "/journal.html", {'objects': objects, 'journal': journal, 'formSM': formSM, 'URL': URL,
                                                   'formdate': formdate})

# class StrKinematicviscosityDetailView(DetailView):
#     """ Представление, которое позволяет вывести отдельную запись (запасная версия). """
#     model = MODEL
#     pk_url_kwarg = "pk"
#     context_object_name = "note"
#
#     template_name = 'kinematicviscosity/str.html'
# docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/
# class CreateWork(CreateView):
#     model = MODEL
#     fields = ['name',  'lot']
#     template_name = 'kinematicviscosity/test.html'
#     success_url = '/'
#
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(CreateWork, self).form_valid(form)


# url of this view is 'search_result'
