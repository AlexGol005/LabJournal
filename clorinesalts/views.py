# все стандратно кроме поиска по полям, импорта моделей и констант
from decimal import Decimal
from PIL import Image
import xlwt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from xlwt import Borders, Alignment

from jouViscosity.models import CvKinematicviscosityVG, CvDensityDinamicVG
from main.models import AttestationJ
from .models import Clorinesalts, CommentsClorinesalts, IndicatorDFK, TitrantHg, GetTitrHg, ClorinesaltsCV, \
    CommentsClorinesaltsCV
from .forms import*

JOURNAL = AttestationJ
MODEL = Clorinesalts
COMMENTMODEL = CommentsClorinesalts
URL = 'clorinesalts'
NAME = 'хлористые соли'
COLONTITUL = 'ИСП_ГОСТ 21534 (метод А)'
from utils_forms import*
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
        form = StrTitrantHgUdateForm()
        return render(request, URL + '/strTitrantHg.html',  {'obj': obj, 'form': form})
    def post(self, request, pk, *args, **kwargs):
        form = StrTitrantHgUdateForm(request.POST, instance=TitrantHg.objects.get(id=pk))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect(order)

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

class AllTitrantHgView(ListView):
    """ Представление, которое выводит все записи о приготовлении титранта. """
    """стандартное"""
    model = TitrantHg
    template_name = URL + '/journalTitrantHg.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super(AllTitrantHgView, self).get_context_data(**kwargs)
        context['URL'] = URL
        return context

