import xlwt
import pytils.translit
from datetime import timedelta, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Max, Q, Value, CharField
from django.db.models.functions import Upper, Concat, Extract, ExtractYear
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import request
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView
from xlwt import Alignment, Borders

from equipment.forms import*
from equipment.models import*

URL = 'equipment'

class SearchMustVerView(ListView):
    """ выводит список СИ у которых месяц заказа поверки совпадает с указанным либо раньше него"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(SearchMustVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        queryset = MeasurEquipment.objects.exclude(equipment__status='С')
        return queryset


class MeteorologicalParametersView(TemplateView):
    """ Представление, которое выводит формы для метеопараметров """
    template_name = URL + '/meteo.html'

class MetrologicalEnsuringView(TemplateView):
    """выводит заглавную страницу для вывода данных по поверке и аттестации, списков в ексель и пр """
    template_name = URL + '/metro.html'

    def get_context_data(self, **kwargs):
        context = super(MetrologicalEnsuringView, self).get_context_data(**kwargs)
        context['form'] = DateForm()
        return context

class VerificationLabelsView(TemplateView):
    """выводит страницу с формой для ввода внутренних номеров для распечатки этикеток о метрологическом обслуживании приборов """
    template_name = URL + '/labels.html'

    def get_context_data(self, **kwargs):
        context = super(VerificationLabelsView, self).get_context_data(**kwargs)
        context['form'] = LabelEquipmentform()
        return context

class RoomsCreateView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления помещения """
    template_name = URL + '/reg.html'
    form_class = RoomsCreateForm
    success_url = '/equipment/meteo/'
    success_message = "Помещение успешно добавлено"

    def get_context_data(self, **kwargs):
        context = super(RoomsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить помещение'
        return context


class VerificatorsCreationView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления компании поверителя """
    template_name = URL + '/reg.html'
    form_class = VerificatorsCreationForm
    success_url = '/equipment/verificators/'
    success_message = "Организация поверитель успешно добавлена"

    def get_context_data(self, **kwargs):
        context = super(VerificatorsCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Внести организацию поверителя'
        return context


class VerificatorPersonCreationView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления сотрудника поверителя """
    template_name = URL + '/reg.html'
    form_class = VerificatorPersonCreationForm
    success_url = '/equipment/verificatorpersons/'
    success_message = "Сотрудник поверитель успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(VerificatorPersonCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Внести сотрудника поверителя'
        return context


class ManufacturerRegView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления производителя """
    template_name = URL + '/reg.html'
    form_class = ManufacturerCreateForm
    success_url = '/equipment/manufacturerlist/'
    success_message = "Производитель успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(ManufacturerRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить производителя ЛО'
        return context


class MeteorologicalParametersCreateView(SuccessMessageMixin, CreateView):
    """ выводит форму добавления метеопараметров """
    template_name = URL + '/reg.html'
    form_class = MeteorologicalParametersRegForm
    success_url = '/equipment/meteo/'
    success_message = "Условия окружающей среды успешно добавлены"

    def get_context_data(self, **kwargs):
        context = super(MeteorologicalParametersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить условия окружающей среды'
        return context


class MeasurEquipmentCharaktersRegView(SuccessMessageMixin, CreateView):
    """ выводит форму внесения госреестра. """
    template_name = URL + '/reg.html'
    form_class = MeasurEquipmentCharaktersCreateForm
    success_url = '/equipment/measurequipmentcharacterslist/'
    success_message = "Госреестр успешно добавлен"

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить госреестр'
        context['dopin'] = '/equipment/measureequipmentcharacterslist/'
        return context

class TestingEquipmentCharaktersRegView(SuccessMessageMixin, CreateView):
    """ выводит форму внесения характеристик ИО. """
    template_name = URL + '/reg.html'
    form_class = TestingEquipmentCharaktersCreateForm
    success_url = '/equipment/testingequipmentcharacterslist/'
    success_message = "Характеристики ИО успешно добавлены"

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить характеристики ИО'
        context['dopin'] = '/equipment/testingequipmentcharacterslist/'
        return context

class MeasureequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации СИ на основе ЛО и Госреестра """
    form_class = MeasurEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(MeasureequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать СИ'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
                order.save()
                return redirect(f'/equipment/measureequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Регистрировать может только ответственный за поверку приборов')
            return redirect(reverse('measureequipmentreg', kwargs={'str': self.kwargs['str']}))


class TestingequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации ИО на основе ЛО и характеристик ИО """
    form_class = TestingEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(TestingequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать ИО'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
                order.save()
                return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Регистрировать может только ответственный за метрологическое обеспечение приборов')
            return redirect(reverse('testequipmentreg', kwargs={'str': self.kwargs['str']}))



# class MeasureequipmentregView(View):
#     """ выводит форму регистрации СИ на основе ЛО и Госреестра """
#     def get(self, request, str):
#         form = MeasurEquipmentCreateForm()
#         title = 'Зарегистрировать СИ'
#         dop = Equipment.objects.get(exnumber=str)
#         data = {
#                 'title': title,
#                 'dop': dop,
#                 'form': form,
#                 }
#         return render(request, 'equipment/reg.html', data)
#     def post(self, request, str, *args, **kwargs):
#         form = MeasurEquipmentCreateForm(request.POST)
#         if request.user.is_superuser:
#             if form.is_valid():
#                 order = form.save(commit=False)
#                 order.equipment = Equipment.objects.get(exnumber=str)
#                 try:
#                     order.save()
#                 except:
#                     messages.success(request, f'Такой прибор уже есть')
#                 return redirect(f'/equipment/measureequipment/{str}')
#         else:
#             messages.success(request, f'Регистрировать может только ответственный за поверку приборов')
#             return redirect(reverse('measureequipmentreg', kwargs={'str': str}))


class EquipmentView(ListView):
    """ Выводит список Всего ЛО """
    model = Equipment
    template_name = URL + '/equipmentlist.html'
    context_object_name = 'objects'
    ordering = ['exnumber']
    paginate_by = 12

class VerificatorsView(ListView):
    """ Выводит список всех организаций поверителей """
    model = Verificators
    template_name = 'main/plainlist.html'
    context_object_name = 'objects'


class VerificatorsPersonsView(ListView):
    """ Выводит список всех сотрудников поверителей """
    model = VerificatorPerson
    template_name = 'main/plainlist.html'
    context_object_name = 'objects'


class ManufacturerView(ListView):
    """ Выводит список всех производителей """
    model = Manufacturer
    template_name = URL + '/manufacturerlist.html'
    context_object_name = 'objects'
    ordering = ['companyName']
    paginate_by = 12


class MeasurEquipmentCharaktersView(ListView):
    """ Выводит список госреестров """
    model = MeasurEquipmentCharakters
    template_name = URL + '/measurequipmentcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['reestr']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MeasurEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchreestrform()
        return context

class TestingEquipmentCharaktersView(ListView):
    """ Выводит список характеристик ИО """
    model = TestingEquipmentCharakters
    template_name = URL + '/testingequipmentcharacterslist.html'
    context_object_name = 'objects'
    ordering = ['name']
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TestingEquipmentCharaktersView, self).get_context_data(**kwargs)
        context['form'] = Searchtestingform()
        return context

class ReestrsearresView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку характеристик ИО """

    template_name = URL + '/measurequipmentcharacterslist.html'

    def get_context_data(self, **kwargs):
        context = super(ReestrsearresView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        if name:
            objects = MeasurEquipmentCharakters.objects.\
            filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
            context['objects'] = objects
        context['form'] = Searchreestrform(initial={'name': name})
        context['URL'] = URL
        return context

class ChromatoView(TemplateView):
    """ Представление, которое выводит список принадлежностей для хроматографа """
    template_name = URL + '/chromato.html'


class MeasurEquipmentView(ListView):
    """ Выводит список средств измерений """
    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']
    paginate_by = 12

    def get_queryset(self):
        queryset = MeasurEquipment.objects.exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MeasurEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


class TestingEquipmentView(ListView):
    """ Выводит список испытательного оборудования """
    template_name = URL + '/testingequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters__name']
    paginate_by = 12

    def get_queryset(self):
        queryset = TestingEquipment.objects.exclude(equipment__status='С')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context


class StrMeasurEquipmentView(View):
    """ выводит отдельную страницу СИ """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(MeasurEquipment, equipment__exnumber=str)
        context =  {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/equipmentstr.html', context)


class StrTestEquipmentView(View):
    """ выводит отдельную страницу ИО """
    def get(self, request, str):
        note = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(TestingEquipment, equipment__exnumber=str)
        context = {
            'obj': obj,
            'note': note,
        }
        return render(request, URL + '/testingequipmentstr.html', context)


class CommentsView(View):
    """ выводит комментарии к оборудованию и форму для добавления комментариев """
    form_class = NoteCreationForm
    initial = {'key': 'value'}
    template_name = 'equipment/comments.html'

    def get(self, request, str):
        note = CommentsEquipment.objects.filter(forNote__exnumber=str).order_by('-pk')
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
    try:
        get_pk = title.personchange_set.latest('pk').pk
        person = Personchange.objects.get(pk=get_pk).person
    except:
        person = 1

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
        try:
            strreg = note.latest('pk').equipmentSM.equipment.exnumber
        except:
            strreg = Equipment.objects.get(exnumber=str).exnumber
        try:
            calinterval = note.latest('pk').equipmentSM.charakters.calinterval
        except:
            calinterval = '-'
        title = Equipment.objects.get(exnumber=str)
        try:
            dateorder = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не поверен'
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
            form = VerificationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = MeasurEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = VerificationRegForm()
    data = {
        'form': form,
        'title': title
            }
    return render(request, 'equipment/verificationreg.html', data)


@login_required
def EquipmentReg(request):
    """выводит форму для регистрации  ЛО"""
    if request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentCreateForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                # try:
                #     a = Equipment.objects.filter(exnumber__startswith=order.exnumber).last().exnumber
                #     b = int(str(a)[-3::]) + 1
                #     c = str(b).rjust(3, '0')
                #     d = str(order.exnumber) + c
                #     order.exnumber = d
                # except:
                #     order.exnumber = str(order.exnumber) + '001'
                order.save()
                if order.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipmentreg/{order.exnumber}/')
                if order.kategory == 'ИО':
                    return redirect(f'/equipment/testequipmentreg/{order.exnumber}/')
                else:
                    return redirect('equipmentlist')
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect('equipmentreg')
    else:
        form = EquipmentCreateForm()
        form2 = ManufacturerCreateForm(request.POST)
        # form3 = VerificatorPersonCreationForm(request.POST)
        content = {
            'form': form,
                }
        return render(request, 'equipment/equipmentreg.html', content)


class DocsConsView(View):
    """ выводит список принадлежностей прибора и форму для добавления принадлежности """
    def get(self, request, str):
        template_name = 'equipment/docsconslist.html'
        form = DocsConsCreateForm()
        title = Equipment.objects.get(exnumber=str)
        objects = DocsCons.objects.filter(equipment__exnumber=str).order_by('pk')
        context = {
                'title': title,
                'form': form,
                'objects': objects,
                }
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = DocsConsCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=str)
            order.save()
            return redirect(f'/equipment/docsreg/{str}')



class PersonchangeFormView(View):
    """вывод формы смены ответсвенного за прибор, URL=personchangereg/<str:str>/"""
    def get(self, request, str):
        title = 'Смена ответственного за прибор'
        dop = Equipment.objects.get(exnumber=str)
        form = PersonchangeForm()
        context = {
            'title': title,
            'dop': dop,
            'form': form,
        }
        template_name = 'equipment/reg.html'
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = PersonchangeForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(f'/equipment/measureequipment/{str}')
        else:
            messages.success(request, f'Раздел для ответственного за поверку приборов')
            return redirect(f'/equipment/measureequipment/{str}')

class RoomschangeFormView(View):
    """вывод формы смены помещения, URL=roomschangereg/<str:str>/"""
    def get(self, request, str):
        title = 'Смена размещения прибора'
        dop = Equipment.objects.get(exnumber=str)
        form = RoomschangeForm()
        context = {
            'title': title,
            'dop': dop,
            'form': form,
        }
        template_name = 'equipment/reg.html'
        return render(request, template_name, context)

    def post(self, request, str, *args, **kwargs):
        form = RoomschangeForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(f'/equipment/measureequipment/{str}')
        else:
            messages.success(request, f'Раздел для ответственного за поверку приборов')
            return redirect(f'/equipment/measureequipment/{str}')

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


class SearchResultTestingEquipmentView(TemplateView):
    """ Представление, которое выводит результаты поиска по списку испытательного оборудования """

    template_name = URL + '/testingequipment.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultTestingEquipmentView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        exnumber = self.request.GET['exnumber']
        lot = self.request.GET['lot']
        dateser = self.request.GET['dateser']
        if dateser:
            delt = datetime.now() - timedelta(days=60 * 24 * 7)

        get_id_actual = TestingEquipment.objects.select_related('equipmentSM_att').values('equipmentSM_att'). \
            annotate(id_actual=Max('id')).values('id_actual')
        list_ = list(get_id_actual)
        set = []
        for n in list_:
            set.append(n.get('id_actual'))

        if name and not lot and not exnumber and not dateser:
            objects = TestingEquipment.objects.\
            filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if lot and not name  and not exnumber and not dateser:
            objects = TestingEquipment.objects.filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and not lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if exnumber and name and not lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                order_by('charakters__name')
            context['objects'] = objects
        if exnumber and not name and lot and not dateser:
            objects = TestingEquipment.objects.filter(equipment__exnumber=exnumber).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if lot and name and not exnumber and not dateser:
            objects = TestingEquipment.objects.\
                filter(Q(charakters__name__icontains=name)|Q(charakters__name__icontains=name1)).\
                filter(equipment__lot=lot).order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and not lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_ver__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot).\
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and exnumber:
            objects = TestingEquipment.objects. \
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and not name and not lot and exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(equipment__exnumber=exnumber). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                filter(Q(charakters__name__icontains=name) | Q(charakters__name__icontains=name1)). \
                filter(equipment__lot=lot). \
                order_by('charakters__name')
            context['objects'] = objects

        context['form'] = SearchMEForm(initial={'name': name, 'lot': lot, 'exnumber': exnumber, 'dateser': dateser})
        context['URL'] = URL
        return context


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


    style = xlwt.XFStyle()



    style.font.name = 'Calibri'

    style.borders.left = 1
    style.borders.right = 1
    style.borders.top = 1
    style.borders.bottom = 1

    style.alignment.wrap = 1
    style.alignment.horz = 0x02
    style.alignment.vert = 0x01


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
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
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
            ws.write(row_num, col_num, row[col_num], style)

    wb.save(response)
    return response


def export_mecard_xls(request, pk):
    '''представление для выгрузки карточки на прибор (СИ) в ексель'''
    note = MeasurEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' +\
                pytils.translit.translify(note.charakters.name) +\
                ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Основная информация', cell_overwrite_ok=True)

    ws.col(0).width = 2700
    ws.col(1).width = 2500
    ws.col(2).width = 8000
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 4300
    ws.col(6).width = 4000
    ws.col(7).width = 4300
    ws.col(8).width = 2000
    ws.col(9).width = 2000

    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'&F c. &P  '
    ws.footer_str = b' '
    ws.start_page_number = 1



    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 26


    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Calibri'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Calibri'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 15 * 20
    style3.font.bold = True
    style3.font.name = 'Calibri'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Calibri'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 20 * 20
    style5.font.bold = True
    style5.font.name = 'Calibri'
    style5.alignment = al1
    style5.alignment.wrap = 1

    # for row_num in range(4):
    #     for col_num in range(8):
    #         ws.row(row_num).height_mismatch = True
    #         ws.row(row_num).height = 500

    row_num = 4
    columns = [
        'Регистрационная карточка на СИ и ИО'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        'Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 7
    columns = [
        'Внутренний номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        'Новый или б/у',
        'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 8
    columns = [
        note.equipment.exnumber,
        note.charakters.reestr,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        note.equipment.yearintoservice,
        note.equipment.new,
        note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 9
    columns = [
        'Расположение и комплектность'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 9)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 10
    columns = [
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Документы, комплектные принадлежности, программное обеспечение',
        'Ответственный за прибор',
        'Ответственный за прибор',
        'Расположение прибора',
        'Расположение прибора',
        'Расположение прибора',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 4, style2)
        ws.merge(row_num, row_num, 5, 6, style2)
        ws.merge(row_num, row_num, 7, 9, style2)

    row_num = 11
    columns = [
        'год появления',
        'наименование документа/комплектной принадлежности/ПО',
        'наименование документа/комплектной принадлежности/ПО',
        'откуда поступил документ/ принадлежность/ПО',
        'откуда поступил документ/ принадлежность/ПО',
        'дата',
        'ответственный, ФИО',
        'дата',
        'номер комнаты',
        'номер комнаты',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 2, style2)
        ws.merge(row_num, row_num, 3, 4, style2)
        ws.merge(row_num, row_num, 8, 9, style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    rows_1 = DocsCons.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'docs',
        'docs',
        'source',
        'source',
    )
    rows_2 = Personchange.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'person__username',
    )

    rows_3 = Roomschange.objects.filter(equipment=note.equipment). \
        values_list(
        'date',
        'roomnumber__roomnumber',
    )


    for row in rows_1:
        row_num += 1
        for col_num in range(5):
            ws.write(row_num, col_num, row[col_num], style1)
            ws.merge(row_num, row_num, 1, 2, style2)
            ws.merge(row_num, row_num, 3, 4, style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    a = row_num

    row_num = 11
    for row in rows_2:
        row_num += 1
        for col_num in range(5, 7):
            ws.write(row_num, col_num, row[col_num - 5], style4)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    b = row_num


    row_num = 11
    for row in rows_3:
        row_num += 1
        for col_num in range(7, 9):
            ws.write(row_num, col_num, row[col_num - 7], style4)
            ws.merge(row_num, row_num, 8, 9, style4)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500
    c = row_num

    d = max(a, b, c)


    row_num = 24
    columns = [
        'Данные верификации о соответствии оборудования  установленным требованиям подтверждаются сведениями о поверке'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 9, style2)

    ws1 = wb.add_sheet('Данные о ремонте и поверке', cell_overwrite_ok=True)

    ws1.col(0).width = 1500
    ws1.col(1).width = 7000
    ws1.col(2).width = 1000
    ws1.col(3).width = 2400
    ws1.col(4).width = 2000
    ws1.col(5).width = 4000
    ws1.col(6).width = 14000
    ws1.col(7).width = 4000

    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws1.insert_bitmap('logo.bmp', 0, 0)
    ws1.left_margin = 0

    ws1.header_str = b'&F c. &P  '
    ws1.footer_str = b' '
    ws1.start_page_number = 2

    row_num = 4
    columns = [
        'Особенности работы прибора',
        'Особенности работы прибора',
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
        note.equipment.individuality,
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 0, 1, style2)
    for col_num in range(2, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style1)
        ws1.merge(row_num, row_num, 2, 7, style1)
    ws1.row(row_num).height_mismatch = True
    ws1.row(row_num).height = 2000


    row_num = 6
    columns = [
        'Поверка',
        'Поверка',
        '',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
        'Техническое обслуживание и данные о повреждениях, неисправностях, модификациях и ремонте',
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 0, 1, style2)
    for col_num in range(3, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 3, 7, style2)

    row_num = 7
    columns = [
        'Год',
        'Сведения о результатах поверки',
        '',
        'Дата',
        'Описание',
        'Описание',
        'Описание',
        'ФИО исполнителя',
    ]
    for col_num in range(2):
        ws1.write(row_num, col_num, columns[col_num], style2)
    for col_num in range(3, len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style2)
        ws1.merge(row_num, row_num, 4, 6, style2)


    rows_1 = Verificationequipment.objects.filter(equipmentSM__equipment=note.equipment). \
        annotate(ver=Concat(
        Value('Свидетельство о поверке: \n  '),
        'certnumber',
        Value('\n от '), str('date'),
         Value('\n до '), str('datedead'),
        Value('\n выдано '),
        'verificator__companyName', output_field=CharField(),),
    ). \
        annotate(ver_year=Concat(
        'date__year', 'year',
         output_field=CharField(), ),
    ). \
        values_list(
        'ver_year',
        'ver',
    )

    rows_2 = CommentsEquipment.objects.filter(forNote=note.equipment). \
        values_list(
        'date',
        'note',
        'note',
        'note',
        'author',
    )

    for row in rows_1:
        row_num += 1
        for col_num in range(0, 1):
            ws1.write(row_num, col_num, row[col_num], style4)
        for col_num in range(1, 2):
            ws1.write(row_num, col_num, row[col_num], style4)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1500

    row_num = 7
    for row in rows_2:
        row_num += 1
        for col_num in range(3, 8):
            ws1.write(row_num, col_num, row[col_num - 3], style4)
            ws1.merge(row_num, row_num, 4, 6, style1)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1500

    wb.save(response)
    return response

# стили для exel (для этикеток)
brd1 = Borders()
brd1.left = 1
brd1.right = 1
brd1.top = 1
brd1.bottom = 1

al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_BOTTOM

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

def export_verificlabel_xls(request):
    '''представление для выгрузки этикеток для указания поверки'''
    note = []

    for n in (request.GET['n1'], request.GET['n2'],
              request.GET['n3'], request.GET['n4'],
              request.GET['n5'], request.GET['n6'],
              request.GET['n7'], request.GET['n8'],
              request.GET['n9'], request.GET['n10'],
              request.GET['n11'], request.GET['n12'],
              request.GET['n13'], request.GET['n14']):
        try:
            MeasurEquipment.objects.get(equipment__exnumber=n)
            note.append(MeasurEquipment.objects.get(equipment__exnumber=n))
        except:
            pass
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="verification_labels.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('1', cell_overwrite_ok=True)
    ws.header_str = b' '
    ws.footer_str = b' '

    # ширина столбцов
    ws.col(0).width = 300
    ws.col(1).width = 3400
    ws.col(2).width = 3600
    ws.col(3).width = 2000
    ws.col(4).width = 2000
    ws.col(5).width = 800
    ws.col(6).width = 3400
    ws.col(7).width = 3600
    ws.col(8).width = 2000
    ws.col(9).width = 2000
    ws.col(10).width = 300


    i = 0
    j = 0
    if len(note) % 2 != 0:
        note.append(note[0])
    while i <= len(note) - 2:
        currentnote1 = note[i]
        currentnote2 = note[i + 1]

        row_num = 0 + j
        columns = [
            '',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            f'{currentnote1.charakters.name} {currentnote1.charakters.typename}/{currentnote1.charakters.modificname}',
            '',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            f'{currentnote2.charakters.name} {currentnote2.charakters.typename}/{currentnote2.charakters.modificname}',
            '',
        ]

        for col_num in (1, 2, 3, 4, 6, 7, 8, 9):
            ws.write(row_num, col_num, columns[col_num], style2)
            ws.merge(row_num, row_num, 1, 4, style2)
            ws.merge(row_num, row_num, 6, 9, style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 750

        row_num = 1 + j
        columns = [
            '',
            f'Заводской №:',
            f'{currentnote1.equipment.lot}',
            f'Внут. №',
            f'{currentnote1.equipment.exnumber}',
            '',
            f'Заводской №:',
            f'{currentnote2.equipment.lot}',
            f'Внут. №',
            f'{currentnote2.equipment.exnumber}',
            '',
        ]

        for col_num in (1, 3, 6, 8):
            ws.write(row_num, col_num, columns[col_num], style1)
        for col_num in (2, 4, 7, 9):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 270

        row_num = 2 + j
        columns = [
            '',
            f'Св-во поверки:',
            f'{currentnote1.newcertnumber}',
            f'{currentnote1.newcertnumber}',
            f'{currentnote1.newcertnumber}',
            '',
            f'Св-во поверки:',
            f'{currentnote2.newcertnumber}',
            f'{currentnote2.newcertnumber}',
            f'{currentnote2.newcertnumber}',
            '',
        ]

        for col_num in (1, 6):
            ws.write(row_num, col_num, columns[col_num], style1)
        for col_num in range(2, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(7, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 2, 4, style2)
        ws.merge(row_num, row_num, 7, 9, style2)

        row_num = 3 + j
        columns = [
            '',
            f'поверен от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'поверен от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'поверен от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'поверен от {currentnote1.newdate} до {currentnote1.newdatedead}',
            ' ',
            f'поверен от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'поверен от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'поверен от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'поверен от {currentnote2.newdate} до {currentnote2.newdatedead}',
            ' ',
            ]
        for col_num in range(1, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(6, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 4, style1)
        ws.merge(row_num, row_num, 6, 9, style1)

        row_num = 4 + j
        columns = [
            '',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            ' ',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            f'Ответственный за поверку {"              "} А.Б.Головкина',
            ' ',
        ]
        for col_num in range(1, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(6, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 4, style1)
        ws.merge(row_num, row_num, 6, 9, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 400

        row_num = 5 + j
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 370

        i += 2
        j += 6


    wb.save(response)
    return response

