from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView, TemplateView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from main.models import AttestationJ
from .models import ViscosityMJL, CommentsKinematicviscosity
from .forms import StrJournalCreationForm, StrJournalUdateForm, CommentCreationForm, AdvancedSearchForm

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
        return render(request, URL + '/head.html', {'note': note})


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
    """Стандартное"""
    if request.method == "POST":
        form = StrJournalCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            return redirect(order)
    else:
        form = StrJournalCreationForm()
    return render(request, URL + '/registration.html', {'form': form})


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
        context['form'] = AdvancedSearchForm()
        return context




def filterview(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр """
    """Стандартная"""
    journal = JOURNAL.objects.filter(for_url=URL)
    objects = MODEL.objects.all()
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
    return render(request, URL + "/journal.html", {'objects': objects, 'journal': journal})

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
class AdvancedSearchView(FormView):
    form_class = AdvancedSearchForm
    template_name = "kinematicviscosity/test.html"
    success_url = '/search_location/result/'

# url of this view is 'search_result'
class SearchResultView(TemplateView):
    template_name = "kinematicviscosity/testresult.html"

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        location = self.request.GET['name']
        location = location.upper()
        keywords = self.request.GET['lot']
        # how should I use keywords (string of words split by commas)
        # in order to get locations_searched by name and keywords simultaneously
        locations_searched = MODEL.objects.filter(name=location)
        context['locations_searched'] = locations_searched
        return context