from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import AttestationJ
from .forms import DinamicviscosityUdateForm, CommentCreationForm, DinamicviscosityCreationForm
from .models import Dinamicviscosity, CommentsDinamicviscosity


class DinamicviscosityJournalView(View):
    """ Представление, которое выводит заглавную страницу журнала """

    def get(self, request):
        note = AttestationJ.objects.all().filter(for_url='dinamicviscosity')
        return render(request, 'dinamicviscosity/head.html', {'note': note})


class StrDinamicviscosityView(View):
    """ выводит отдельную запись и форму добавления в ЖАЗ. (актуальная) """

    def get(self, request, pk):
        note = get_object_or_404(Dinamicviscosity, pk=pk)
        form = DinamicviscosityUdateForm()
        return render(request, 'dinamicviscosity/str.html', {'note': note, 'form': form})

    def post(self, request, pk, *args, **kwargs):
        if Dinamicviscosity.objects.get(id=pk).performer == request.user:
            form = DinamicviscosityUdateForm(request.POST, instance=Dinamicviscosity.objects.get(id=pk))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect(order)
        else:
            form = DinamicviscosityUdateForm(request.POST, instance=Dinamicviscosity.objects.get(id=pk))
            order = form.save(commit=False)
            messages.success(request, f'АЗ не подтверждено! Подтвердить АЗ может только исполнитель данного измерения!')
            return redirect(order)


@login_required
def RegDinamicviscosityView(request):
    """ Представление, которое выводит форму регистрации в журнале. """
    if request.method == "POST":
        form = DinamicviscosityCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            return redirect(order)
    else:
        form = DinamicviscosityCreationForm()

    return render(
        request,
        'dinamicviscosity/registration.html',
        {
            'form': form
        })



class CommentsKinematicviscosityView(View):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    form_class = CommentCreationForm
    initial = {'key': 'value'}
    template_name = 'dinamicviscosity/comments.html'

    def get(self, request, pk):
        note = CommentsDinamicviscosity.objects.filter(forNote=pk)
        title = Dinamicviscosity.objects.get(pk=pk)
        form = CommentCreationForm()
        return render(request, 'dinamicviscosity/comments.html', {'note': note, 'title': title, 'form': form})

    def post(self, request, pk, *args, **kwargs):
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.author = request.user
            order.forNote = Dinamicviscosity.objects.get(pk=pk)
            order.save()
            messages.success(request, f'Комментарий добавлен!')
            return redirect(order)


class AllDinamicviscosityView(ListView):
    """ Представление, которое выводит все записи в журнале. """
    model = Dinamicviscosity
    template_name = 'dinamicviscosity/journal.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8


def Dinamicviscosityobjects_filter(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр
    """
    objects = Dinamicviscosity.objects.all()
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
    return render(request, "dinamicviscosity/journal.html", {'objects': objects})

