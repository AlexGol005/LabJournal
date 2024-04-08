# все стандратно кроме поиска по полям, импорта моделей и констант
from PIL import Image
import xlwt
from django.db.models import Value
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import render
from xlwt import Alignment, Borders

from jouViscosity.models import CvKinematicviscosityVG
from kinematicviscosity.models import ViscosityMJL

# этот блок нужен для всех журналов
from equipment.models import CompanyCard
from .forms import *
from utils_forms import*
from .models import *

from .j_constants import *
from kinematicviscosity.constvisc import *
from utils import *
from metods import *
from textconstants import *


MODEL = Dinamicviscosity
COMMENTMODEL = CommentsDinamicviscosity

class Constants:
    URL = URL
    JOURNAL = JOURNAL
    MODEL = MODEL
    COMMENTMODEL = COMMENTMODEL
    NAME = NAME
    journal = journal
    SearchForm = SearchForm
    SearchDateForm = SearchDateForm
# конец блока для всех журналов

# блок стандартных 'View' но с индивидуальностями,  возможно унаследованных от стандартных классов из модуля utils
class PicnometerView(TemplateView):
    """ Представление, которое выводит табличку с объёмами пикнометра """
    """ уникальное """
    template_name = 'dinamicviscosity/picnometer.html'


class RegView(RegView):
    """ Представление, которое выводит форму регистрации в журнале. """
    """ метод форм валид перегружен для заполнения полей """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = URL + '/registration.html'
        self.form_class = StrJournalCreationForm
        self.success_message = "Запись внесена, подтвердите АЗ!"

    def form_valid(self, form):
        order = form.save(commit=False)
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
            if kinematicviscosity.cvt100dead >= date.today():
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


# блок  'View' для различных поисков (не унаследованные)
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


def filterview(request, pk):
    """ Фильтры записей об измерениях по дате, АЗ, мои записи и пр """
    """Стандартная"""
    journal = JOURNAL.objects.filter(for_url=URL)
    objects = MODEL.objects.all()
    formSM = SearchForm()
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
            date__gte=datetime.datetime.now()).order_by('-pk')
    return render(request, URL + "/journal.html", {'objects': objects, 'journal': journal, 'formSM': formSM, 'URL': URL,
                                                   'formdate': formdate})



