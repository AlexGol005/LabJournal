# все стандратно кроме поиска по полям, импорта моделей и констант
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from jouViscosity.models import CvKinematicviscosityVG, CvDensityDinamicVG
from main.models import AttestationJ
from .models import Clorinesalts, CommentsClorinesalts, IndicatorDFK, TitrantHg, GetTitrHg, ClorinesaltsCV, \
    CommentsClorinesaltsCV
from .forms import DPKForm, TitrantHgForm, GetTitrHgForm, StrJournalUdateForm, SearchForm, SearchDateForm, \
    CommentCreationForm, StrJournalCreationForm, ClorinesaltsCVUpdateForm, ClorinesaltsCVUpdateFixationForm, \
    CommentCVCreationForm

JOURNAL = AttestationJ
MODEL = Clorinesalts
COMMENTMODEL = CommentsClorinesalts
URL = 'clorinesalts'
NAME = 'хлористые соли'


class StrDPKView(View):
    """ выводит отдельную запись об изготовлении индикатора """
    """уникальное для титрования"""

    def get(self, request, pk):
        obj = get_object_or_404(IndicatorDFK, pk=pk)
        return render(request, URL + '/strDPK.html',  {'obj': obj})

@login_required
def RegDPKView(request):
    """ выводит форму регистрации индикатора в журнале. """
    """уникальное для титрования"""
    if request.method == "POST":
        form = DPKForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            return redirect(order)
    else:
        form = DPKForm()
    return render(request, URL + '/registrationDPK.html', {'form': form, 'URL': URL})


class StrTitrantHgView(View):
    """ выводит отдельную запись приготовлении титранта """
    """уникальное для титрования"""

    def get(self, request, pk):
        obj = get_object_or_404(TitrantHg, pk=pk)
        return render(request, URL + '/strTitrantHg.html',  {'obj': obj})

@login_required
def RegTitrantHgView(request):
    """ выводит форму регистрации приготовления титранта в журнале. """
    """уникальное для титрования"""
    if request.method == "POST":
        form = TitrantHgForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            return redirect(order)
    else:
        form = TitrantHgForm()
    return render(request, URL + '/registrationTitrantHg.html', {'form': form, 'URL': URL})


class StrGetTitrHgView(View):
    """ выводит отдельную запись установки титра """
    """уникальное для титрования"""

    def get(self, request, pk):
        obj = get_object_or_404(GetTitrHg, pk=pk)
        return render(request, URL + '/strGetTitrHg.html',  {'obj': obj})

@login_required
def GetTitrHgView(request):
    """ выводит форму регистрации установки титра """
    """уникальное для титрования"""
    if request.method == "POST":
        form = GetTitrHgForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            return redirect(order)
    else:
        form = GetTitrHgForm()
    return render(request, URL + '/registrationGetTitrHg.html', {'form': form, 'URL': URL})



# далее идут стандартные представления

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
        form = StrJournalUdateForm(request.POST, instance=MODEL.objects.get(id=pk))
        if MODEL.objects.get(id=pk).performer == request.user:
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

    if request.method == "POST":
        form = StrJournalCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            a = order.lotHg[-1]
            try:
                get_id_actual = GetTitrHg.objects.select_related('lot'). \
                    filter(lot__exact=a). \
                    values('lot').annotate(id_actual=Max('id')).values('id_actual')
                list_ = list(get_id_actual)
                set = list_[0].get('id_actual')
                aktualTiter = GetTitrHg.objects.get(id=set)
                order.titerHg = Decimal(aktualTiter.titr)
                order.titerHgdead = aktualTiter.datedead
            except:
                pass
            order.dfkdead = IndicatorDFK.objects.last().datedead
            order.save()
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

class AllStrCVView(ListView):
    """ Представление, которое выводит все записи в журнале расчёта АЗ. """
    """стандартное"""
    model = ClorinesaltsCV
    template_name = URL + '/journalCV.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super(AllStrCVView, self).get_context_data(**kwargs)
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        # context['formSM'] = SearchForm()
        # context['formdate'] = SearchDateForm()
        context['URL'] = URL
        return context

class SearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала. """
    """нестандартное"""

    template_name = URL + '/journal.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        namedop = self.request.GET['namedop']
        lot = self.request.GET['lot']
        if name and lot:
            objects = MODEL.objects.filter(name=name).filter(namedop=namedop).filter(lot=lot).order_by('-pk')
            context['objects'] = objects
        if name and not lot:
            objects = MODEL.objects.filter(name=name).filter(namedop=namedop).order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm(initial={'name': name, 'namedop': namedop,'lot': lot})
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


class VolumecsView(View):
    """ Представление, которое выводит табличку с объёмами аликвоты и растворителя """
    """ уникальное """

    def get(self, request):
        return render(request, 'clorinesalts/volume.html')

class ClorinesaltsCVView(View):
    """ выводит отдельную запись расчёта АЗ и форму для её обновления """

    def get(self, request, pk):
        note = get_object_or_404(ClorinesaltsCV, pk=pk)
        form = ClorinesaltsCVUpdateForm()
        form2 = ClorinesaltsCVUpdateFixationForm()
        try:
            counter = CommentsClorinesaltsCV.objects.filter(forNote=note.id)
        except ObjectDoesNotExist:
            counter = None
        return render(request, URL + '/strCV.html',
                      {'note': note, 'form': form, 'form2': form2, 'URL': URL, 'counter': counter})
    def post(self, request, pk, *args, **kwargs):
        form = ClorinesaltsCVUpdateForm(request.POST, instance=ClorinesaltsCV.objects.get(id=pk))
        form2 = ClorinesaltsCVUpdateFixationForm(request.POST, instance=ClorinesaltsCV.objects.get(id=pk))
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            return redirect(order)
        if form2.is_valid():
            order2 = form2.save(commit=False)
            order2.save()
            return redirect(f'/attestationJ/clorinesalts/clorinesaltsstrcv/{pk}/')

class CommentsCVView(View):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """

    form_class = CommentCVCreationForm
    initial = {'key': 'value'}
    template_name = URL + '/comments.html'

    def get(self, request, pk):
        note = CommentsClorinesaltsCV.objects.filter(forNote=pk)
        form = CommentCVCreationForm()
        # title = ClorinesaltsCV.objects.get(pk=pk)
        return render(request, 'main/comments.html', {'note': note, 'form': form, 'URL': URL})

    def post(self, request, pk, *args, **kwargs):
        form = CommentCVCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.forNote = ClorinesaltsCV.objects.get(pk=pk)
            order.save()
            messages.success(request, f'Комментарий добавлен!')
            return redirect(order)

