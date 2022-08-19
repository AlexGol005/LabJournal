import xlwt
from datetime import timedelta, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Max, Q, F, Value
from django.db.models.functions import Upper, Concat
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import upper
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView

from equipment.forms import SearchMEForm, NoteCreationForm, EquipmentUpdateForm, VerificationRegForm, \
    CommentsVerificationCreationForm, VerificatorsCreationForm, VerificatorPersonCreationForm, EquipmentCreateForm
from equipment.models import MeasurEquipment, Verificationequipment, Roomschange, Personchange, CommentsEquipment, \
    Equipment, CommentsVerificationequipment

URL = 'equipment'

class EquipmentView(ListView):
    """ Выводит список Всего ЛО """
    model = Equipment
    template_name = URL + '/equipmentlist.html'
    context_object_name = 'objects'
    ordering = ['exnumber']


class MeasurEquipmentView(ListView):
    """ Выводит список средств измерений """
    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters__name']
    paginate_by = 12

    def get_queryset(self):
        queryset = MeasurEquipment.objects.exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


class SearchResultMeasurEquipmentView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку средств измерений """

    template_name = URL + '/measureequipment.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultMeasurEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']
        dateser = self.request.GET['dateser']
        if dateser:
            delt = datetime.now() - timedelta(days=60 * 24 * 7)

        get_id_actual = Verificationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))

        if name and not lot and not exnumber and not dateser:
            objects = MeasurEquipment.objects.\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot and not dateser:
            objects = MeasurEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber and not dateser:
            objects = MeasurEquipment.objects.\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and not lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot).\
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and exnumber:
            objects = MeasurEquipment.objects. \
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = MeasurEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_ver__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects

        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber, 'dateser': dateser})
        context['URL'] = URL
        return context


class StrMeasurEquipmentView(View):
    """ выводит отдельную страницу СИ """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(MeasurEquipment, equipment__exnumber=str)
        return render(request, URL + '/equipmentstr.html',
                      {'obj': obj, 'note': note})


class CommentsView(View):
    """ выводит комментарии к записи в журнале и форму для добавления комментариев """
    """Стандартное"""
    form_class = NoteCreationForm
    initial = {'key': 'value'}
    template_name = 'equipment/comments.html'

    def get(self, request, str):
        note = CommentsEquipment.objects.filter(forNote__exnumber=str)
        title = Equipment.objects.get(exnumber=str)
        form = NoteCreationForm()
        return render(request, 'equipment/comments.html', {'note': note, 'title': title, 'form': form, 'URL': URL})

    def post(self, request, str, *args, **kwargs):
        form = NoteCreationForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user and not order.author:
                order.author = request.user
            if not request.user and order.author:
                order.author = order.author
            order.forNote = Equipment.objects.get(exnumber=str)
            order.save()
            messages.success(request, f'Запись добавлена!')
            return redirect(order)


def EquipmentUpdate(request, str):
    """выводит форму для обновления разрешенных полей оборудования ответственному за оборудование"""
    title = Equipment.objects.get(exnumber=str)
    get_pk = title.personchange_set.latest('pk').pk
    person = Personchange.objects.get(pk=get_pk).person

    if person == request.user or request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentUpdateForm(request.POST, request.FILES,  instance=Equipment.objects.get(exnumber=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect(reverse('measureequipment', kwargs={'str': str}))
    if person != request.user and not request.user.is_superuser:
        messages.success(request, f' Для внесения записей о приборе нажмите на кнопку ниже:'
                                  f' "Внести запись о приборе и смотреть записи (для всех пользователей)"'
                                  f'. Добавить особенности работы или поменять статус может только ответственный '
                                  f'за прибор или поверку.')

        return redirect(reverse('measureequipment', kwargs={'str': str}))
    else:
        form = EquipmentUpdateForm(instance=Equipment.objects.get(exnumber=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/individuality.html', data)

class VerificationequipmentView(View):
    """ выводит историю поверок и форму для добавления комментария к истории поверок """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        strreg = note.latest('pk').equipmentSM.equipment.exnumber
        calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        title = Equipment.objects.get(exnumber=str)
        dateorder = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        now = date.today()
        try:
            comment = CommentsVerificationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsVerificationCreationForm(initial={'comment': comment})
        data = {'note': note,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/verification.html', data)
    def post(self, request, str, *args, **kwargs):
        form = CommentsVerificationCreationForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('measureequipmentver', kwargs={'str': str}))

@login_required
def VerificationReg(request, str):
    """выводит форму для внесения сведений о поверке"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = VerificationRegForm(request.POST)
            form2 = VerificatorsCreationForm(request.POST)
            form3 = VerificatorPersonCreationForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = MeasurEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
            if form2.is_valid():
                order = form2.save(commit=False)
                order.save()
                return redirect(reverse('measureequipmentver', kwargs={'str': str}))
            if form3.is_valid():
                order = form3.save(commit=False)
                order.save()
                return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = VerificationRegForm()
        form2 = VerificatorsCreationForm()
        form3 = VerificatorPersonCreationForm(request.POST)
    data = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'title': title
            }
    return render(request, 'equipment/verificationreg.html', data)


