# все стандратно кроме поиска по полям, импорта моделей и констант
from PIL import Image
import xlwt
from django.db.models import Value
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models.functions import Concat
from xlwt import Borders, Alignment

# этот блок нужен для всех журналов
from equipment.models import CompanyCard
from metods import *
from .forms import *
from utils_forms import*
from .models import *

from .j_constants import *
from utils import *
from textconstants import *
from .constvisc import *
from protokol_exel import *
MODEL = ViscosityMJL
COMMENTMODEL = Comments


class Constants:
    URL = URL
    JOURNAL = JOURNAL
    MODEL = MODEL
    COMMENTMODEL = COMMENTMODEL
    NAME = NAME
    journal = journal
    SearchForm = SearchForm
    SearchSeriaForm = SearchSeriaForm
    SearchDateForm = SearchDateForm
# конец блока для всех журналов

def export_protocol_xls_template_1(request, pk):
    num = pk
    response = export_protocol_xls_template(num, MATERIAL1, MODEL, constitoptional, aimoptional, conclusionoptional, attcharacteristic)
    return response

def SeriaUpdate(request, str):
    """выводит страницу с формой для обновления номера серии измерений""" 
    title = f'{ViscosityMJL.objects.get(pk=str).name}, п. {ViscosityMJL.objects.get(pk=str).lot}'
    if request.method == "POST":
        form = SeriaUpdateForm(request.POST, request.FILES,  instance=ViscosityMJL.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect(f'/attestationJ/kinematicviscosity/attestation/{str}/')  
    else:
        form = SeriaUpdateForm(instance=ViscosityMJL.objects.get(pk=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/reg.html', data)


# блок стандартных 'View' но с индивидуальностями,  возможно унаследованных от стандартных классов из модуля utils


class RegView(RegView):
    """ Представление, которое выводит форму регистрации в журнале. """
    """ метод форм валид перегружен для заполнения полей """
    template_name = URL + '/registration.html'
    form_class = StrJournalCreationForm
    success_message = "Запись внесена, подтвердите АЗ!"

    def form_valid(self, form):
        order = form.save(commit=False)
        """вставка начало"""
        get_id_actualconstant1 = Kalibration.objects.select_related('id_Viscosimeter'). \
            filter(id_Viscosimeter__exact=order.ViscosimeterNumber1). \
            values('id_Viscosimeter').annotate(id_actualkonstant=Max('id')).values('id_actualkonstant')
        list1_ = list(get_id_actualconstant1)
        set1 = list1_[0].get('id_actualkonstant')
        aktualkalibration1 = Kalibration.objects.get(id=set1)
        try:
            get_id_actualconstant2 = Kalibration.objects.select_related('id_Viscosimeter'). \
                filter(id_Viscosimeter__exact=order.ViscosimeterNumber2). \
                values('id_Viscosimeter').annotate(id_actualkonstant=Max('id')).values('id_actualkonstant')
            list2_ = list(get_id_actualconstant2)
            set2 = list2_[0].get('id_actualkonstant')
            aktualkalibration2 = Kalibration.objects.get(id=set2)
            order.Konstant2 = aktualkalibration2.konstant
        except:
            order.ViscosimeterNumber2.id = 10
        order.Konstant1 = aktualkalibration1.konstant
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
        return super().form_valid(form)
# конец блока стандартных 'View' но с индивидуальностями

# блок стандартных 'View' унаследованных от стандартных классов из модуля utils
# основные


class HeadView(Constants, HeadView):
    """ Представление, которое выводит заглавную страницу журнала """
    """ Стандартное """
    template_name = URL + '/head.html'


class StrJournalView(Constants, StrJournalView):
    """ выводит отдельную запись и форму добавления в ЖАЗ """
    form_class = StrJournalUdateForm
    template_name = URL + '/str.html'


class CommentsView(Constants, CommentsView):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    """Стандартное"""
    form_class = CommentCreationForm


class AllStrView(Constants, AllStrView):
    """ Представление, которое выводит все записи в журнале. """
    """стандартное"""
    template_name = URL + '/journal.html'
    model = MODEL


# блок View для формирования протокола
class RoomsUpdateView(Constants, RoomsUpdateView):
    """ выводит форму добавления помещения к измерению """
    form_class = StrJournalProtocolRoomUdateForm
    template_name = 'main/reg.html'
    success_message = "Помещение успешно добавлено"


class ProtocolbuttonView(Constants, ProtocolbuttonView):
    """ Выводит кнопку для формирования протокола """
    template_name = URL + '/buttonprotocol.html'


class ProtocolHeadView(Constants, ProtocolHeadView):
    """ выводит форму внесения для внесения допинформации для формирования протокола и кнопку для протокола """
    template_name = 'main/reg.html'
    form_class = StrJournalProtocolUdateForm


# блок  'View' для различных поисков - унаследованные
class DateSearchResultView(Constants, DateSearchResultView):
    """ Представление, которое выводит результаты поиска по датам на странице со всеми записями журнала. """
    """стандартное"""
    template_name = URL + '/journal.html'


# блок  'View' для различных поисков - НЕунаследованные
class SearchResultView(Constants, TemplateView):
    """ Представление, которое выводит результаты поиска на странице со всеми записями журнала. """
    """нестандартное"""
    template_name = URL + '/journal.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        lot = self.request.GET['lot']
        temperature = self.request.GET['temperature']
        if name and lot and temperature:
            objects = MODEL.objects.filter(name=name).filter(lot=lot).filter(temperature=temperature).order_by('-pk')
                
            context['objects'] = objects
        if name and lot and not temperature:
            objects = MODEL.objects.filter(name=name).filter(lot=lot).order_by('-pk')
            context['objects'] = objects
        if name and not lot and not temperature:
            objects = MODEL.objects.filter(name=name).order_by('-pk')
            context['objects'] = objects
        if name and temperature and not lot:
            objects = MODEL.objects.filter(name=name).filter(temperature=temperature).\
                order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm(initial={'name': name, 'lot': lot, 'temperature': temperature})
        context['formdate'] = SearchDateForm()
        context['formS'] = SearchSeriaForm()
        context['URL'] = URL
        return context

class SearchResultSeriaView(Constants, TemplateView):
    """ Представление, которое выводит результаты поиска по серии """
    """нестандартное"""
    template_name = URL + '/journal.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultSeriaView, self).get_context_data(**kwargs)
        seria = self.request.GET['seria']
        if seria:
            objects = MODEL.objects.filter(seria=seria).\
            order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm()
        context['formS'] = SearchSeriaForm()
        context['formdate'] = SearchDateForm()
        context['URL'] = URL
        return context


def filterview(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр """
    """Стандартная"""
    journal = JOURNAL.objects.filter(for_url=URL)
    objects = MODEL.objects.all()
    formSM = SearchForm()
    formS = SearchSeriaForm()
    formdate = SearchDateForm()
    
    if pk == 1:
        now = datetime.datetime.now() - timedelta(minutes=60 * 24 * 7)
        objects = objects.filter(date__gte=now).order_by('-pk')
    elif pk == 2:
        now = datetime.datetime.now()
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
    return render(request, URL + "/journal.html", {'objects': objects, 'journal': journal, 'formSM': formSM, 'URL': URL, 'formS': formS,
                                                   'formdate': formdate})


# блок выгрузок данных в формате ексель (не унаследованные)
# вспомогательная общая информация
b1 = Borders()
b1.left = 1
b1.right = 1
b1.top = 1
b1.bottom = 1

b2 = Borders()
b2.left = 6
b2.right = 6
b2.bottom = 6
b2.top = 6

al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_CENTER

al2 = Alignment()
al2.horz = Alignment.HORZ_RIGHT
al2.vert = Alignment.VERT_CENTER

al3 = Alignment()
al3.horz = Alignment.HORZ_LEFT
al3.vert = Alignment.VERT_CENTER


def export_me_xls(request, pk):
    """представление для выгрузки отдельной странички журнала в ексель"""
    note = MODEL.objects.get(pk=pk)
    try:
        comment = Comments.objects.filter(forNote=note.pk)    
        comment = comment.first().name
    except:
        comment = ''
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    nn = str(note.name)[:10]
    nl = str(note.lot)[:3]
    ws = wb.add_sheet(f'{nn}, п. {nl},{note.temperature}', cell_overwrite_ok=True)
    ws.header_str = b''
    ws.footer_str = b''

    # высота строк
    for i in range(0, 21):
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

    # стили
    style1 = xlwt.XFStyle()
    style1.font.bold = True
    style1.font.name = 'Times New Roman'
    style1.borders = b1
    style1.alignment = al1
    style1.alignment.wrap = 1

    style2 = xlwt.XFStyle()
    style2.font.name = 'Times New Roman'
    style2.borders = b1
    style2.alignment = al1

    style3 = xlwt.XFStyle()
    style3.font.name = 'Times New Roman'
    style3.borders = b1
    style3.alignment = al1
    style3.num_format_str = 'DD.MM.YYYY'

    style4 = xlwt.XFStyle()
    style4.font.name = 'Times New Roman'
    style4.borders = b1
    style4.alignment = al1
    style4.num_format_str = '0.00'

    style5 = xlwt.XFStyle()
    style5.font.name = 'Times New Roman'
    style5.borders = b1
    style5.alignment = al1
    style5.num_format_str = '0.00000'

    style6 = xlwt.XFStyle()
    style6.font.name = 'Times New Roman'
    style6.alignment = al1

    style7 = xlwt.XFStyle()
    style7.font.name = 'Times New Roman'
    style7.alignment = al2



    row_num = 0
    columns = [
                 f'{AttestationJ.objects.get(id=1).name}___{note.date.year}'
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 5, style6)

    row_num = 2
    columns = [
        'Дата измерения',
        'Индекс СО',
        'Номер внутренней партии',
        'Т, °C',
        '№ флакона',
        'Сод. нефть или октол',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 800

    row_num = 3
    columns = [
        note.date,
        note.name,
        note.lot,
        note.temperature,
        note.numberexample,
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
        'Проведение испытаний'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 300

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
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

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
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

    row_num = 7
    columns = [
        'Константа вискозиметра, мм2/с2',
        note.Konstant1,
        note.Konstant1,
        note.Konstant2,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

    row_num = 8
    columns = [
        'Время истечения 1',
        'τ11, мин',
        'τ11, с',
        'τ21, мин',
        'τ21, мин',
        'τ21, с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, 9, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 3, 4, style1)

    row_num = 9
    columns = [
        'Время истечения 1',
        f'{note.plustimeminK1T1}:{ note.plustimesekK1T1}',
        note.timeK1T1_sec,
        f'{note.plustimeminK2T1}:{ note.plustimesekK2T1}',
        f'{note.plustimeminK2T1}:{ note.plustimesekK2T1}',
        note.timeK2T1_sec,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(row_num, row_num, 3, 4, style4)

    row_num = 10
    columns = [
        'Время истечения 2',
        'τ12, мин',
        'τ12, с',
        'τ22, мин',
        'τ22, мин',
        'τ22, с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, 11, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 3, 4, style1)

    am21 = f'{note.plustimeminK1T2}:{note.plustimesekK1T2}'
    as21 = note.timeK1T2_sec
    am22 = f'{note.plustimeminK2T2}:{note.plustimesekK2T2}'
    as22 = note.timeK1T2_sec

    if not note.plustimeminK1T2 and not note.plustimesekK1T2:
        am21 = '-'
        as21 = '-'
    if not note.plustimeminK2T2 and not note.plustimesekK2T2:
        am22 = '-'
        as22 = '-'

    row_num = 11
    columns = [
        'Время истечения 2',
        am21,
        as21,
        am22,
        am22,
        as22,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(row_num, row_num, 3, 4, style4)

    row_num = 12
    columns = [
        'Время истечения среднее',
        'τ1(сред.), c',
        'τ2(сред.), c',
        'τ2(сред.), c',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(12, 13, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

    row_num = 13
    columns = [
        'Время истечения среднее',
         note.timeK1_avg,
         note.timeK2_avg,
         note.timeK2_avg
    ]

    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(row_num, row_num, 1, 2, style4)
        ws.merge(row_num, row_num, 3, 5, style4)

    row_num = 14
    columns = [
        'Вязкость кинематическая  νi= Кi * τi',
        'ν1, мм2/с',
        'ν2, мм2/с',
        'ν2, мм2/с',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, 15, 0, 0, style1)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

    row_num = 15
    columns = [
        'Вязкость кинематическая  νi= Кi * τi',
        note.viscosity1,
        note.viscosity2,
        note.viscosity2,
    ]
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 1, 2, style5)
        ws.merge(row_num, row_num, 3, 5, style5)

    row_num = 16
    columns = [
        'Обработка результатов'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 300

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
        ws.merge(row_num, row_num, 0, 1, style1)
        ws.merge(row_num, row_num, 2, 3, style1)
        ws.merge(row_num, row_num, 4, 5, style1)

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
        ws.merge(row_num, row_num, 0, 1, style5)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 2, 3, style2)
        ws.merge(row_num, row_num, 4, 5, style2)

    row_num = 19
    columns = [
        f'{note.aim}; {note.resultMeas}; {comment}'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 600

    row_num = 20
    columns = [
       ' Результат испытаний'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 5, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 300

    row_num = 21
    columns = [
        'АЗ, мм2/с',
        'Абс. погр. (νсред * 0,3)/100',
        'Пред. знач. вязкости, νпред, мм2/с ',
        'Разница с νпред, %',
        'Отличие АЗ <= 0,7%',
        'Отличие АЗ <= 0,7%',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 4, 5, style1)


    note.certifiedValue_text = str(note.certifiedValue_text).replace('.', ',')
    note.abserror = str(note.abserror).replace('.', ',')
    note.oldCertifiedValue = str(note.oldCertifiedValue).replace('.', ',')

    if not note.deltaOldCertifiedValue:
        note.deltaOldCertifiedValue = '-'
        note.oldCertifiedValue = '-'
        note.resultWarning = '-'
    if note.resultWarning == '' and not note.oldCertifiedValue:
        note.resultWarning = '-'
    if note.resultWarning == '' and note.oldCertifiedValue:
        note.resultWarning = 'да'
    if note.resultWarning == '' and not note.oldCertifiedValue:
        note.resultWarning = 'нет'

    row_num = 22
    columns = [
        note.certifiedValue_text,
        note.abserror,
        note.oldCertifiedValue,
        note.deltaOldCertifiedValue,
        note.resultWarning,
        note.resultWarning,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 4, 5, style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1100

    row_num = 23
    columns = [
        'Исполнитель',
        'Исполнитель.',
        'Исполнитель',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 5, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 300
        

    row_num = 24
    columns = [
        str(note.performer),
        str(note.performer),
        str(note.performer),
        note.seria,
        note.seria,
        note.seria,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style2)
        ws.merge(row_num, row_num, 3, 5, style2)

    


    row_num = 27
    columns = [
        'Страница №           ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 0, 5, style7)

    wb.save(response)
    return response

# флажок протокол
def export_protocol_xls(request, pk):
    """представление для выгрузки протокола испытаний в ексель"""
    company = CompanyCard.objects.get(pk=1)
    note = ViscosityMJL.objects.\
        annotate(name_rm=Concat(Value('СО '), 'name', Value(' , партия '), 'lot')).\
        annotate(performer_rm=Concat('performer__profile__userposition', Value(' '), 'performer__username')). \
        annotate(equipment_set=Concat('equipment1__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(' , зав. № '), 'equipment1__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        )). \
        annotate(equipment_set1=Concat('equipment2__charakters__name',                                        
                                        Value(' тип '), 'equipment2__charakters__typename',
                                        Value(' , зав. № '), 'equipment2__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment2__newcertnumber',
                                        Value(' от '), 'equipment2__newdate',
                                        Value(' действительно до '), 'equipment2__newdatedead',
                                        )). \
        annotate(equipment_set2=Concat('equipment3__charakters__name',
                                       Value(' тип '), 'equipment3__charakters__typename',
                                       Value(' , зав. № '), 'equipment3__equipment__lot',
                                       Value(', свидетельство о поверке № '), 'equipment3__newcertnumber',
                                       Value(' от '), 'equipment3__newdate',
                                       Value(' действительно до '), 'equipment3__newdatedead',
                                       Value('; \n'),
                                       )). \
        annotate(equipment_set3=Concat('equipment4__charakters__name',
                                       Value(' тип '), 'equipment4__charakters__typename',
                                       Value(' , зав. № '), 'equipment4__equipment__lot',
                                       Value(', свидетельство о поверке № '), 'equipment4__newcertnumber',
                                       Value(' от '), 'equipment4__newdate',
                                       # Value(', '),
                                       Value(' действительно до '), 'equipment4__newdatedead',
                                       )). \
        get(pk=pk)

    meteo = MeteorologicalParameters.objects. \
        annotate(equipment_meteo=Concat('equipment1__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(' , зав. № '), 'equipment1__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        )).\
        annotate(equipment_meteo1=Concat('equipment2__charakters__name',                                        
                                        Value(' тип '), 'equipment2__charakters__typename',
                                        Value(' , зав. № '), 'equipment2__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment2__newcertnumber',
                                        Value(' от '), 'equipment2__newdate',
                                        Value(' действительно до '), 'equipment2__newdatedead',
                                        )).\
        get(date__exact=note.date, roomnumber__roomnumber__exact=note.room)

    if note.name[0:2] == 'ВЖ':
        constit = constitoptional[0]
    if note.name[0:2] == 'CC':
        constit = constitoptional[1]
    if note.name[0:2] == 'ТМ':
        constit = constitoptional[2]
    if note.name[0:2] != 'ВЖ' and note.name[0:2] != 'СС' and note.name[0:2] != 'TM':
        constit = constitoptional[3]
        
    ndocument = note.ndocument
    
    if note.aim == aimoptional[1][1]:
        measureresult = str(note.certifiedValue_text).replace('.',',')
    if note.aim != aimoptional[1][1]:
        measureresult = note.certifiedValue
    if note.aim == aimoptional[0][1]:
       conclusion = conclusionoptional[0]
    if note.aim == aimoptional[1][1]:
       conclusion = conclusionoptional[1]
    if note.aim == aimoptional[2][1]:
       conclusion = conclusionoptional[2]
    if note.aim == aimoptional[3][1]:
       conclusion = conclusionoptional[3]
    if note.aim == aimoptional[4][1]:
       conclusion = conclusionoptional[4]

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}_protocol.xls"'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('protocol', cell_overwrite_ok=True)

    ws.col(0).width = 400
    ws.col(1).width = 6000
    ws.col(2).width = 3500
    ws.col(3).width = 3500
    ws.col(4).width = 2700
    ws.col(5).width = 2700
    ws.col(6).width = 2700
    ws.col(7).width = 3900
    ws.col(8).width = 3900

    Image.open(company.imglogoadress.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 2)
    sheet = wb.get_sheet(0)
    sheet.header_str = b'1'
    sheet.footer_str = b' '

    style1 = xlwt.XFStyle()
    style1.font.height = 20 * 8
    style1.font.name = 'Times New Roman'
    style1.alignment = al1
    style1.alignment.wrap = 1

    style2 = xlwt.XFStyle()
    style2.font.height = 20 * 8
    style2.font.name = 'Times New Roman'
    style2.alignment = al2
    style2.alignment.wrap = 1

    style3 = xlwt.XFStyle()
    style3.font.height = 20 * 8
    style3.font.name = 'Times New Roman'
    style3.alignment = al2
    style3.alignment.wrap = 1
    style3.num_format_str = 'DD.MM.YYYY г.'

    style4 = xlwt.XFStyle()
    style4.font.height = 20 * 8
    style4.font.name = 'Times New Roman'
    style4.alignment = al2
    style4.alignment.wrap = 1
    style4.font.bold = True

    style5 = xlwt.XFStyle()
    style5.font.height = 20 * 8
    style5.font.name = 'Times New Roman'
    style5.alignment = al2
    style5.alignment.wrap = 1
    style5.num_format_str = 'DD.MM.YYYY г.'
    style5.font.bold = True

    style6 = xlwt.XFStyle()
    style6.font.height = 20 * 8
    style6.font.name = 'Times New Roman'
    style6.alignment = al3
    style6.alignment.wrap = 1
    style6.font.bold = True

    style7 = xlwt.XFStyle()
    style7.font.height = 20 * 8
    style7.font.name = 'Times New Roman'
    style7.alignment = al3
    style7.alignment.wrap = 1
    style7.num_format_str = 'DD.MM.YYYY г.'

    style8 = xlwt.XFStyle()
    style8.font.height = 20 * 8
    style8.font.name = 'Times New Roman'
    style8.alignment = al1
    style8.alignment.wrap = 1
    style8.borders = b1
    style5.num_format_str = '0.0000'

    style9 = xlwt.XFStyle()
    style9.font.height = 20 * 8
    style9.font.name = 'Times New Roman'
    style9.alignment = al1
    style9.alignment.wrap = 1
    style9.borders = b1
    style9.font.bold = True

    style10 = xlwt.XFStyle()
    style10.font.height = 20 * 8
    style10.font.name = 'Times New Roman'
    style10.alignment = al1
    style10.alignment.wrap = 1
    style10.borders = b2

    style11 = xlwt.XFStyle()
    style11.font.height = 20 * 8
    style11.font.name = 'Times New Roman'
    style11.alignment = al1
    style11.alignment.wrap = 1
    style11.borders = b1
    style11.num_format_str = '0.00'

    row_num = 4
    columns = [
        sertificat9001,
        sertificat9001,
        sertificat9001,
        sertificat9001,
        '',
        affirmationprod,
        affirmationprod,
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(4, 4, 0, 3, style1)
    for col_num in range(6, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(4, 4, 6, 7, style2)
    ws.row(4).height_mismatch = True
    ws.row(4).height = 900

    row_num = 5
    columns = [
        '',
        '',
        '',
        '',
        '',
        '',
        fordate,
        fordate,
        ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 6, 7, style3)

    row_num = 6
    columns = [
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)
        ws.merge(row_num, row_num, 0, 3, style4)


    row_num = 7
    dp = get_datenow()
    columns = [
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(7, 7, 0, 3, style5)

    row_num = 8
    columns = [
        '',
        '',
        ' ',
        f' по {note.ndocument}',
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style4)

    row_num = 9
    columns = [
        '1 Наименование объекта/образца испытаний:',
        '1 Наименование объекта/образца испытаний:',
        note.name_rm,
        note.name_rm,
        note.name_rm,
        note.name_rm,
        note.name_rm,
        note.name_rm,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(9, 9, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(9, 9, 2, 7, style7)
    ws.row(9).height_mismatch = True
    ws.row(9).height = 500

    row_num = 10
    columns = [
        '2 Изготовитель материала СО: ',
        '2 Изготовитель материала СО: ',
        'ООО "Петроаналитика" ',
        'ООО "Петроаналитика" ',
        'ООО "Петроаналитика" ',
        'ООО "Петроаналитика" ',
        'ООО "Петроаналитика" ',
        'ООО "Петроаналитика" ',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(10, 10, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(10, 10, 2, 7, style7)

    row_num = 11
    columns = [
        '3 Испытатель: ',
        '3 Испытатель: ',
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
        note.performer_rm,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(11, 11, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(11, 11, 2, 7, style7)
        
    
    
    row_num = 12
    columns = [
        '4 Идентификационные данные объектов/образцов:',
        '4 Идентификационные данные объектов/образцов: ',
        constit,
        constit,
        constit,
        constit,
        constit,
        constit,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(12, 12, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(12, 12, 2, 7, style7)
    ws.row(12).height_mismatch = True
    ws.row(12).height = 600

    row_num = 13
    columns = [
        '5 Дата отбора проб:',
        '5 Дата отбора проб: ',
        takesamples,
        takesamples,
        takesamples,
        takesamples,
        takesamples,
        takesamples,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(13, 13, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(13, 13, 2, 7, style7)

    row_num = 14
    columns = [
        '6 Дата и место проведения испытаний:',
        '6 Дата и место проведения испытаний: ',
        note.date,
        company.adress,
        company.adress,
        company.adress,
        'п.',
        note.room.roomnumber,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(14, 14, 0, 1, style6)
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(3, 6):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(14, 14, 3, 5, style7)
    for col_num in range(6, 7):
        ws.write(row_num, col_num, columns[col_num], style2)
    for col_num in range(7, 8):
        ws.write(row_num, col_num, columns[col_num], style7)
    ws.row(14).height_mismatch = True
    ws.row(14).height = 500

    row_num +=1
    columns = [
        '7 Условия проведения измерений:',
        '7 Условия проведения измерений:',
        '',
        '',
        '',
        '',
        '',
        '',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    r = row_num + 1
    columns = [
        '',
        '7.1 Условия проведения \n измерений соответствуют требованиям рабочей \n эксплуатации средств измерений:',
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
        meteo.equipment_meteo,
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, r, 1, 1, style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400
    
    row_num +=1
    columns = [
        '',
        '7.1 Условия проведения \n измерений соответствуют требованиям рабочей \n эксплуатации средств измерений:',
        meteo.equipment_meteo1,
        meteo.equipment_meteo1,
        meteo.equipment_meteo1,
        meteo.equipment_meteo1,
        meteo.equipment_meteo1,
        meteo.equipment_meteo1,
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '',
        '7.2 Условия окружающей среды:',
        '',
        '',
        '',
        '',
        '',
        '',
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    p = str(meteo.pressure).replace('.', ',')
    row_num ==1
    columns = [
        '',
        'давление, кПа',
        p,
        p,
        p,
        p,
        p,
        p,
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    t = str(meteo.temperature).replace('.', ',')
    columns = [
        '',
        'температура, °С',
        t,
        t,
        t,
        t,
        t,
        t,
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    h = str(meteo.humidity).replace('.', ',')
    columns = [
        '',
        'влажность, %',
        h,
        h,
        h,
        h,
        h,
        h,
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    columns = [
        '8 Измеряемый параметр: ',
        '8 Измеряемый параметр: ',
         measureparameter,
         measureparameter,
         measureparameter,
         measureparameter,
         measureparameter,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    if note.ndocument == 'МИ-02-2018':
        normdocument = ndocumentoptional[0][1]
    if note.ndocument == 'ГОСТ 33-2016':
        normdocument = ndocumentoptional[2][1]
    if note.ndocument != 'ГОСТ 33-2016' and  note.ndocument != 'МИ-02-2018':
        normdocument = ndocumentoptional[1][1]

    row_num +=1
    columns = [
        '9 Метод измерений/методика \n измерений:  ',
        '9 Метод измерений/методика \n измерений:  ',
        normdocument,
        normdocument,
        normdocument,
        normdocument,
        normdocument,
        normdocument,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '10 Средства измерений:  ',
        '10 Средства измерений:  ',
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
        note.equipment_set,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '',
        '',
        note.equipment_set1,
        note.equipment_set1,
        note.equipment_set1,
        note.equipment_set1,
        note.equipment_set1,
        note.equipment_set1,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '',
        '',
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '',
        '',
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400


    row_num +=1
    columns = [
        '11 Обработка результатов испытаний:  ',
        '11 Обработка результатов испытаний:  ',
        f'В соответствии с {normdocument}',
        f'В соответствии с {normdocument}',
        f'В соответствии с {normdocument}',
        f'В соответствии с {normdocument}',
        f'В соответствии с {normdocument}',
        f'В соответствии с {normdocument}',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '12 Результаты испытаний:  ',
        '12 Результаты испытаний:  ',
        'приведены в таблице 1  ',
        f'В соответствии с {note.ndocument}  ',
        f'В соответствии с {note.ndocument}  ',
        f'В соответствии с {note.ndocument}  ',
        f'В соответствии с {note.ndocument}  ',
        f'В соответствии с {note.ndocument}  ',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    columns = [
        'Таблица 1. Результаты испытаний  ',
        'Таблица 1. Результаты испытаний  ',
        ' ',
        ' ',
        ' ',
        ' ',
        ' ',
        ' ',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 0, 1, style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

  
    row_num +=1
    columns = [
        f'Испытание {note.name_rm} по {ndocument}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(row_num, row_num, 0, 7, style8)
    count1=row_num





    if note.seria == False or note.seria == '0':

        row_num +=1
        columns = [
        'Аттестуемая характеристика',
        'Аттестуемая характеристика',
        'Т °C',
        'Измеренное значение Х1, мм2/с ',
        'Измеренное значение Х2, мм2/с ',
        'Измеренное значение Хср, мм2/с ',
        'Оценка приемлемости измерений, % отн. ',
        'Норматив контроля, r, % отн. ',
        ]
        for col_num in range(2):
            ws.write(row_num, col_num, columns[col_num], style9)
            ws.merge(row_num, row_num, 0, 1, style9)
        for col_num in range(1, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style9)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1050
    
        row_num +=1
        v1 = Decimal(note.viscosity1).quantize(Decimal('1.0000'), ROUND_HALF_UP)
        v2 = Decimal(note.viscosity2).quantize(Decimal('1.0000'), ROUND_HALF_UP)
        columns = [
            attcharacteristic,
            attcharacteristic,
            note.temperature,
            v1,
            v2,
            measureresult,
            note.accMeasurement,
            note.kriteriy,
        ]
        for col_num in range(2):
            ws.write(row_num, col_num, columns[col_num], style8)
            ws.merge(row_num, row_num, 0, 1, style8)
        for col_num in range(2, 3):
            ws.write(row_num, col_num, columns[col_num], style11)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style8)

    if  note.seria != '0':

        row_num +=1
        columns = [
        'Характеристика',
        'Характеристика',
        'Номер экземпляра СО',
        'Измеренное значение Х1, мм2/с ',
        'Измеренное значение Х2, мм2/с ',
        'Измеренное значение Хср, мм2/с ',
        'Оценка приемлемости измерений, % отн. ',
        'Норматив контроля, r, % отн.',
        ]
        for col_num in range(2):
            ws.write(row_num, col_num, columns[col_num], style9)
            ws.merge(row_num, row_num, 0, 1, style9)
        for col_num in range(1, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style9)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1050

        a = note.seria
        qseria = ViscosityMJL.objects.all().filter(seria=a). \
        values_list(
        'numberexample',
        'viscosity1',
        'viscosity2',    
        'certifiedValue',
        'accMeasurement',
        )
        
        for row in qseria:
            row_num += 1
            for col_num in range(0, 5):
                ws.write(row_num, col_num + 2, row[col_num], style8)
        counthe = row_num
            
        row_num1 = count1 + 2
        columns = [
        f'Кинематическая вязкость, мм2/с при {note.temperature} °С',
        f'Кинематическая вязкость, мм2/с при {note.temperature} °С',
        ]
        for col_num in range(2):
            ws.write(row_num1, col_num, columns[col_num], style8)
            ws.merge(row_num1, counthe, 0, 1, style8)

        row_num2 = count1 + 2
        columns = [
        note.kriteriy,
        ]
        for col_num in range(1):
            ws.write(row_num2, col_num + 7, columns[col_num], style8)
            ws.merge(row_num2, counthe, 7, 7, style8)



    row_num +=1
    columns = [
        'Дополнительные сведения: ',
        'Дополнительные сведения: ',
        note.aim,
        note.aim,
        note.aim,
        note.aim,
        note.aim,
        note.aim,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    columns = [
        'Выводы: ',
        'Выводы: ',  
        conclusion,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1000

    row_num +=1
    columns = [
        company.prohibitet
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 0, 7, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1000

    row_num +=1
    columns = [
        'Исполнитель: ',
        'Исполнитель: ',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)

    row_num +=1
    columns = [
        note.performer.profile.userposition,
        note.performer.profile.userposition,
        note.performer.profile.userposition,
        '(подпись)',
        note.performer.username,
        note.performer.username,
        note.performer.username,
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style2)
    for col_num in range(3, 4):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 4, 7, style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 600

    wb.save(response)
    return response
