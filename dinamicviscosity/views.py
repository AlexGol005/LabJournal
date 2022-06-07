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
from .models import Dinamicviscosity


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
                # form.save()
                messages.success(request, f'АЗ успешно подтверждено!')
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


class DinamicviscosityJournalView(View):
    """ Представление, которое выводит заглавную страницу журнала """

    def get(self, request):
        note = AttestationJ.objects.all().filter(for_url='dinamicviscosity')
        return render(request, 'dinamicviscosity/head.html', {'note': note})


# class CommentsKinematicviscosityView(View):
#     """ выводит комментарии к записи в журнале и форму для добавления комментариев """
#     form_class = CommentCreationForm
#     initial = {'key': 'value'}
#     template_name = 'kinematicviscosity/comments.html'
#
#     def get(self, request, pk):
#         note = CommentsKinematicviscosity.objects.filter(forNote=pk)
#         title = ViscosityMJL.objects.get(pk=pk)
#         form = CommentCreationForm()
#         return render(request, 'kinematicviscosity/comments.html', {'note': note, 'title': title, 'form': form})
#
#     def post(self, request, pk, *args, **kwargs):
#         form = CommentCreationForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.author = request.user
#             order.forNote = ViscosityMJL.objects.get(pk=pk)
#             order.save()
#             messages.success(request, f'Комментарий добавлен!')
#             return redirect(order)
#
#
class AllDinamicviscosityView(ListView):
    """ Представление, которое выводит все записи в журнале. """
    model = Dinamicviscosity
    template_name = 'dinamicviscosity/journal.html'
    context_object_name = 'dinamicviscosityobjects'
    ordering = ['-date']
    paginate_by = 8
#
#
# def viscosityobjects_filter(request, pk):
#     """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр
#     """
#     viscosityobjects = ViscosityMJL.objects.all()
#     if pk == 1:
#         now = datetime.now() - timedelta(minutes=60 * 24 * 7)
#         viscosityobjects = viscosityobjects.filter(date__gte=now).order_by('-pk')
#     elif pk == 2:
#         now = datetime.now()
#         viscosityobjects = viscosityobjects.filter(date__gte=now).order_by('-pk')
#     elif pk == 3:
#         viscosityobjects = viscosityobjects.order_by('-pk')
#     elif pk == 4:
#         viscosityobjects = viscosityobjects.filter(fixation__exact=True).order_by('-pk')
#     elif pk == 5:
#         viscosityobjects = viscosityobjects.filter(performer=request.user).order_by('-pk')
#     elif pk == 6:
#         viscosityobjects = viscosityobjects.filter(performer=request.user).filter(fixation__exact=True).order_by('-pk')
#     elif pk == 7:
#         viscosityobjects = viscosityobjects.filter(performer=request.user).filter(fixation__exact=True).filter(
#             date__gte=datetime.now()).order_by('-pk')
#
#     return render(request, "kinematicviscosity/journal.html", {'viscosityobjects': viscosityobjects})
#
#
# from django.shortcuts import render
#
# # Create your views here.