# ---------------------------------------------
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
    '''представление для выгрузки отдельной странички журнала в ексель'''
    note = MODEL.objects.get(pk=pk)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'{note.name}, п. {note.lot},{note.temperature}', cell_overwrite_ok=True)
    ws.header_str = b''
    ws.footer_str = b''


    for i in range(26):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600

    ws.row(22).height_mismatch = True
    ws.row(22).height = 800

    for i in range(22, 25):
        ws.row(i).height_mismatch = True
        ws.row(i).height = 600


    # ширина столбцов
    ws.col(0).width = 4000
    ws.col(1).width = 4000
    ws.col(2).width = 4000
    ws.col(3).width = 2700
    ws.col(4).width = 6500

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
    style7.alignment = al1

    style8 = xlwt.XFStyle()
    style8.font.name = 'Times New Roman'
    style8.borders = b1
    style8.alignment = al1
    style8.num_format_str = '0.0000'


    row_num = 0
    columns = [
        f'{AttestationJ.objects.get(id=2).name}___{note.date.year}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 4, style6)

    row_num = 2
    columns = [
        'Дата измерения',
        'Индекс СО',
        'Номер внутренней партии',
        'Т, °C',
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
        f'Измерение плотности {note.equipment}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(4, 4, 0, 4, style1)

    if note.equipment == 'денсиметром':
        note.piknometer_volume = '-'
        note.piknometer_mass1 = '-'
        note.piknometer_mass2 = '-'
        note.piknometer_plus_SM_mass1 = '-'
        note.piknometer_plus_SM_mass2 = '-'
        note.SM_mass1 = '-'
        note.SM_mass2 = '-'

    row_num = 5
    columns = [
        'V(пикн.), см3',
        note.piknometer_volume,
        'Измерение 1',
        'Измерение 2',
        'Измерение 2',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(5, 5, 2, 3, style2)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)

    row_num = 6
    columns = [
        'm(пикн.), г',
        'm(пикн.), г',
        note.piknometer_mass1,
        note.piknometer_mass2,
        note.piknometer_mass2,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(6, 6, 0, 1, style1)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(6, 6, 2, 3, style2)

    row_num = 7
    columns = [
        'm(СО + пикн.), г',
        'm(СО + пикн.), г',
        note.piknometer_plus_SM_mass1,
        note.piknometer_plus_SM_mass2,
        note.piknometer_plus_SM_mass2,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(7, 7, 0, 1, style1)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(7, 7, 2, 3, style8)

    row_num = 8
    columns = [
        'm(СО), г',
        'm(СО), г',
        note.SM_mass1,
        note.SM_mass2,
        note.SM_mass2,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(8, 8, 0, 1, style1)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(8, 8, 2, 3, style8)

    row_num = 9
    columns = [
        'ρ1, г/см3',
        'ρ1, г/см3',
        note.density1,
        note.density1,
        note.density1,

    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(9, 9, 0, 1, style1)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(9, 9, 2, 4, style2)

    row_num = 10
    columns = [
        'ρ2, г/см3',
        'ρ2, г/см3',
        note.density2,
        note.density2,
        note.density2,

    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(10, 10, 0, 1, style1)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(10, 10, 2, 4, style2)

    try:
        row_num = 11
        columns = [
            'плотность измерил',
            'плотность измерил',
            note.performerdensity.username,
            note.performerdensity.username,
            note.performerdensity.username,
        ]
        for col_num in range(1):
            ws.write(row_num, col_num, columns[col_num], style1)
            ws.merge(11, 11, 0, 1, style1)
        for col_num in range(2, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style2)
            ws.merge(11, 11, 2, 4, style2)
    except:
        row_num = 11
        columns = [
            'плотность измерил',
            'плотность измерил',
            ' ',
            ' ',
            ' ',
        ]
        for col_num in range(1):
            ws.write(row_num, col_num, columns[col_num], style1)
            ws.merge(11, 11, 0, 1, style1)
        for col_num in range(2, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style2)
            ws.merge(11, 11, 2, 4, style2)


    row_num = 12
    columns = [
        'Обработка результатов'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(12, 12, 0, 4, style1)

    row_num = 13
    columns = [
        'ρ сред., г/см3',
        'Оценка приемлемости измерений   \n Δ = (|ρ1 - ρ2|/ρ сред.) * 100 %',
        'Оценка приемлемости измерений   \n Δ = (|ρ1 - ρ2|/ρ сред.) * 100 %',
        'Оценка приемлемости измерений   \n Δ = (|ρ1 - ρ2|/ρ сред.) * 100 %',
         'Критерий приемл. измерений, r',
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(13, 13, 1, 3, style1)

    row_num = 14
    columns = [
         note.density_avg,
         note.accMeasurement,
         note.accMeasurement,
         note.accMeasurement,
         note.kriteriy,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(14, 14, 1, 3, style2)

    row_num = 15
    columns = [
        f'Результат измерений: {note.resultMeas}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(15, 15, 0, 4, style1)

    row_num = 16
    columns = [
        'Расчёт динамической вязкости'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(16, 16, 0, 4, style1)

    row_num = 17
    columns = [
        'Вязкость кинематическая при температуре измерений, ν, мм2/с',
        'Вязкость кинематическая при температуре измерений, ν, мм2/с',
        'Вязкость динамическая, νдин = ν * ρсред , Па*с',
        'Вязкость динамическая, νдин = ν * ρсред , Па*с',
        'Вязкость динамическая, νдин = ν * ρсред , Па*с',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(17, 17, 0, 1, style1)
        ws.merge(17, 17, 2, 4, style1)

    note.kinematicviscosity = str(note.kinematicviscosity).replace('.', ',')

    row_num = 18
    columns = [
       note.kinematicviscosity,
       note.kinematicviscosity,
       note.dinamicviscosity_not_rouned,
       note.dinamicviscosity_not_rouned,
       note.dinamicviscosity_not_rouned,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(18, 18, 0, 1, style2)
        ws.merge(18, 18, 2, 4, style2)


    row_num = 19
    columns = [
       ' Результат испытаний'
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(19, 19, 0, 4, style1)

    row_num = 20
    columns = [
        'АЗ, Дин. вязк., Па * с',
        'Абс. погр.  (νдин сред. * 0,3)/ 1000',
        'Пред. зн. плот., ρпред, г/см3 ',
        'Разница с ρпред, %',
        'Разница с ρпред <= 0,7%',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)

    note.certifiedValue = str(note.certifiedValue).replace('.', ',')
    note.abserror = str(note.abserror).replace('.', ',')
    note.olddensity = str(note.olddensity).replace('.', ',')

    if not note.olddensity:
        note.deltaolddensity = '-'
        note.olddensity = '-'
        note.resultWarning = '-'
    if note.resultWarning == '' and not note.olddensity:
        note.resultWarning = '-'
    if note.resultWarning == '' and note.olddensity:
        note.resultWarning = 'да'
    if note.resultWarning == '' and not note.olddensity:
        note.resultWarning = 'нет'

    row_num = 21
    columns = [
        note.certifiedValue,
        note.abserror,
        note.olddensity,
        note.deltaolddensity,
        note.resultWarning,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)


    row_num = 22
    columns = [
        'Исполнитель',
        'Исполнитель',
        'Исполнитель',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 4, style1)

    row_num = 23
    columns = [
        str(note.performer),
        str(note.performer),
        str(note.performer),
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 4, style1)

    row_num = 26
    columns = [
        'Страница №           ',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 0, 4, style7)

    wb.save(response)
    return response


# флажок протокол
def export_protocol_xls(request, pk):
    '''представление для выгрузки протокола испытаний в ексель'''
    company = CompanyCard.objects.get(pk=1)
    note = MODEL.objects.\
        annotate(name_rm=Concat(Value('СО '), 'name', Value(' п. '), 'lot')).\
        annotate(performer_rm=Concat('performer__profile__userposition', Value(' '), 'performer__username')). \
        annotate(equipment_set=Concat('equipment1__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        # Value(', '),
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        'equipment2__charakters__name',
                                        Value(' тип '), 'equipment2__charakters__typename',
                                        Value(', свидетельство о поверке № '), 'equipment2__newcertnumber',
                                        Value(' от '), 'equipment2__newdate',
                                        # Value(', '),
                                        Value(' действительно до '), 'equipment2__newdatedead',
                                        )). \
        annotate(equipment_set2=Concat('equipment3__charakters__name',
                                       Value(' тип '), 'equipment3__charakters__typename',
                                       Value(', свидетельство о поверке № '), 'equipment3__newcertnumber',
                                       Value(' от '), 'equipment3__newdate',
                                       # Value(', '),
                                       Value(' действительно до '), 'equipment3__newdatedead',
                                       Value('; \n'),
                                       'equipment4__charakters__name',
                                       Value(' тип '), 'equipment4__charakters__typename',
                                       Value(', свидетельство о поверке № '), 'equipment4__newcertnumber',
                                       Value(' от '), 'equipment4__newdate',
                                       # Value(', '),
                                       Value(' действительно до '), 'equipment4__newdatedead',
                                       )). \
        annotate(equipment_set3=Concat('equipment5__charakters__name',
                                       Value(' тип '), 'equipment5__charakters__typename',
                                       Value(', свидетельство о поверке № '), 'equipment3__newcertnumber',
                                       Value(' от '), 'equipment3__newdate',
                                       # Value(', '),
                                       Value(' действительно до '), 'equipment5__newdatedead',
                                       )). \
        get(pk=pk)

    meteo = MeteorologicalParameters.objects. \
        annotate(equipment_meteo=Concat('equipment1__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        # Value(', '),
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        'equipment2__charakters__name',
                                        Value(' тип '), 'equipment2__charakters__typename',
                                        Value(', свидетельство о поверке № '), 'equipment2__newcertnumber',
                                        Value(' от '), 'equipment2__newdate',
                                        # Value(', '),
                                        Value(' действительно до '), 'equipment2__newdatedead',
                                        )).\
        get(date__exact=note.date, roomnumber__roomnumber__exact=note.room)

    kinematic = ViscosityMJL.objects.filter(name=note.name, lot=note.lot, temperature=note.temperature).last()

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
    sheet = wb.get_sheet(0)
    sheet.header_str = b'1/1'
    sheet.footer_str = b' '

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


    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    al2 = Alignment()
    al2.horz = Alignment.HORZ_RIGHT
    al2.vert = Alignment.VERT_CENTER

    al3 = Alignment()
    al3.horz = Alignment.HORZ_LEFT
    al3.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    b2 = Borders()
    b2.left = 6
    b2.right = 6
    b2.bottom = 6
    b2.top = 6

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
    ws.row(4).height = 1000

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
        ws.merge(6, 6, 0, 3, style4)

    row_num = 7
    dp = get_datenow()
    columns = [
        f'от  {dp}',
        f'от  {dp}',
        f'от  {dp}',
        f'от  {dp}',
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
    ws.row(12).height = 900

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

    row_num = 15
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
        ws.merge(15, 15, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(15, 15, 2, 7, style7)

    row_num = 16
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
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(16, 16, 2, 7, style7)
    ws.row(16).height_mismatch = True
    ws.row(16).height = 800

    row_num = 17
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
        ws.merge(17, 17, 2, 7, style7)


    row_num = 18
    p = str(meteo.pressure).replace('.', ',')
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
        ws.merge(18, 18, 2, 7, style7)

    row_num = 19
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
        ws.merge(19, 19, 2, 7, style7)

    row_num = 20
    columns = [
        '',
        'влажность, %',
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
        meteo.humidity,
    ]
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(20, 20, 2, 7, style7)

    row_num = 21
    columns = [
        '8 Измеряемый параметр: ',
        '8 Измеряемый параметр: ',
        measureparameter,
        measureparameter,
        measureparameter,
        measureparameter,
        measureparameter,
        measureparameter,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(21, 21, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(21, 21, 2, 7, style7)

    row_num = 22
    if note.ndocument == 'МИ-02-2018':
        normdocument = ndocumentoptional[0][1]
    if note.ndocument == 'ГОСТ 33-2016':
        normdocument = ndocumentoptional[2][1]
    if note.ndocument != 'ГОСТ 33-2016' and  note.ndocument != 'МИ-02-2018':
        normdocument = ndocumentoptional[1][1]
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
        ws.merge(22, 22, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(22, 22, 2, 7, style7)
    ws.row(22).height_mismatch = True
    ws.row(22).height = 500

    row_num = 23
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
        ws.merge(23, 23, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(23, 23, 2, 7, style7)
    ws.row(23).height_mismatch = True
    ws.row(23).height = 800

    row_num = 24
    columns = [
        '  ',
        '  ',
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
        note.equipment_set2,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(24, 24, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(24, 24, 2, 7, style7)
    ws.row(24).height_mismatch = True
    ws.row(24).height = 800

    row_num = 25
    columns = [
        '  ',
        '  ',
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
        note.equipment_set3,
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(25, 25, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(25, 25, 2, 7, style7)
    ws.row(25).height_mismatch = True
    ws.row(25).height = 500

    row_num = 26
    columns = [
        '11 Обработка результатов испытаний:  ',
        '11 Обработка результатов испытаний:  ',
         f'В соответствии с {normdocument}',
         f'В соответствии с {normdocument}',
         f'В соответствии с {normdocument}',
         f'В соответствии с {normdocument}',
         f'В соответствии с {normdocument}',
        f'В соответствии с {normdocument}'
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(26, 26, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(26, 26, 2, 7, style7)
    ws.row(26).height_mismatch = True
    ws.row(26).height = 500

    row_num = 27
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
        ws.merge(27, 27, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(27, 27, 2, 7, style7)

    row_num = 28
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
        ws.merge(28, 28, 0, 1, style7)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(28, 28, 2, 7, style7)

    row_num = 29
    columns = [
        f'Испытание {note.name_rm} по {ndocument}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(29, 29, 0, 7, style8)

    row_num = 30
    columns = [
        'Измеряемый параметр',
        'Измеряемый параметр',
        'Т °C',
        'Измеренное значение Х1, Па * с ',
        'Измеренное значение Х2, Па * с ',
        'Измеренное значение Хср, Па * с ',
        'Результат контрольной процедуры измерения, rk, % отн.',
        'Норматив контроля, r, % отн.',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style9)
        ws.merge(30, 30, 0, 1, style9)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style9)
    ws.row(30).height_mismatch = True
    ws.row(30).height = 1000

    row_num = 31
 
    columns = [
         measureparameter,
         measureparameter,
         note.temperature,
         note.density1,
         note.density2,
         note.density_avg,
         note.accMeasurement,
         note.kriteriy,
        ]


    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(31, 31, 0, 1, style8)
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], style11)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)

    row_num = 32
    columns = [
        countparameter,
        countparameter,
        f'вязкость кинематическая при температуре измерений: {note.kinematicviscosity} мм2/с; ',
        f'вязкость кинематическая при температуре измерений: {note.kinematicviscosity} мм2/с; ',
        f'вязкость кинематическая при температуре измерений: {note.kinematicviscosity} мм2/с; ',
        f'вязкость динамическая рассчитанная: {note.kinematicviscosity} Па*с.',
        f'вязкость динамическая рассчитанная: {note.kinematicviscosity} Па*с.',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(32, 32, 0, 2, style8)
    for col_num in range(3, 5):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(6, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)

    row_num = 33
    columns = [
        'Дополнительные сведения: ',
        'Дополнительные сведения: ',
        note.aim,
        note.aim,
        note.aim,
        note.aim,
        note.aim,

    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(33, 33, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(33, 33, 2, 7, style7)

    row_num = 34
    columns = [
        'Выводы: ',
        'Выводы: ',
         conclusion,

    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(34, 34, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(34, 34, 2, 7, style7)
    ws.row(34).height_mismatch = True
    ws.row(34).height = 500

    row_num = 35
    columns = [
        company.prohibitet
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(35, 35, 0, 7, style10)
    ws.row(35).height_mismatch = True
    ws.row(35).height = 1000

    row_num = 36
    columns = [
        'Исполнитель: ',
        'Исполнитель: ',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(36, 36, 0, 1, style6)

    row_num = 37
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
        ws.merge(37, 37, 0, 2, style2)
    for col_num in range(3, 4):
        ws.write(row_num, col_num, columns[col_num], style1)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(37, 37, 4, 7, style7)
    ws.row(37).height_mismatch = True
    ws.row(37).height = 600

    wb.save(response)
    return response
