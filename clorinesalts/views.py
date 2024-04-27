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
from django.db.models.functions import Concat

from jouViscosity.models import CvKinematicviscosityVG, CvDensityDinamicVG
from main.models import AttestationJ
from .models import Clorinesalts, CommentsClorinesalts, IndicatorDFK, TitrantHg, GetTitrHg, ClorinesaltsCV, \
    CommentsClorinesaltsCV
from .forms import*
from textconstants import *
from equipment.models import CompanyCard
from metods import *
from .forms import *
from utils_forms import*
from .models import *
from .j_constants import *
from utils import *
from textconstants import *

JOURNAL = AttestationJ
MODEL = Clorinesalts
COMMENTMODEL = CommentsClorinesalts
NAME = 'хлористые соли'
COLONTITUL = 'ИСП_ГОСТ 21534 (метод А)'
from utils_forms import*
from .j_constants import *

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


class ProtocolbuttonView(Constants, ProtocolbuttonView):
    """ Выводит кнопку для формирования протокола """
    template_name = URL + '/buttonprotocol.html'



class StrDPKView(View):
    """ выводит отдельную запись об изготовлении индикатора """
    """уникальное для титрования"""

    def get(self, request, pk):
        obj = get_object_or_404(IndicatorDFK, pk=pk)
        return render(request, URL + '/strDPK.html',  {'obj': obj})
        
def SeriaUpdate(request, str):
    """выводит страницу с формой для обновления номера серии измерений""" 
    title = f'{Clorinesalts.objects.get(pk=str).name}, п. {Clorinesalts.objects.get(pk=str).lot}'
    if request.method == "POST":
        form = SeriaUpdateForm(request.POST, request.FILES,  instance=Clorinesalts.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect(f'/attestationJ/clorinesalts/attestation/{str}/')  
    else:
        form = SeriaUpdateForm(instance=Clorinesalts.objects.get(pk=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/reg.html', data)

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
        index = self.request.GET['index']
        lot = self.request.GET['lot']
        if name and lot:
            objects = MODEL.objects.filter(name=name).filter(index=index).filter(lot=lot).order_by('-pk')
            context['objects'] = objects
        if name and not lot:
            objects = MODEL.objects.filter(name=name).filter(index=index).order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm(initial={'name': name, 'index': index,'lot': lot})
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
        index = self.request.GET['index']
        lot = self.request.GET['lot']
        if name and lot:
            objects = ClorinesaltsCV.objects.filter(fixation=True).filter(clorinesalts__name=name).filter(clorinesalts__index=index).filter(clorinesalts__lot=lot).order_by('-pk')
            context['objects'] = objects
        if name and not lot:
            objects = ClorinesaltsCV.objects.filter(fixation=True).filter(clorinesalts__name=name).filter(clorinesalts__index=index).order_by('-pk')
            context['objects'] = objects
        context['journal'] = JOURNAL.objects.filter(for_url=URL)
        context['formSM'] = SearchForm(initial={'name': name, 'index': index,'lot': lot})
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







def export_protocol_xls(request, pk):
    """представление для выгрузки протокола испытаний в ексель"""
    company = CompanyCard.objects.get(pk=1)
    note = Clorinesalts.objects.\
        annotate(name_rm=Concat(Value('СО '), 'name', Value(' , партия '), 'lot')).\
        annotate(performer_rm=Concat('performer__profile__userposition', Value(' '), 'performer__username')).get(pk=pk)
        
        

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


    for i in range(len(MATERIAL)):
        if self.name == MATERIAL[i][0]:
            self.constit = constitoptional[i]

    ndocument = note.ndocument

    for i in range(len(aimoptional)):
        if self.aim == aimoptional[i][0]:
            self.constit = conclusionoptional[i]
    
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
        note.equipment1,
        note.equipment1,
        note.equipment1,
        note.equipment1,
        note.equipment1,
        note.equipment1,
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
        'Измеренное значение Х1, мг/дм3 ',
        'Измеренное значение Х2, мг/дм3 ',
        'Измеренное значение Хср, мг/дм3 ',
        'Оценка приемлемости измерений, мг/дм3. ',
        'Норматив контроля, r,мг/дм3 ',
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
            attcharacteristic,
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
        'Измеренное значение Х1, мг/дм3 ',
        'Измеренное значение Х2, мг/дм3 ',
        'Измеренное значение Хср, мг/дм3 ',
        'Оценка приемлемости измерений, мг/дм3 ',
        'Норматив контроля, r, мг/дм3',
        ]
        for col_num in range(2):
            ws.write(row_num, col_num, columns[col_num], style9)
            ws.merge(row_num, row_num, 0, 1, style9)
        for col_num in range(1, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style9)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1050

        a = note.seria
        qseria = Clorinesalts.objects.all().filter(seria=a). \
        values_list(
        'numberexample',
        'x1',
        'x2',    
        'x_avg',
        'accMeasurement',
        )
        
        for row in qseria:
            row_num += 1
            for col_num in range(0, 5):
                ws.write(row_num, col_num + 2, row[col_num], style8)
        counthe = row_num
            
        row_num1 = count1 + 2
        columns = [
        attcharacteristic,
        attcharacteristic,
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

