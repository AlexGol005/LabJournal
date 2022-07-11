# все стандратно кроме поиска по полям, импорта моделей и констант
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from jouViscosity.models import CvKinematicviscosityVG, CvDensityDinamicVG
from kinematicviscosity.models import ViscosityMJL
from main.models import AttestationJ
from .models import Dinamicviscosity, CommentsDinamicviscosity
from .forms import StrJournalCreationForm, StrJournalUdateForm, CommentCreationForm, SearchForm, SearchDateForm, \
    StrKinematicaForm

JOURNAL = AttestationJ
MODEL = Dinamicviscosity
COMMENTMODEL = CommentsDinamicviscosity
URL = 'dinamicviscosity'
NAME = 'динамика'



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
                      {'note': note, 'form': form, 'URL': URL, 'NAME': NAME, 'counter': counter,
                       # 'formkinematica': formkinematica
                       })

    def post(self, request, pk, *args, **kwargs):
        form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
        if MODEL.objects.get(id=pk).performer == request.user:
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                messages.success(request, f'Запись внесена, подтвердите АЗ!')
                return redirect(order)
        else:
            form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
            order = form.save(commit=False)
            messages.success(request, f'АЗ не подтверждено! Подтвердить АЗ может только исполнитель данного измерения!')
            return redirect(order)


@login_required
def RegNoteJournalView(request):
    """ Представление, которое выводит форму регистрации в журнале. """
    """Полустандартное со уникальной вставкой"""
    if request.method == "POST":
        form = StrJournalCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            """вставка начало"""
            try:
                olddencity = CvDensityDinamicVG.objects.get(namelot__nameVG__name=order.name, namelot__lot=order.lot)
                if order.temperature == 20:
                    order.olddensity = olddencity.cvt20

                if order.temperature == 25:
                    order.olddensity = olddencity.cvt25

                if order.temperature == 40:
                    order.olddensity = olddencity.cvt40

                if order.temperature == 50:
                    order.olddensity = olddencity.cvt50

                if order.temperature == 60:
                    order.olddensity = olddencity.cvt60

                if order.temperature == 80:
                    order.olddensity = olddencity.cvt80

                if order.temperature == 100:
                    order.olddensity = olddencity.cvt100

                if order.temperature == 150:
                    order.olddensity = olddencity.cvt150

                if order.temperature == -20:
                    order.olddensity = olddencity.cvtminus20
            except ObjectDoesNotExist:
                pass

            try:
                kinematicviscosity = CvKinematicviscosityVG.objects.get(namelot__nameVG__name=order.name,
                                                                        namelot__lot=order.lot)
                if order.temperature == 20:
                    if kinematicviscosity.cvt20dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt20
                        order.kinematicviscositydead = kinematicviscosity.cvt20dead
                if order.temperature == 25:
                    if kinematicviscosity.cvt25dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt25
                        order.kinematicviscositydead = kinematicviscosity.cvt25dead
                if order.temperature == 40:
                    if kinematicviscosity.cvt40dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt40
                        order.kinematicviscositydead = kinematicviscosity.cvt40dead
                if order.temperature == 50:
                    if kinematicviscosity.cvt50dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt50
                        order.kinematicviscositydead = kinematicviscosity.cvt50dead
                if order.temperature == 60:
                    if kinematicviscosity.cvt60dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt60
                        order.kinematicviscositydead = kinematicviscosity.cvt60dead
                if order.temperature == 80:
                    if kinematicviscosity.cvt80dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt80
                        order.kinematicviscositydead = kinematicviscosity.cvt80dead
                if order.temperature == 100:
                    if kinematicviscosity.cvt20dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt100
                        order.kinematicviscositydead = kinematicviscosity.cvt100dead
                if order.temperature == 150:
                    if kinematicviscosity.cvt150dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvt150
                        order.kinematicviscositydead = kinematicviscosity.cvt150dead
                if order.temperature == -20:
                    if kinematicviscosity.cvtminus20dead >= date.today():
                        order.kinematicviscosity = kinematicviscosity.cvtminus20
                        order.kinematicviscositydead = kinematicviscosity.cvtminus20dead
            except:
                pass
            """вставка окончание"""

            order.save()
            return redirect(order)
    else:
        form = StrJournalCreationForm()
    return render(request, URL + '/registrationAtt.html', {'form': form, 'URL': URL})


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
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала. """
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


class PicnometerView(View):
    """ Представление, которое выводит табличку с объёмами пикнометра """
    """ уникальное """

    def get(self, request):
        return render(request, 'dinamicviscosity/picnometer.html')