class AllTitrantHgTitrView(ListView):
    """ Представление, которое выводит все записи об установке титра. """
    """стандартное"""
    model = GetTitrHg
    template_name = URL + '/journalTitrantHgTitr.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super(AllTitrantHgTitrView, self).get_context_data(**kwargs)
        context['URL'] = URL
        return context


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
        note = JOURNAL.objects.get(for_url=URL)
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
            # a = order.lotHg[-1]
            # try:
                # get_id_actual = GetTitrHg.objects.select_related('lot'). \
                    # filter(lot__exact=a). \
                    # values('lot').annotate(id_actual=Max('id')).values('id_actual')
                # list_ = list(get_id_actual)
                # set = list_[0].get('id_actual')
                # aktualTiter = GetTitrHg.objects.get(id=set)
                # order.titerHg = Decimal(aktualTiter.titr)
                # order.titerHgdead = aktualTiter.datedead
            # except:
                # pass
            # order.dfkdead = IndicatorDFK.objects.last().datedead
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
    """нестандартное"""
    model = ClorinesaltsCV
    template_name = URL + '/journalCV.html'
    context_object_name = 'objects'
    ordering = ['-date']
    paginate_by = 8

    def get_queryset(self, *args, **kwargs):
        qs = super(AllStrCVView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(fixation=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super(AllStrCVView, self).get_context_data(**kwargs)
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

class SearchCVResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала расчёта АЗ. """
    """нестандартное"""

    template_name = URL + '/journalCV.html'

    def get_context_data(self, **kwargs):
        context = super(SearchCVResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        namedop = self.request.GET['namedop']
        lot = self.request.GET['lot']
        if name and lot:
            objects = ClorinesaltsCV.objects.filter(fixation=True).filter(clorinesalts__name=name).filter(clorinesalts__namedop=namedop).filter(clorinesalts__lot=lot).order_by('-pk')
            context['objects'] = objects
        if name and not lot:
            objects = ClorinesaltsCV.objects.filter(fixation=True).filter(clorinesalts__name=name).filter(clorinesalts__namedop=namedop).order_by('-pk')
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


class DateSearchCVResultView(TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми расчётами АЗ. """
    """стандартное"""

    template_name = URL + '/journalCV.html'

    def get_context_data(self, **kwargs):
        context = super(DateSearchCVResultView, self).get_context_data(**kwargs)
        datestart = self.request.GET['datestart']
        datefinish = self.request.GET['datefinish']
        try:
            objects = ClorinesaltsCV.objects.all().filter(fixation=True).filter(date__range=(datestart, datefinish)).order_by('-pk')
            context['objects'] = objects
            context['journal'] = JOURNAL.objects.filter(for_url=URL)
            context['formSM'] = SearchForm()
            context['formdate'] = SearchDateForm(initial={'datestart': datestart, 'datefinish': datefinish})
            context['URL'] = URL
            return context
        except ValidationError:
            objects = ClorinesaltsCV.objects.filter(id=5)
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

def filtercvview(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр для Журнала расчёта АЗ"""
    """Стандартная"""
    journal = JOURNAL.objects.filter(for_url=URL)
    objects = ClorinesaltsCV.objects.all()
    formSM = SearchForm()
    formdate = SearchDateForm()
    if pk == 2:
        now = datetime.now()
        objects = objects.filter(date__gte=now).order_by('-pk')
    elif pk == 5:
        objects = objects.filter(performer=request.user).order_by('-pk')
    return render(request, URL + "/journalCV.html", {'objects': objects, 'journal': journal, 'formSM': formSM, 'URL': URL,
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

class BottlesView(View):
    """ выводит этикетки для растворов """
    """уникальное для титрования"""

    def get(self, request):

        indicatordead = IndicatorDFK.objects.last().datedead
        indicatorbirth = IndicatorDFK.objects.last().date
        indicatormother = IndicatorDFK.objects.last().performer
        titrantbirth = TitrantHg.objects.last().date
        titrantmother = TitrantHg.objects.last().performer
        titrantlot = TitrantHg.objects.last().pk
        context = {
            'indicatordead': indicatordead,
            'indicatorbirth': indicatorbirth,
            'indicatormother': indicatormother,
            'titrantbirth': titrantbirth,
            'titrantmother': titrantmother,
            'titrantlot': titrantlot,
        }

        return render(request, URL + '/bottles.html', context)

# стили для exel
brd1 = Borders()
brd1.left = 1
brd1.right = 1
brd1.top = 1
brd1.bottom = 1

al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_CENTER

style1 = xlwt.XFStyle()
style1.font.bold = True
style1.font.name = 'Calibri'
style1.borders = brd1
style1.alignment = al1
style1.alignment.wrap = 1

style2 = xlwt.XFStyle()
style2.font.name = 'Calibri'
style2.borders = brd1
style2.alignment = al1

style3 = xlwt.XFStyle()
style3.font.name = 'Calibri'
style3.alignment = al1

style4 = xlwt.XFStyle()
style4.font.bold = True
style4.font.name = 'Calibri'
style4.alignment = al1


def export_TitrantHg_xls(request, pk):
    '''представление для выгрузки отдельной странички журнала в ексель - приготовление титранта'''
    note = TitrantHg.objects.get(pk=pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="titrant {note.pk}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('1', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '

    # ширина столбцов
    ws.col(0).width = 6000
    ws.col(1).width = 6000
    ws.col(2).width = 6000

    # высота столбцов
    for i in range(12):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600

    row_num = 0
    columns = [
        f'{COLONTITUL}_{note.date.year}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 3, style3)

    row_num = 2
    columns = [
        'Приготовление 0,01 н. раствора азотнокислой ртути',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(row_num, row_num, 0, 3, style4)


    row_num = 4
    columns = [
        'Реактив',
        'Производство и партия',
        'Количество',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)

    row_num = 5
    columns = [
        'Ртуть (II) азотнокислая 1-водная',
        note.lotreakt1,
        f'{note.massHgNO3} г',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 6
    columns = [
        'Вода дистиллированная',
        note.lotreakt2,
        f'{note.volumeH2O} мл',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 7
    columns = [
        'Кислота азотная 0,2 М',
        note.lotreakt3,
        f'{note.volumeHNO3} мл',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 8
    columns = [
        f'Партия титранта: {note.pk}',
        f'Изготовлен: {note.date} Годен до: Н/О',
        f'Приготовил: {note.performer.username}',

    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)

    wb.save(response)
    return response


def export_GetTitrHg_xls(request, pk):
    '''представление для выгрузки отдельной странички журнала в ексель - установка титра'''
    note = GetTitrHg.objects.get(pk=pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="titr {note.lot.pk}-{note.pk}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('1', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '

    # ширина столбцов
    ws.col(0).width = 6000
    ws.col(1).width = 6000
    ws.col(2).width = 6000

    # высота столбцов
    for i in range(12):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600

    row_num = 0
    columns = [
        f'{COLONTITUL}_{note.date.year}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 2, style3)

    row_num = 2
    columns = [
        f'Установка титра Hg(NO3)2 р-р, п. {note.lot.pk}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(row_num, row_num, 0, 2, style4)

    row_num = 4
    columns = [
       f" {note.date}",
        f'Исп. {note.performer.username}',
        f'Vхол = {note.backvolume} мл',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 5
    columns = [
        f'V1 = {note.volumeHGNO1} мл',
        f'V2 = {note.volumeHGNO2} мл',
        f'V3 = {note.volumeHGNO3} мл',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 6
    columns = [
        f'Т1 = {note.titr1} мг/мл',
        f'Т2 = {note.titr2} мг/мл',
        f'Т3 = {note.titr3} мг/мл',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 7
    columns = [
        f'Расхождение между определениями: Тmax - Tmin = {note.krit}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style2)

    row_num = 8
    columns = [
        f'Удовлетворительно: Tmax - Tmin <=  {note.ndockrit}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style2)

    row_num = 9
    columns = [
        f'Титр Hg(NO3)2 = {note.titr} мг/мл  ',
        f'Титр Hg(NO3)2 = {note.titr} мг/мл  ',
        f'годен до: {note.datedead} ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 1, style1)

    wb.save(response)
    return response

def export_Clorinesalts_xls(request, pk):
    '''представление для выгрузки отдельной странички журнала в ексель - приготовление титранта'''
    note = Clorinesalts.objects.get(pk=pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('1', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '

    # ширина столбцов
    ws.col(0).width = 4000
    ws.col(1).width = 4000
    ws.col(2).width = 4000
    ws.col(3).width = 4000
    ws.col(4).width = 4000
    ws.col(5).width = 4000

    # высота столбцов
    for i in range(25):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600


    row_num = 0
    columns = [
        f'{COLONTITUL}_{note.date.year}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 5, style2)

    row_num = 1
    columns = [
        f'Определение содержания хлористых солей в нефтепродуктах по {note.ndocument}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)

    row_num = 2
    columns = [
        'Дата',
        'Наименование',
        'Партия',
        'Диапазон содержания хлористых солей по методу, мг/л',
        'Расчётное содержание хлористых солей, мг/л',
        'Очерёдность отбора пробы',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num = 3
    columns = [
        f'{note.date}',
        f'{ note.name}({ note.namedop})',
        f'{note.lot}',
        f'{note.constit}',
        f'{note.projectconc}',
        f'{note.que}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num = 4
    columns = [
        'Партия раствора нитрата ртути',
        'Партия раствора нитрата ртути',
        'Титр  нитрата ртути, мг/мл',
        'Титр  нитрата ртути, мг/мл',
        'Титр  нитрата ртути годен до',
        'Титр  нитрата ртути годен до',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 1,  style1)
        ws.merge(row_num, row_num, 2, 3,  style1)
        ws.merge(row_num, row_num, 4, 5,  style1)

    row_num = 5
    columns = [
        f'{note.lotHg}',
        f'{note.lotHg}',
        f'{ note.titerHg}',
        f'{ note.titerHg}',
        f'{note.titerHgdead}',
        f'{note.titerHgdead}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 1, style2)
        ws.merge(row_num, row_num, 2, 3, style2)
        ws.merge(row_num, row_num, 4, 5, style2)

    row_num = 6
    columns = [
        'ДФК индикатор р-р годен до',
        'Растворитель',
        'Объём аликвоты пробы, мл',
        'Объём растворителя',
        'Поведение пробы при экстракции',
        'Объём на титрование холостой пробы, мл',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1200

    row_num = 7
    columns = [
        f'{note.dfkdead}',
        f'{ note.solvent}',
        f'{note.aliquotvolume}',
        f'{note.solventvolume}',
        f'{note.behaviour}',
        f'{note.backvolume}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 8
    columns = [
        f'Титрование экстрактов',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)

    row_num = 9
    columns = [
        f'Воронка № 1',
        f'Воронка № 1',
        f'Воронка № 1',
        f'Воронка № 2',
        f'Воронка № 2',
        f'Воронка № 2',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 5, style1)

    row_num = 10
    columns = [
        ' ',
        'V(Hg(NO3)2), мл	',
        'А',
        ' ',
        'V(Hg(NO3)2), мл	',
        'А',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)

    row_num = 11
    columns = [
        '11 ',
        f'{note.V1E1}',
        f'{note.aV1E1}',
        '21',
        f'{note.V2E1}',
        f'{note.aV2E1}',
    ]
    for col_num in (0, 3):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in (1, 2, 4, 5):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 12
    columns = [
        '12',
        f'{note.V1E2}',
        f'{note.aV1E2}',
        '22',
        f'{note.V2E2}',
        f'{note.aV2E2}',
    ]
    for col_num in (0, 3):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in (1, 2, 4, 5):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 13
    columns = [
        '13',
        f'{note.V1E3}',
        f'{note.aV1E3}',
        '13',
        f'{note.V2E3}',
        f'{note.aV2E3}',
    ]
    for col_num in (0, 3):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in (1, 2, 4, 5):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 14
    columns = [
        '14',
        note.V1E4,
        note.aV1E4,
        '24',
        note.V2E4,
        note.aV2E4,
    ]
    for col_num in (0, 3):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in (1, 2, 4, 5):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 15
    columns = [
        '15',
        note.V1E5,
       note.aV1E5,
        '25',
        note.V2E5,
        note.aV2E5,
    ]
    for col_num in (0, 3):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in (1, 2, 4, 5):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 16
    columns = [
        'X1, мг/л',
        note.x1,
        note.x1,
        'X2, мг/л',
        note.x2,
        note.x2,
    ]
    for col_num in (0, 3):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in (1, 2, 4, 5):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 4, 5, style2)

    row_num = 17
    columns = [
        'Сходимость по ГОСТ, мг/л',
        'Сходимость по ГОСТ, мг/л',
        'Сходимость по ГОСТ, мг/л',
        'Сходимость фактическая, мг/л',
        'Сходимость фактическая, мг/л',
        'Сходимость фактическая, мг/л',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 5, style1)

    row_num = 18
    columns = [
        note.ndocconvergence,
        note.ndocconvergence,
        note.ndocconvergence,
        note.factconvergence,
        note.factconvergence,
        note.factconvergence,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

    row_num = 19
    columns = [
        f'Результат измерений: {note.resultMeas}'

    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)

    row_num = 20
    columns = [
        'Исполнитель',
        'Исполнитель',
        'Исполнитель',
        'ОТК',
        'ОТК',
        'ОТК',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 5, style1)

    row_num = 21
    columns = [
        note.performer.username,
        note.performer.username,
        note.performer.username,
        ' ',
        ' ',
        ' ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)


    wb.save(response)
    return response
