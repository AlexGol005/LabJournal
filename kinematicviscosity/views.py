# все стандратно кроме поиска по полям, импорта моделей и констант
import os
from wsgiref.util import FileWrapper

import xlwt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sqlparse.filters import output
from xlwt import Borders, Alignment

from jouViscosity.models import CvKinematicviscosityVG
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
    """Стандартное, но со вставкой по поводу констант и предыдущего значения"""
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
            try:
                oldvalue = CvKinematicviscosityVG.objects.get(namelot__nameVG__name=order.name, namelot__lot=order.lot)
                if order.temperature == 20:
                    order.oldCertifiedValue = oldvalue.cvt20

                if order.temperature == 25:
                    order.oldCertifiedValue = oldvalue.cvt25

                if order.temperature == 40:
                    order.oldCertifiedValue = oldvalue.cvt40

                if order.temperature == 50:
                    order.oldCertifiedValue = oldvalue.cvt50

                if order.temperature == 60:
                    order.oldCertifiedValue = oldvalue.cvt60

                if order.temperature == 80:
                    order.oldCertifiedValue = oldvalue.cvt80

                if order.temperature == 100:
                    order.oldCertifiedValue = oldvalue.cvt100

                if order.temperature == 150:
                    order.oldCertifiedValue = oldvalue.cvt150

                if order.temperature == -20:
                    order.oldCertifiedValue = oldvalue.cvtminus20
            except ObjectDoesNotExist:
                pass
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
# --------------------------------
def export_me_xls(request, pk):
    '''представление для выгрузки отдельной странички  в ексель'''
    note = ViscosityMJL.objects.get(pk=pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}.xls"'


    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{note.name}, п. {note.lot},{note.temperature}', cell_overwrite_ok=True)


    for i in range(21):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600

    ws.row(21).height_mismatch = True
    ws.row(21).height = 800

    for i in range(22, 25):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600



    # ширина столбцов
    ws.col(0).width = 4100
    ws.col(1).width = 4100
    ws.col(2).width = 4100
    ws.col(5).width = 4100



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
    style3.borders = brd1
    style3.alignment = al1
    style3.num_format_str = 'DD.MM.YYYY'

    style4 = xlwt.XFStyle()
    style4.font.name = 'Calibri'
    style4.borders = brd1
    style4.alignment = al1
    style4.num_format_str = '0.00'

    style5 = xlwt.XFStyle()
    style5.font.name = 'Calibri'
    style5.borders = brd1
    style5.alignment = al1
    style5.num_format_str = '0.00000'

    row_num = 0
    columns = [
                 f'Атт.-ВЖ-(МИ № 02-2018)-{note.date}'
               ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(0, 0, 0, 5, style1)

    row_num = 1
    columns = [
        f'Определение кинематической вязкости, метод: { note.ndocument }'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(1, 1, 0, 5, style1)

    row_num = 2
    columns = [
        'Дата измерения',
        'Наименование',
        'Номер партии',
        'Т °C',
        'Термост. 20 мин',
        'Сод. нефть или октол',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)

    row_num = 3
    columns = [
        note.date,
        note.name,
        note.lot,
        note.temperature,
        'V',
        note.constit,
    ]
    for col_num in range(1, 4):
        ws.write(row_num, col_num, columns[col_num], style2)
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style3)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)

    row_num = 4
    columns = [
        'Проведение измерений'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(4, 4, 0, 5, style1)

    row_num = 5
    columns = [
        '№ виск-ра',
        str(note.ViscosimeterNumber1),
        str(note.ViscosimeterNumber1),
        str(note.ViscosimeterNumber2),
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(5, 5, 1, 2, style2)
        ws.merge(5, 5, 3, 5, style2)

    row_num = 6
    columns = [
        'Константа вискозиметра, мм2/с2',
        'К1',
        'К1',
        'К2',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(6, 7, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(6, 6, 1, 2, style2)
        ws.merge(6, 6, 3, 5, style2)

    row_num = 7
    columns = [
        'Константа вискозиметра, мм2/с2',
        note.Konstant1,
        note.Konstant1,
        note.Konstant2,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(7, 7, 1, 2, style2)
        ws.merge(7, 7, 3, 5, style2)

    row_num = 8
    columns = [
        'Время истечения 1, τ1',
        'τ11, минут',
        'τ11, секунд',
        'τ21, минут',
        'τ21, минут',
        'τ21, секунд',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(8, 9, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(8, 8, 3, 4, style1)

    row_num = 9
    columns = [
        'Время истечения 1, τ1',
        f'{note.plustimeminK1T1}:{ note.plustimesekK1T1}',
        note.timeK1T1_sec,
        f'{note.plustimeminK2T1}:{ note.plustimesekK2T1}',
        f'{note.plustimeminK2T1}:{ note.plustimesekK2T1}',
        note.timeK2T1_sec,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(9, 9, 3, 4, style4)

    row_num = 10
    columns = [
        'Время истечения 2, τ2',
        'τ21, минут',
        'τ21, секунд',
        'τ22, минут',
        'τ22, минут',
        'τ22, секунд',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(10, 11, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(10, 10, 3, 4, style1)

    row_num = 11
    columns = [
        'Время истечения 2, τ2',
        f'{note.plustimeminK1T2}:{note.plustimesekK1T2}',
        note.timeK1T2_sec,
        f'{note.plustimeminK2T2}:{note.plustimesekK2T2}',
        f'{note.plustimeminK2T2}:{note.plustimesekK2T2}',
        note.timeK2T2_sec,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(11, 11, 3, 4, style4)

    row_num = 12
    columns = [
        'Время истечения среднее',
        'τ1',
        'τ2',
        'τ2',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(12, 13, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(12, 12, 1, 2, style2)
        ws.merge(12, 12, 3, 5, style2)

    row_num = 13
    columns = [
        'Время истечения среднее',
         note.timeK1_avg,
         note.timeK2_avg,
         note.timeK2_avg,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(13, 13, 1, 2, style4)
        ws.merge(13, 13, 3, 5, style4)

    row_num = 14
    columns = [
        'Вязкость кинематическая  νi= Кi * τi',
        'ν1, мм2/с',
        'ν2, мм2/с',
        'ν2, мм2/с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(14, 15, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(14, 14, 1, 2, style2)
        ws.merge(14, 14, 3, 5, style2)

    row_num = 15
    columns = [
        'Вязкость кинематическая  νi= Кi * τi',
        note.viscosity1,
        note.viscosity2,
        note.viscosity2,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(15, 15, 1, 2, style5)
        ws.merge(15, 15, 3, 5, style5)

    row_num = 16
    columns = [
        'Обработка результатов'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(16, 16, 0, 5, style1)

    row_num = 17
    columns = [
        'νсред = (ν1 + ν2)/2',
        'νсред = (ν1 + ν2)/2',
        'Оценка приемл. изм. Δ = (|ν1 - ν2|)/νсред) * 100%',
        'Оценка приемл. изм. Δ = (|ν1 - ν2|)/νсред) * 100%',
        'Критерий приемлемости измерений, r',
        'Критерий приемлемости измерений, r',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(17, 17, 0, 1, style1)
        ws.merge(17, 17, 2, 3, style1)
        ws.merge(17, 17, 4, 5, style1)

    row_num = 18
    columns = [
        note.viscosityAVG,
        note.viscosityAVG,
        note.accMeasurement,
        note.accMeasurement,
        note.kriteriy,
        note.kriteriy,
    ]
    for col_num in range(0, 2):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(18, 18, 0, 1, style5)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(18, 18, 2, 3, style2)
        ws.merge(18, 18, 4, 5, style2)

    row_num = 19
    columns = [
        f'Результат измерений: {note.resultMeas}'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(19, 19, 0, 5, style1)

    row_num = 20
    columns = [
       ' Фиксация результатов'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(20, 20, 0, 5, style1)

    row_num = 21
    columns = [
        'АЗ, мм2/с',
        'Абс. погр. (νсред * 0,3)/100',
        'Пред. знач. вязкости, νпред, мм2/с ',
        'Разница с νпред, %',
        'Разница с νпред, %',
        'Разница с νпред, %',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(21, 21, 3, 5, style1)

    row_num = 22
    columns = [
        note.certifiedValue_text,
        note.abserror,
        note.oldCertifiedValue,
        note.deltaOldCertifiedValue,
        note.deltaOldCertifiedValue,
        note.deltaOldCertifiedValue,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(22, 22, 3, 5, style2)

    row_num = 23
    columns = [
        'Исполнитель',
        'отпр.',
        'внесено',
        'ОТК',
        'ОТК',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(23, 23, 3, 5, style1)

    row_num = 24
    columns = [
        str(note.performer),
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(24, 24, 3, 5, style2)
    # response = HttpResponse('C:\\Users\\АлександраГоловкина\\Петроаналитика\\Петроаналитика - Производство и склад\\Личные папки сотрудников\\Саша Головкина\\', )
    wb.save(response)
    return response