@login_required
def EquipmentReg(request):
    """выводит форму для внесения нового ЛО"""
    if request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentCreateForm(request.POST)
            # form2 = VerificatorsCreationForm(request.POST)
            # form3 = VerificatorPersonCreationForm(request.POST)

            if form.is_valid():
                order = form.save(commit=False)
                a = Equipment.objects.get()
                order.exnumber = exnumber
                order.save()
                # return redirect(f'/equipment/measureequipment/{order.exnumber}/')
                return redirect('equipmentlist')
            # if form2.is_valid():
            #     order = form2.save(commit=False)
            #     order.save()
            #     return redirect(reverse('measureequipmentver', kwargs={'str': str}))
            # if form3.is_valid():
            #     order = form3.save(commit=False)
            #     order.save()
            #     return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('equipmentreg')
    else:
        form = EquipmentCreateForm()
        # form2 = VerificatorsCreationForm()
        # form3 = VerificatorPersonCreationForm(request.POST)
        content = {
            'form': form,
                }
        return render(request, 'equipment/equipmentreg.html', content)

# -------------------


def export_me_xls(request):
    '''представление для выгрузки списка всех СИ в ексель'''
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="measure equipment.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('График поверки СИ', cell_overwrite_ok=True)

    # ширина столбцов
    ws.col(2).width = 4500
    ws.col(8).width = 3000

    # заголовки, первый ряд
    row_num = 0

    def set_style_top():
        style = xlwt.XFStyle()
        style.font.bold = True
        style.font.name = 'Calibri'
        style.borders.left = 1
        style.borders.right = 1
        style.borders.top = 1
        style.borders.bottom = 1

        style.alignment.wrap = 1
        style.alignment.horz = 0x02
        style.alignment.vert = 0x01


        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['tan']
        style.pattern = pattern

        return style

    columns = [
                # '№',
                'Внутренний  номер',
                'Номер в госреестре',
                'Наименование',
                'Тип/Модификация',
                'Заводской номер',
                'Год выпуска',
                'Новый или б/у',
                'Год ввода в эксплуатацию',
                'Страна, наименование производителя',
                'Место установки или хранения',
                'Ответственный за СИ',
                'Статус',
                'Ссылка на сведения о поверке',
                'Краткий номер свидетельства',
                'Дата поверки/калибровки',
                'Дата окончания свидетельства',
                'Дата заказа поверки/калибровки',
                'Периодичность поверки /калибровки (месяцы)',
                'Инвентарный номер',
                'Ссылка на карточку',
               ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], set_style_top())
        # ws.merge(0, 0, 3, 4)

    # значения, остальные ряды
    def set_style_body():
        style = xlwt.XFStyle()

        style.font.name = 'Calibri'

        style.borders.left = 1
        style.borders.right = 1
        style.borders.top = 1
        style.borders.bottom = 1

        style.alignment.wrap = 1
        style.alignment.horz = 0x02
        style.alignment.vert = 0x01
        return style

    get_id_room = Roomschange.objects.select_related('equipment').values('equipment'). \
        annotate(id_actual=Max('id')).values('id_actual')
    list_ = list(get_id_room)
    setroom = []
    for n in list_:
        setroom.append(n.get('id_actual'))

    get_id_person = Personchange.objects.select_related('equipment').values('equipment'). \
        annotate(id_actual=Max('id')).values('id_actual')
    list_ = list(get_id_person)
    setperson = []
    for n in list_:
        setperson.append(n.get('id_actual'))

    get_id_verification = Verificationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
        annotate(id_actual=Max('id')).values('id_actual')
    list_ = list(get_id_verification)
    setver = []
    for n in list_:
        setver.append(n.get('id_actual'))

    rows = MeasurEquipment.objects.all().\
        annotate(mod_type=Concat('charakters__modtype__typename', 'charakters__modtype__modificname'),
    manuf_country=Concat('equipment__manufacturer__country', Value(', '), 'equipment__manufacturer__companyName')).\
        filter(equipment__roomschange__in=setroom).\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__in=setver).\
        exclude(equipment__status='C').\
        values_list(
            'equipment__exnumber',
            'charakters__reestr',
            'charakters__name',
            'mod_type',
            'equipment__lot',
            'equipment__yearmanuf',
            'equipment__new',
            'equipment__yearintoservice',
            'manuf_country',
            'equipment__roomschange__roomnumber__roomnumber',
            'equipment__personchange__person__username',
            'equipment__status',
            'equipmentSM_ver__arshin',
            'equipmentSM_ver__certnumbershort',
            'equipmentSM_ver__date',
            'equipmentSM_ver__datedead',
            'equipmentSM_ver__dateorder',
            'charakters__calinterval',
            'equipment__invnumber',
            'ecard',
        )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], set_style_body())
            # ws.merge(1, 1, 3, 4)


    wb.save(response)
    return response
