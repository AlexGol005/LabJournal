import http

import xlwt
import pytils.translit
from datetime import timedelta, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpRequest
from datetime import datetime, timedelta
from django.db.models import Max, Q, Value, CharField, Count, Sum
from django.db.models.functions import Upper, Concat, Extract, ExtractYear
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import request
from django.views import View
from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView
from xlwt import Alignment, Borders

from equipment.constants import servicedesc0
from equipment.forms import*
from equipment.models import*
from metods import get_dateformat
from users.models import Profile

URL = 'equipment'
now = date.today()

class ContactsVerregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации контактов поверителей"""
    form_class = ContactsVerForm
    template_name = 'equipment/personverreg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(ContactsVerregView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить контакт поверителя'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            order = form.save(commit=False)
            order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
            order.save()
            if order.equipment.kategory == 'СИ':
                return redirect(f'/equipment/measureequipment/verification/{self.kwargs["str"]}')
            if order.equipment.kategory == 'ИО':
                return redirect(f'/equipment/testingequipment/attestation/{self.kwargs["str"]}')


# флаг1
class SearchMustVerView(ListView):
    """ выводит список СИ у которых дата заказа поверки совпадает с указанной либо раньше неё"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.filter(haveorder=False).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(dateorder__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(id__in=set1).filter(equipment__status='Э')
        return queryset

class SearchNotVerView(ListView):
    """ выводит список СИ у которых дата окончания поверки совпадает с указанной либо раньше неё"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchNotVerView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(datedead__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(id__in=set1).exclude(equipment__status='С')
        return queryset


class LastNewEquipmentView(ListView):
    """ выводит список 10 приборов, которые были добавлены последними"""

    template_name = URL + '/equipmentlist.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(LastNewEquipmentView, self).get_context_data(**kwargs)
        context['URL'] = URL
        return context

    def get_queryset(self):
        Total = Equipment.objects.count()
        queryset = Equipment.objects.filter()[Total-10:Total]
        return queryset


class SearchMustOrderView(ListView):
    """ выводит список СИ у которых месяц заказа поверки совпадает с указанным либо раньше него"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['charakters_name']

    def get_context_data(self, **kwargs):
        context = super(SearchMustOrderView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = SearchMEForm()
        return context

    def get_queryset(self):
        serdate = self.request.GET['date']
        queryset_get = Verificationequipment.objects.filter(haveorder=False).\
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        queryset_get1 = Verificationequipment.objects.filter(id__in=set).\
            filter(dateordernew__lte=serdate).values('equipmentSM__id')
        b = list(queryset_get1)
        set1 = []
        for i in b:
            a = i.get('equipmentSM__id')
            set1.append(a)
        queryset = MeasurEquipment.objects.filter(id__in=set1).filter(equipment__status='Э')
        return queryset


class MeteorologicalParametersView(TemplateView):
    """ Представление, которое выводит формы для метеопараметров """
    template_name = URL + '/meteo.html'





class VerdoneView(ListView):
    """ выводит список СИ у которых год поверки совпадает с годом указанным в форме и поверку заказывала Петроаналитика"""

    template_name = URL + '/measureequipment.html'
    context_object_name = 'objects'
    ordering = ['newdate']

    def get_context_data(self, **kwargs):
        context = super(VerdoneView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = YearForm()
        return context

    def get_queryset(self):
        needyear = self.request.GET['date']
        queryset = MeasurEquipment.objects.filter(newdate__contains=needyear)
        return queryset


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class MetrologicalEnsuringView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    """выводит заглавную страницу для метрологического обеспечения """
    template_name = URL + '/metro.html'
    success_message = "Раздел для ответственного за метрологию"

    def get_context_data(self, **kwargs):
        context = super(MetrologicalEnsuringView, self).get_context_data(**kwargs)
        context['form'] = DateForm()
        return context

class ReportsView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    """ Представление, которое выводит страницу с кнопками для вывода планов и отчётов по оборудованию"""
    template_name = URL + '/reports.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        context['URL'] = URL
        context['form'] = YearForm()
        return context



class VerificationLabelsView(TemplateView):
    """выводит форму для ввода внутренних номеров для распечатки этикеток о метрологическом обслуживании приборов """
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
        context['dopin'] = 'equipment/measurequipmentcharacterslist'
        return context
    
@login_required
def MeasurEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о госреестре"""
    if request.method == "POST":
        form = MeasurEquipmentCharaktersCreateForm(request.POST,  instance=MeasurEquipmentCharakters.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('measurequipmentcharacterslist')
    else:
        form = MeasurEquipmentCharaktersCreateForm(instance=MeasurEquipmentCharakters.objects.get(pk=str))
    data = {'form': form,
            }
    return render(request, 'equipment/reg.html', data)


class TestingEquipmentCharaktersRegView(SuccessMessageMixin, CreateView):
    """ выводит форму внесения характеристик ИО. """
    template_name = URL + '/reg.html'
    form_class = TestingEquipmentCharaktersCreateForm
    success_url = '/equipment/testingequipmentcharacterslist/'
    success_message = "Характеристики ИО успешно добавлены"

    def get_context_data(self, **kwargs):
        context = super(TestingEquipmentCharaktersRegView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить характеристики ИО'
        context['dopin'] = 'equipment/testingequipmentcharacterslist'
        return context

@login_required
def TestingEquipmentCharaktersUpdateView(request, str):
    """выводит форму для обновления данных о характеристиках ИО"""
    if request.method == "POST":
        form = TestingEquipmentCharaktersCreateForm(request.POST,  instance=TestingEquipmentCharakters.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('testingequipmentcharacterslist')
    else:
        form = TestingEquipmentCharaktersCreateForm(instance=TestingEquipmentCharakters.objects.get(pk=str))
    data = {'form': form,
            }
    return render(request, 'equipment/reg.html', data)


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


class HelpingequipmentregView(LoginRequiredMixin, CreateView):
    """ выводит форму регистрации ВО на основе ЛО и характеристик ВО """
    form_class = HelpingEquipmentCreateForm
    template_name = 'equipment/reg.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Equipment, exnumber=self.kwargs['str'])

    def get_context_data(self, **kwargs):
        context = super(HelpingequipmentregView, self).get_context_data(**kwargs)
        context['title'] = 'Зарегистрировать ВО'
        context['dop'] = Equipment.objects.get(exnumber=self.kwargs['str'])
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.equipment = Equipment.objects.get(exnumber=self.kwargs['str'])
                order.save()
                return redirect(f'/equipment/helpequipment/{self.kwargs["str"]}')
        else:
            messages.success(request, f'Регистрировать может только ответственный за метрологическое обеспечение приборов')
            return redirect(reverse('helpequipmentreg', kwargs={'str': self.kwargs['str']}))



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
    template_name = 'equipment/verpersonlist.html'
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
    """ Представление, которое выводит результаты поиска по списку госреестров """

    template_name = URL + '/measurequipmentcharacterslist.html'

    def get_context_data(self, **kwargs):
        context = super(ReestrsearresView, self).get_context_data(**kwargs)
        name = self.request.GET['name']
        reestr = self.request.GET['reestr']
        if self.request.GET['name']:
            name1 = self.request.GET['name'][0].upper() + self.request.GET['name'][1:]
        reestr = self.request.GET['reestr']
        if name and not reestr:
            objects = MeasurEquipmentCharakters.objects.\
            filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        if reestr and not name:
            objects = MeasurEquipmentCharakters.objects.filter(reestr__icontains=reestr)
            context['objects'] = objects
        if reestr and  name:
            objects = MeasurEquipmentCharakters.objects.filter(reestr__icontains=reestr).\
                filter(Q(name__icontains=name)|Q(name__icontains=name1)).order_by('name')
            context['objects'] = objects
        context['form'] = Searchreestrform(initial={'name': name, 'reestr': reestr})
        context['URL'] = URL
        return context


class ChromatoView(TemplateView):
    """ Представление, которое выводит список принадлежностей для хроматографа """
    template_name = URL + '/chromato.html'


class MeasurEquipmentView(ListView):
    """Выводит список средств измерений"""
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


class HaveorderVerView(UpdateView):
    """ выводит форму добавления инфо о заказе поверки """
    template_name = 'equipment/reg.html'
    form_class = OrderMEUdateForm

    def get_object(self, queryset=None):
        queryset_get = Verificationequipment.objects. \
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        q = Verificationequipment.objects.filter(id__in=set). \
            get(equipmentSM_id=self.kwargs['pk'])
        return q

    def get_context_data(self, **kwargs):
        context = super(HaveorderVerView, self).get_context_data(**kwargs)
        context['title'] = "Заказана поверка или новое СИ"
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            order = form.save(commit=False)
            order.save()
            return redirect(f"/equipment/measureequipmentall/")
        else:
            return redirect(f"/equipment/measureequipmentall/")


class HaveorderAttView(UpdateView):
    """ выводит форму добавления инфо о заказе поверки """
    template_name = 'equipment/reg.html'
    form_class = OrderMEUdateForm

    def get_object(self, queryset=None):
        queryset_get = Attestationequipment.objects. \
            select_related('equipmentSM').values('equipmentSM'). \
            annotate(id_actual=Max('id')).values('id_actual')
        b = list(queryset_get)
        set = []
        for i in b:
            a = i.get('id_actual')
            set.append(a)
        q = Attestationequipment.objects.filter(id__in=set). \
            get(equipmentSM_id=self.kwargs['pk'])
        return q


    def get_context_data(self, **kwargs):
        context = super(HaveorderAttView, self).get_context_data(**kwargs)
        context['title'] = "Заказана аттестация или новое ИО"
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser:
            order = form.save(commit=False)
            order.save()
            return redirect(f"/equipment/testingequipmentall/")
        else:
            return redirect(f"/equipment/testingequipmentall/")


class StrMeasurEquipmentView(View):
    """ выводит отдельную страницу СИ """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        obj = get_object_or_404(MeasurEquipment, equipment__exnumber=str)
        context = {
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
                if title.kategory == 'СИ':
                    return redirect(reverse('measureequipment', kwargs={'str': str}))
                if title.kategory == 'ИО':
                    return redirect(reverse('testequipment', kwargs={'str': str}))
                if title.kategory == 'ВО':
                    return redirect(reverse('supequipment', kwargs={'str': str}))
    if person != request.user and not request.user.is_superuser:
        messages.success(request, f' Для внесения записей о приборе нажмите на кнопку ниже:'
                                  f' "Внести запись о приборе и смотреть записи (для всех пользователей)"'
                                  f'. Добавить особенности работы или поменять статус может только ответственный '
                                  f'за прибор или поверку.')

        if title.kategory == 'СИ':
            return redirect(reverse('measureequipment', kwargs={'str': str}))
        if title.kategory == 'ИО':
            return redirect(reverse('testequipment', kwargs={'str': str}))
        if title.kategory == 'ВО':
            return redirect(reverse('supequipment', kwargs={'str': str}))
    else:
        form = EquipmentUpdateForm(instance=Equipment.objects.get(exnumber=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/individuality.html', data)


def EquipmentMetrologyUpdate(request, str):
    """выводит форму для обновления постоянных особенностей поверки"""
    title = Equipment.objects.get(exnumber=str)
    try:
        get_pk = title.personchange_set.latest('pk').pk
        person = Personchange.objects.get(pk=get_pk).person
    except:
        person = 1

    if person == request.user or request.user.is_superuser:
        if request.method == "POST":
            form = MetrologyUpdateForm(request.POST, instance=Equipment.objects.get(exnumber=str))
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                if title.kategory == 'СИ':
                    return redirect(reverse('measureequipmentver', kwargs={'str': str}))
                if title.kategory == 'ИО':
                    return redirect(reverse('testingequipmentatt', kwargs={'str': str}))
    if person != request.user and not request.user.is_superuser:
        messages.success(request, f'. поменять статус может только ответственный за поверку.')
        return redirect(reverse('measureequipmentver', kwargs={'str': str}))
    else:
        form = MetrologyUpdateForm(instance=Equipment.objects.get(exnumber=str))
    data = {'form': form, 'title': title
            }
    return render(request, 'equipment/metrologyindividuality.html', data)


def VerificatorUpdate(request, str):
    """выводит форму для обновления данных о сотруднике поверителе"""
    if request.method == "POST":
        form = VerificatorPersonCreationForm(request.POST,  instance=VerificatorPerson.objects.get(pk=str))
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            return redirect('verificatorpersons')
    else:
        form = VerificatorPersonCreationForm(instance=VerificatorPerson.objects.get(pk=str))
    data = {'form': form,
            }
    return render(request, 'equipment/personverreg.html', data)


class VerificationequipmentView(View):
    """ выводит историю поверок и форму для добавления комментария к истории поверок """
    def get(self, request, str):
        note = Verificationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        note2 = ContactsVer.objects.filter(equipment__exnumber=str).order_by('-pk')
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
                'note2': note2,
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


class AttestationequipmentView(View):
    """ выводит историю аттестаций и форму для добавления комментария к истории аттестаций """
    def get(self, request, str):
        note = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).order_by('-pk')
        note2 = ContactsVer.objects.filter(equipment__exnumber=str).order_by('-pk')
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
            dateorder = Attestationequipment.objects.filter(equipmentSM__equipment__exnumber=str).last().dateorder
        except:
            dateorder = 'не аттестован'
        now = date.today()
        try:
            comment = CommentsAttestationequipment.objects.filter(forNote__exnumber=str).last().note
        except:
            comment = ''
        form = CommentsAttestationequipmentForm(initial={'comment': comment})
        data = {'note': note,
                'note2': note2,
                'title': title,
                'calinterval': calinterval,
                'now': now,
                'dateorder': dateorder,
                'form': form,
                'comment': comment,
                'strreg': strreg,
                }
        return render(request, 'equipment/attestation.html', data)

    def post(self, request, str, *args, **kwargs):
        form = CommentsAttestationequipmentForm(request.POST)
        if request.user.is_superuser:
            if form.is_valid():
                order = form.save(commit=False)
                order.author = request.user
                order.forNote = Equipment.objects.get(exnumber=str)
                order.save()
                return redirect(order)
        else:
            messages.success(request, f'Комментировать может только ответственный за поверку приборов')
            return redirect(reverse('testingequipmentattestation', kwargs={'str': str}))


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
def AttestationReg(request, str):
    """выводит форму для внесения сведений об аттестации"""
    title = Equipment.objects.get(exnumber=str)
    if request.user.is_superuser:
        if request.method == "POST":
            form = AttestationRegForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.equipmentSM = TestingEquipment.objects.get(equipment__exnumber=str)
                order.save()
                return redirect(order)
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(reverse('testingequipmentatt', kwargs={'str': str}))
    else:
        form = AttestationRegForm()
    data = {
        'form': form,
        'title': title
            }
    return render(request, 'equipment/attestationreg.html', data)

# флаг регистрация внесение нового оборудования
@login_required
def EquipmentReg(request):
    """выводит форму для регистрации  ЛО"""
    if request.user.is_superuser:
        if request.method == "POST":
            form = EquipmentCreateForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                if order.kategory == 'ВО':
                    try:
                        x = str(order.exnumber) + 'В'
                        a = Equipment.objects.filter(kategory='ВО').\
                            filter(exnumber__contains=x).last().exnumber
                        b = int(str(a)[-3::]) + 1
                        c = str(b).rjust(3, '0')
                        d = str(order.exnumber) + 'В' + c
                        order.exnumber = d
                    except:
                        order.exnumber = str(order.exnumber) + 'В001'
                if order.kategory == 'ИО' or order.kategory == 'СИ':
                    try:
                        a = Equipment.objects.exclude(kategory='ВО').\
                            filter(exnumber__startswith=order.exnumber).last().exnumber
                        b = int(str(a)[-3::]) + 1
                        c = str(b).rjust(3, '0')
                        d = str(order.exnumber) + c
                        order.exnumber = d
                    except:
                        order.exnumber = str(order.exnumber) + '001'
                order.yearintoservice = now.year
                order.save()
                if order.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipmentreg/{order.exnumber}/')
                if order.kategory == 'ИО':
                    return redirect(f'/equipment/testequipmentreg/{order.exnumber}/')
                if order.kategory == 'ВО':
                    return redirect(f'/equipment/helpequipmentreg/{order.exnumber}/')
                else:
                    return redirect('equipmentlist')
    if not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только инженеру по оборудованию')
        return redirect(f'/equipment/')
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
                if order.equipment.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipment/{str}')
                if order.equipment.kategory == 'ИО':
                    return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')

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
                if order.equipment.kategory == 'СИ':
                    return redirect(f'/equipment/measureequipment/{str}')
                if order.equipment.kategory == 'ИО':
                    return redirect(f'/equipment/testequipment/{self.kwargs["str"]}')
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
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
                order_by('charakters__name')
            context['objects'] = objects
        if dateser and name and not lot and not exnumber:
            objects = TestingEquipment.objects.\
                filter(Q(equipmentSM_att__datedead__gte=dateser) & Q(equipmentSM_att__id__in=set)). \
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

# блок выгрузок данных в формате ексель


# запросы к БД для выгрузо списков СИ
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

get_id_attestation = Attestationequipment.objects.select_related('equipmentSM').values('equipmentSM'). \
    annotate(id_actual=Max('id')).values('id_actual')
list_ = list(get_id_attestation)
setatt = []
for n in list_:
    setatt.append(n.get('id_actual'))

# get_id_comver = CommentsVerificationequipment.objects.select_related('forNote').values('forNote'). \
#     annotate(id_actual=Max('id')).values('id_actual')
# list_ = list(get_id_comver)
# setcomver = []
# for n in list_:
#     setcomver.append(n.get('id_actual'))
# setcomver = setcomver.append(None)

# флаг2


# флаг график поверки и аттестации
def export_me_xls(request):
    '''представление для выгрузки графика поверки и аттестации'''
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="pov_att_shedule_{now.year}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('График поверки СИ', cell_overwrite_ok=True)
    ws1 = wb.add_sheet('График аттестации ИО', cell_overwrite_ok=True)

    # ширина столбцов графика поверки
    ws.col(1).width = 3000
    ws.col(2).width = 3000
    ws.col(3).width = 4500
    ws.col(4).width = 3000
    ws.col(5).width = 4200
    ws.col(9).width = 4200
    ws.col(10).width = 3000
    ws.col(11).width = 4200
    ws.col(13).width = 4200
    ws.col(14).width = 4200
    ws.col(15).width = 3000
    ws.col(16).width = 3000
    ws.col(17).width = 3000
    ws.col(18).width = 3000
    ws.col(21).width = 6500
    ws.col(22).width = 6500
    ws.col(23).width = 9000

    # ширина столбцов графика аттестации
    ws1.col(1).width = 3000
    ws1.col(2).width = 4500
    ws1.col(3).width = 3500
    ws1.col(4).width = 4200
    ws1.col(8).width = 4200
    ws1.col(9).width = 4200
    ws1.col(10).width = 4200
    ws1.col(12).width = 4200
    ws1.col(13).width = 3000
    ws1.col(14).width = 3000
    ws1.col(15).width = 3000
    ws1.col(18).width = 8500
    ws1.col(19).width = 6500
    ws1.col(20).width = 6500
    ws1.col(21).width = 9000

    # стили
    al10 = Alignment()
    al10.horz = Alignment.HORZ_CENTER
    al10.vert = Alignment.VERT_CENTER
    al10.wrap = 1

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.top = 1
    b1.bottom = 1

    style10 = xlwt.XFStyle()
    style10.font.bold = True
    style10.font.name = 'Times New Roman'
    style10.borders = b1
    style10.alignment = al10

    style100 = xlwt.XFStyle()
    style100.font.bold = True
    style100.font.name = 'Times New Roman'
    style100.alignment = al10

    style20 = xlwt.XFStyle()
    style20.font.name = 'Times New Roman'
    style20.borders = b1
    style20.alignment = al10

    style30 = xlwt.XFStyle()
    style30.font.name = 'Times New Roman'
    style30.borders = b1
    style30.alignment = al10
    style30.num_format_str = 'DD.MM.YYYY'

    # название графика поверки, первый ряд
    row_num = 1
    columns = [
        f'График поверки средств измерений на {now.year} год'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style100)
        ws.merge(row_num, row_num, 0, 15, style100)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 600


    # заголовки графика поверки, первый ряд
    row_num += 2
    columns = [
                '№ п/п',
                'Внутренний  номер',
                'Номер в госреестре',
                'Наименование СИ, заводской номер',
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
                'Номер свидетельства',
                'Дата поверки/калибровки',
                'Дата окончания свидетельства',
                'Дата заказа поверки/калибровки',
                'Дата заказа замены',
                'Периодичность поверки /калибровки',
                'Инвентарный номер',
                'Диапазон измерений',
                'Метрологические характеристики',
                'Дополнительная информация/\nвыписка из текущих сведений о поверке',
                'Протокол верификации да/нет',
                'Использование для образцов из ОА да/нет',
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)

    rows = MeasurEquipment.objects.all().\
        annotate(big_name=Concat('charakters__name', Value(' '),'charakters__typename', Value(' '), 'charakters__modificname', \
         Value(', зав. № '), 'equipment__lot'),
                 mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
    manuf_country=Concat('equipment__manufacturer__country', Value(', '), 'equipment__manufacturer__companyName')).\
        filter(equipment__roomschange__in=setroom).\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__in=setver).\
        exclude(equipment__status='С').\
        values_list(
            'equipment__exnumber',
            'charakters__reestr',
            'big_name',
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
            'equipmentSM_ver__certnumber',
            'equipmentSM_ver__date',
            'equipmentSM_ver__datedead',
            'equipmentSM_ver__dateorder',
            'equipmentSM_ver__dateordernew',
            'charakters__calinterval',
            'equipment__invnumber',
            'charakters__measurydiapason',
            'charakters__accuracity',
            'equipmentSM_ver__extra',
            'equipment__protocol',
            'equipment__accreditation',
        )

    for row in rows:
        row_num += 1
        for col_num in range(0, 14):
            ws.write(row_num, col_num + 1, row[col_num], style20)
        for col_num in range(14, 18):
            ws.write(row_num, col_num + 1, row[col_num], style30)
        for col_num in range(18, 19):
            c = row[col_num]
            if c == 24:
                c = '24 месяца'
            else:
                c = f'{c} месяцев'

            ws.write(row_num, col_num + 1, f'{c}', style20)
        for col_num in range(19, 23):
            ws.write(row_num, col_num + 1, row[col_num], style20)
        for col_num in range(23, len(row)):
            b = row[col_num]
            if not b:
                b = 'нет'
            else:
                b = 'да'
            ws.write(row_num, col_num + 1, f'{b}', style20)
    a = row_num
    for col_num in range(1):
        for row_num in range(4, a + 1):
            ws.write(row_num, col_num, f'{row_num - 3}', style20)


        # название графика аттестации, первый ряд
    row_num = 1
    columns = [
        f'График аттестации испытательного оборудования на {now.year} год'
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style100)
        ws1.merge(row_num, row_num, 0, 15, style100)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 600

        # заголовки графика аттестации, первый ряд
    row_num += 2
    columns = [
        '№ п/п',
        'Внутренний  номер',
        'Наименование ИО, заводской номер',
        'Тип/Модификация',
        'Заводской номер',
        'Год выпуска',
        'Новый или б/у',
        'Год ввода в эксплуатацию',
        'Страна, наименование производителя',
        'Место установки или хранения',
        'Ответственный за ИО',
        'Статус',
        'Номер аттестата',
        'Дата аттестации',
        'Дата окончания аттестации',
        'Дата заказа аттестации',
        'Периодичность аттестации',
        'Инвентарный номер',
        'Аттестован на методики',
        'Основные технические характеристики',
        'Наименование видов испытаний',
        'Дополнительная информация/\nвыписка из текущего аттестата',
        'Протокол верификации да/нет',
        'Использование для образцов из ОА да/нет',
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style10)

    rows = TestingEquipment.objects.all(). \
        annotate(big_name=Concat('charakters__name', Value(' '),'charakters__typename', Value(' '), 'charakters__modificname', \
         Value(', зав. № '), 'equipment__lot'),
        mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        exclude(equipment__status='С'). \
        values_list(
        'equipment__exnumber',
        'big_name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'equipment__new',
        'equipment__yearintoservice',
        'manuf_country',
        'equipment__roomschange__roomnumber__roomnumber',
        'equipment__personchange__person__username',
        'equipment__status',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead',
        'equipmentSM_att__dateorder',
        'charakters__calinterval',
        'equipment__invnumber',
        'equipmentSM_att__ndocs',
        'charakters__measurydiapason',
        'charakters__aim',
        'equipmentSM_att__extra',
        'equipment__protocol',
        'equipment__accreditation',
    )
    for row in rows:
        row_num += 1
        for col_num in range(0, 12):
            ws1.write(row_num, col_num + 1, row[col_num], style20)
        for col_num in range(12, 15):
            ws1.write(row_num, col_num + 1, row[col_num], style30)
        for col_num in range(15, 16):
            c = row[col_num]
            if c == 24:
                c = '24 месяца'
            else:
                c = f'{c} месяцев'

            ws1.write(row_num, col_num + 1, f'{c}', style20)
        for col_num in range(16, 21):
            ws1.write(row_num, col_num + 1, row[col_num], style20)
        for col_num in range(21, len(row)):
            b = row[col_num]
            if not b:
                b = 'нет'
            else:
                b = 'да'
            ws1.write(row_num, col_num + 1, f'{b}', style20)
    a = row_num
    for col_num in range(1):
        for row_num in range(4, a + 1):
            ws1.write(row_num, col_num, f'{row_num - 3}', style20)

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
        'Соответствие оборудования  установленным требованиям подтверждается протоколом верификации'
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

# флаг карточки на ИО
def export_tecard_xls(request, pk):
    '''представление для выгрузки карточки на прибор (ИО) в ексель'''
    note = TestingEquipment.objects.get(pk=pk)
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
        'Наименование',
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
        ws.merge(row_num, row_num, 1, 2, style2)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num = 8
    columns = [
        note.equipment.exnumber,
        note.charakters.name,
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
        ws.merge(row_num, row_num, 1, 2, style1)
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
        'Соответствие оборудования  установленным требованиям подтверждается протоколом верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 0, 9, style2)

    ws1 = wb.add_sheet('Данные о ремонте и аттестации', cell_overwrite_ok=True)

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
        'Сведения о результатах аттестации',
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


    rows_1 = Attestationequipment.objects.filter(equipmentSM__equipment=note.equipment). \
        annotate(ver=Concat(
        Value('Аттестат: \n  '),
        'certnumber',
        Value('\n от '), str('date'),
         Value('\n до '), str('datedead'),
        Value('\n выдан '),
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

# флаг этикетки СИ
def export_verificlabel_xls(request):
    '''представление для выгрузки этикеток для указания поверки и аттестации'''
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
        try:
            TestingEquipment.objects.get(equipment__exnumber=n)
            note.append(TestingEquipment.objects.get(equipment__exnumber=n))
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

        if currentnote1.equipment.kategory == 'СИ':
            a = 'поверка:'
        if currentnote1.equipment.kategory == 'ИО':
            a = 'аттестация:'
        if currentnote2.equipment.kategory == 'СИ':
            b = 'поверка:'
        if currentnote2.equipment.kategory == 'ИО':
            b = 'аттестация:'

        row_num = 2 + j
        columns = [
            '',
            f'{a}',
            f'{currentnote1.newcertnumber}',
            f'{currentnote1.newcertnumber}',
            f'{currentnote1.newcertnumber}',
            '',
            f'{b}',
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

        if currentnote1.equipment.kategory == 'СИ':
            a = 'поверен'
        if currentnote1.equipment.kategory == 'ИО':
            a = 'аттестован'
        if currentnote2.equipment.kategory == 'СИ':
            b = 'поверен'
        if currentnote2.equipment.kategory == 'ИО':
            b = 'аттестован'

        row_num = 3 + j
        columns = [
            '',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            f'{a} от {currentnote1.newdate} до {currentnote1.newdatedead}',
            ' ',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            f'{b} от {currentnote2.newdate} до {currentnote2.newdatedead}',
            ' ',
            ]
        for col_num in range(1, 5):
            ws.write(row_num, col_num, columns[col_num], style2)
        for col_num in range(6, 10):
            ws.write(row_num, col_num, columns[col_num], style2)
        ws.merge(row_num, row_num, 1, 4, style1)
        ws.merge(row_num, row_num, 6, 9, style1)

        if currentnote1.equipment.kategory == 'СИ':
            a = 'поверку'
        if currentnote1.equipment.kategory == 'ИО':
            a = 'аттест-ю:'
        if currentnote2.equipment.kategory == 'СИ':
            b = 'поверку'
        if currentnote2.equipment.kategory == 'ИО':
            b = 'аттест-ю'

        row_num = 4 + j
        columns = [
            '',
            f'Ответственный за {a} {"              "} М.В.Петров',
            f'Ответственный за {a} {"              "} М.В.Петров',
            f'Ответственный за {a} {"              "} М.В.Петров',
            f'Ответственный за {a} {"              "} М.В.Петров',
            ' ',
            f'Ответственный за {b} {"              "} М.В.Петров',
            f'Ответственный за {b} {"              "} М.В.Петров',
            f'Ответственный за {b} {"              "} М.В.Петров',
            f'Ответственный за {b} {"              "} М.В.Петров',
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

# флаг верифик
def export_exvercard_xls(request, pk):
    '''представление для выгрузки протокола верификации СИ в ексель'''
    note = MeasurEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    # aa = MeasurEquipment.objects.all().filter(equipment__roomschange__in=setroom). \
    #     values_list('equipment__roomschange__roomnumber__roomnumber').get(pk=pk)
    # aa = Roomschange.objects.all().filter(equipment=100). \
    #     values_list('equipment__roomschange__roomnumber__roomnumber').get(pk=pk)
    # aa = str(aa)
    # room = aa[2:-3]
    #
    # bb = MeasurEquipment.objects.all().filter(equipment__personchange__in=setperson). \
    #     values_list('equipment__personchange__person__username').get(pk=pk)
    # bb = str(bb)
    # usere = bb[2:-3]
    room = '1'
    try:
        room = Roomschange.objects.filter(equipment__exnumber=note.equipment.exnumber)
        room = room.last().roomnumber
    except:
        room = 'не указано'
    # try:
    usere = Personchange.objects.filter(equipment__exnumber=note.equipment.exnumber)
    # usere = usere.last().person.name
    usere = usere.last().person
    position = usere.last().person
    usere = str(usere)
    # except:
    #     usere = 'не указано'
    userelat = pytils.translit.translify(usere)
    # positionset = Profile.objects.get(user__username=usere)
    # position = positionset.userposition
    position = '3'
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    filename = f"{userelat}_{cardname}"
    filename = str(filename)
    filename = filename[:251]

    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    # response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x0D

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Протокол верификации СИ', cell_overwrite_ok=True)

    ws.col(0).width = 2600
    ws.col(1).width = 2500
    ws.col(2).width = 7900
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 2400
    ws.col(6).width = 3600


    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws.start_page_number = 1

    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    b5 = Borders()
    b5.left = 5
    b5.right = 5
    b5.bottom = 5
    b5.top = 5

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Times new roman'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style10 = xlwt.XFStyle()
    style10.font.height = 12 * 20
    style10.font.name = 'Times new roman'
    style10.alignment = al1
    style10.alignment.wrap = 1

    style110 = xlwt.XFStyle()
    style110.font.height = 12 * 20
    style110.font.name = 'Times new roman'
    style110.alignment = al1
    style110.alignment.wrap = 1
    style110.pattern = pattern

    style11 = xlwt.XFStyle()
    style11.font.height = 9 * 20
    style11.font.name = 'Times new roman'
    style11.alignment = al1
    style11.alignment.wrap = 1
    style11.borders = b1
    style11.pattern = pattern

    style111 = xlwt.XFStyle()
    style111.font.height = 12 * 20
    style111.font.name = 'Times new roman'
    style111.alignment = al1
    style111.alignment.wrap = 1
    style111.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Times new roman'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 11 * 20
    style3.font.bold = True
    style3.font.name = 'Times new roman'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Times new roman'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 12 * 20
    style5.font.bold = True
    style5.font.name = 'Times new roman'
    style5.alignment = al1
    style5.alignment.wrap = 1

    dateverificformat = now
    dateverific = get_dateformat(now)
    row_num = 4
    columns = [
        f'Протокол верификации № {note.equipment.exnumber}_01/22 от {dateverific} г. СИ вн.№ {note.equipment.exnumber}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        '1. Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=2
    columns = [
        'Внутренний номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        # 'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        # 'Новый или б/у',
        # 'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100


    row_num +=1
    columns = [
        f'СИ {note.equipment.exnumber}',
        note.charakters.reestr,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        # note.equipment.yearintoservice,
        # note.equipment.new,
        # note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num += 2
    columns = [
        'Диапазон измерений',
        'Диапазон измерений',
        'Диапазон измерений',
        'Класс точности, погрешность и/или неопределённость',
        'Класс точности, погрешность и/или неопределённость',
        'Класс точности, погрешность и/или неопределённость',
        'Класс точности, погрешность и/или неопределённость',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        note.charakters.measurydiapason,
        note.charakters.measurydiapason,
        note.charakters.measurydiapason,
        note.charakters.accuracity,
        note.charakters.accuracity,
        note.charakters.accuracity,
        note.charakters.accuracity,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 3, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num +=2
    columns = [
        '2. Верификация комплектности и установки оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '2.1 Соответствие комплектности'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        'Наименование',
        'Наименование',
        'Наименование',
        'Оценка',
        'Примечание',
        'Примечание',
        'Примечание',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.complectlist != '':
        a = note.charakters.complectlist
        st = style1
    else:
        a = 'упаковочный лист'
        st = style11


    row_num += 1
    columns = [
        'Комплектация',
        'Комплектация',
        'Комплектация',
        'cоответствует',
        a,
        a,
        a,
    ]
    for col_num in range(4):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    b = note.equipment.exnumber

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(docs__icontains='аспорт')
        d = d[0]
        a = 'в наличии'
    except:
        a = 'отсутствует'


    row_num +=1
    columns = [
        'Паспорт',
        'Паспорт',
        'Паспорт',
        a,
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(Q(docs__icontains='уководство')|Q(docs__icontains='нструкция')|Q(docs__icontains='ИНСТРУКЦИЯ')|Q(docs__icontains='аспорт'))
        d = d[0]
        a = 'в наличии'
        e = ''
    except:
        a = 'отсутствует'
        e = 'необходимо разработать инструкцию на оборудование'

    row_num += 1
    columns = [
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        a,
        e,
        e,
        e,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Сведения о поверке',
        'Сведения о поверке',
        'Сведения о поверке',
        f'поверен до {note.newdatedead}',
        f'№ {note.newcertnumber}',
        f'№ {note.newcertnumber}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    try:
        microclimat = MeteorologicalParameters.objects.get(roomnumber__roomnumber=room, date=dateverificformat)
        facttemperature = microclimat.temperature
        facthumid = microclimat.humidity
        factpress = microclimat.pressure
    except:
        facttemperature = 'указать'
        facthumid = 'указать'
        factpress = 'указать'




    row_num +=2
    columns = [
        f'2.2 Соответствие  требованиям к условиям эксплуатации в помещении № {room}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Наименование характеристики',
        'Наименование характеристики',
        'Требования руководства по эксплуатации, паспорта или описания типа',
        'Состояние на момент верификации',
        'Состояние на момент верификации',
        'Оценка',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 1, style1)
        ws.merge(row_num, row_num, 3, 4, style1)
        ws.merge(row_num, row_num, 5, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.power == True:
        row_num += 1
        columns = [
            'Соответствие требованиям к  электропитанию'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style1)
            ws.merge(row_num, row_num, 0, 6, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.voltage == '':
            note.charakters.voltage = '-'
            st = style11
        else:
            st = style1



        row_num += 1
        columns = [
            'Напряжение питания сети, В',
            'Напряжение питания сети, В',
            note.charakters.voltage,
            '220',
            '220',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.frequency == '':
            note.charakters.frequency = '-'
            st = style11
        else:
            st = style1

        row_num += 1
        columns = [
            'Частота, Гц',
            'Частота, Гц',
            note.charakters.frequency,
            '50',
            '50',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Соответствие требованиям к  микроклимату'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.temperature == '':
        note.charakters.temperature = '-'
        st1 = style11
    else:
        st1 = style1
    if facttemperature == 'указать':
        st3 = style11
    else:
        st3 = style1


    row_num += 1
    columns = [
        'Диапазон рабочих температур, °С',
        'Диапазон рабочих температур, °С',
        note.charakters.temperature,
        facttemperature,
        facttemperature,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.humidicity == '':
        note.charakters.humidicity = '-'
        st1 = style11
    else:
        st1 = style1
    if facthumid == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Относительная влажность воздуха, %',
        'Относительная влажность воздуха, %',
        note.charakters.humidicity,
        facthumid,
        facthumid,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.pressure == '':
        note.charakters.pressure = '-'
        st1 = style11
    else:
        st1 = style1

    if factpress == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Атмосферное давление, кПа',
        'Атмосферное давление, кПа',
        note.charakters.pressure,
        factpress,
        factpress,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '2.3 Соответствие  установки на рабочем месте требованиям документации на оборудование'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.needsetplace:
        a = ''
        b = '✓'
    if not note.charakters.needsetplace:
        a = '✓'
        b = ''


    row_num += 1
    columns = [
        a,
        'Установка не требуется'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700


    row_num += 1
    columns = [
        b,
        'Требуется установка'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    if note.charakters.needsetplace:
        if not note.charakters.setplace:
            st = style11
        else:
            st = style1


        row_num += 2
        columns = [
            'Описание установки'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style3)
            ws.merge(row_num, row_num, 0, 6)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


        row_num += 1
        columns = [
              note.charakters.setplace
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500



    row_num += 2
    columns = [
        '3. Тестирование при внедрении оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.expresstest:
        a = ''
        b = '✓'
    if not note.charakters.expresstest:
        a = '✓'
        b = ''

    row_num += 1
    columns = [
        a,
        'Тестирование невозможно'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        b,
        'Тестирование возможно. Результаты испытаний в приложении 1'

    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 2
    columns = [
        '4. Заключение по результатам верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    row_num += 1
    columns = [
        f'Пригодно к эксплуатации.  Требования к установке и условиям окружающей среды соответствуют документации на оборудование.\
        \n Закреплено за помещением № {room}.\n Закреплено за ответственным пользователем: {usere}.'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num += 2
    columns = [
        '',
        '',
        'Верификацию провел:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':
        st = style10
    else:
        st = style10

    row_num += 2
    columns = [
        '',
        '',
        position,
        '',
       usere,
       usere,
       usere,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'Согласовано:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'начальник производства'
        '',
        '',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'заведующий АХЧ'
        '',
        '',
        'А.В.Теленков',
        'А.В.Теленков',
        'А.В.Теленков',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':

        row_num += 2
        columns = [
            '',
            '',
            'инженер по качеству'
            '',
            '',
            'М.В.Петров',
            'М.В.Петров',
            'М.В.Петров',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style10)
            ws.merge(row_num, row_num, 4, 6, style10)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


    wb.save(response)
    return response

# флаг верификация ио
def export_exvercardteste_xls(request, pk):
    '''представление для выгрузки протокола верификации ИО в ексель'''
    note = TestingEquipment.objects.get(pk=pk)
    company = CompanyCard.objects.get(pk=1)
    aa = TestingEquipment.objects.all().filter(equipment__roomschange__in=setroom). \
        values_list('equipment__roomschange__roomnumber__roomnumber').get(pk=pk)
    aa = str(aa)
    room = aa[2:-3]

    bb = TestingEquipment.objects.all().filter(equipment__personchange__in=setperson). \
        values_list('equipment__personchange__person__username').get(pk=pk)
    bb = str(bb)
    usere = bb[2:-3]
    userelat = pytils.translit.translify(usere)
    positionset = Profile.objects.get(user__username=usere)
    position = positionset.userposition
    cardname = pytils.translit.translify(note.equipment.exnumber) + ' ' + pytils.translit.translify(note.equipment.lot)
    response = HttpResponse(content_type='application/ms-excel')
    filename = f"{userelat}_{cardname}"
    filename = str(filename)
    filename = filename[:251]

    response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'
    # response['Content-Disposition'] = f'attachment; filename="{cardname}.xls"'
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 0x0D

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Протокол верификации ИО', cell_overwrite_ok=True)

    ws.col(0).width = 2600
    ws.col(1).width = 2500
    ws.col(2).width = 7900
    ws.col(3).width = 3700
    ws.col(4).width = 2500
    ws.col(5).width = 2400
    ws.col(6).width = 3600


    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws.start_page_number = 1

    al1 = Alignment()
    al1.horz = Alignment.HORZ_CENTER
    al1.vert = Alignment.VERT_CENTER

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.bottom = 1
    b1.top = 1

    b5 = Borders()
    b5.left = 5
    b5.right = 5
    b5.bottom = 5
    b5.top = 5

    style1 = xlwt.XFStyle()
    style1.font.height = 9 * 20
    style1.font.name = 'Times new roman'
    style1.alignment = al1
    style1.alignment.wrap = 1
    style1.borders = b1

    style10 = xlwt.XFStyle()
    style10.font.height = 12 * 20
    style10.font.name = 'Times new roman'
    style10.alignment = al1
    style10.alignment.wrap = 1

    style110 = xlwt.XFStyle()
    style110.font.height = 12 * 20
    style110.font.name = 'Times new roman'
    style110.alignment = al1
    style110.alignment.wrap = 1
    style110.pattern = pattern

    style11 = xlwt.XFStyle()
    style11.font.height = 9 * 20
    style11.font.name = 'Times new roman'
    style11.alignment = al1
    style11.alignment.wrap = 1
    style11.borders = b1
    style11.pattern = pattern

    style111 = xlwt.XFStyle()
    style111.font.height = 12 * 20
    style111.font.name = 'Times new roman'
    style111.alignment = al1
    style111.alignment.wrap = 1
    style111.borders = b1

    style2 = xlwt.XFStyle()
    style2.font.height = 9 * 20
    style2.font.name = 'Times new roman'
    style2.alignment = al1
    style2.alignment.wrap = 1
    style2.borders = b1
    style2.pattern = pattern

    style3 = xlwt.XFStyle()
    style3.font.height = 11 * 20
    style3.font.bold = True
    style3.font.name = 'Times new roman'
    style3.alignment = al1
    style3.alignment.wrap = 1

    style4 = xlwt.XFStyle()
    style4.font.height = 9 * 20
    style4.font.name = 'Times new roman'
    style4.alignment = al1
    style4.alignment.wrap = 1
    style4.borders = b1
    style4.num_format_str = 'DD.MM.YYYY'

    style5 = xlwt.XFStyle()
    style5.font.height = 12 * 20
    style5.font.bold = True
    style5.font.name = 'Times new roman'
    style5.alignment = al1
    style5.alignment.wrap = 1

    dateverificformat = now
    dateverific = get_dateformat(now)
    row_num = 4
    columns = [
        f'Протокол верификации № {note.equipment.exnumber}_01/22 от {dateverific} г. ИО вн.№ {note.equipment.exnumber}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style5)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num = 5
    columns = [
        '1. Идентификационная и уникальная информация'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=2
    columns = [
        'Внутренний номер',
        'Наименование',
        'Наименование',
        'Тип/модификация',
        'Заводской номер',
        'Год выпуска',
        'Производитель',
        # 'Год ввода в эксплуатацию в ООО "Петроаналитика" ',
        # 'Новый или б/у',
        # 'Инвентарный номер',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 2, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100


    row_num +=1
    columns = [
        f'СИ {note.equipment.exnumber}',
        note.charakters.name,
        note.charakters.name,
        f'{note.charakters.typename}/{note.charakters.modificname}',
        note.equipment.lot,
        note.equipment.yearmanuf,
        f'{note.equipment.manufacturer.country}, {note.equipment.manufacturer.companyName}',
        # note.equipment.yearintoservice,
        # note.equipment.new,
        # note.equipment.invnumber,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 2, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1100

    row_num += 2
    columns = [
        'Основные технические характеристики',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        note.charakters.measurydiapason,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1700

    row_num +=2
    columns = [
        '2. Верификация комплектности и установки оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '2.1 Соответствие комплектности'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        'Наименование',
        'Наименование',
        'Наименование',
        'Оценка',
        'Примечание',
        'Примечание',
        'Примечание',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.complectlist != '':
        a = note.charakters.complectlist
        st = style1
    else:
        a = 'упаковочный лист'
        st = style11


    row_num += 1
    columns = [
        'Комплектация',
        'Комплектация',
        'Комплектация',
        'cоответствует',
        a,
        a,
        a,
    ]
    for col_num in range(4):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    b = note.equipment.exnumber

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(docs__icontains='аспорт')
        d = d[0]
        a = 'в наличии'
    except:
        a = 'отсутствует'


    row_num +=1
    columns = [
        'Паспорт',
        'Паспорт',
        'Паспорт',
        a,
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    try:
        c = DocsCons.objects.filter(equipment__exnumber=b)
        d = c.filter(Q(docs__icontains='уководство')|Q(docs__icontains='нструкция')|Q(docs__icontains='ИНСТРУКЦИЯ')|Q(docs__icontains='аспорт'))
        d = d[0]
        a = 'в наличии'
        e = ''
    except:
        a = 'отсутствует'
        e = 'необходимо разработать инструкцию на оборудование'

    row_num += 1
    columns = [
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        'Руководство по эксплуатации',
        a,
        e,
        e,
        e,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Сведения об аттестации',
        'Сведения об аттестации',
        'Сведения об аттестации',
        f'аттестован до {note.newdatedead}',
        f'№ {note.newcertnumber}',
        f'№ {note.newcertnumber}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 2, style1)
        ws.merge(row_num, row_num, 4, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    try:
        microclimat = MeteorologicalParameters.objects.get(roomnumber__roomnumber=room, date=dateverificformat)
        facttemperature = microclimat.temperature
        facthumid = microclimat.humidity
        factpress = microclimat.pressure
    except:
        facttemperature = 'указать'
        facthumid = 'указать'
        factpress = 'указать'




    row_num +=2
    columns = [
        f'2.2 Соответствие  требованиям к условиям эксплуатации в помещении № {room}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Наименование характеристики',
        'Наименование характеристики',
        'Требования руководства по эксплуатации, паспорта или описания типа',
        'Состояние на момент верификации',
        'Состояние на момент верификации',
        'Оценка',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 1, style1)
        ws.merge(row_num, row_num, 3, 4, style1)
        ws.merge(row_num, row_num, 5, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.power == True:
        row_num += 1
        columns = [
            'Соответствие требованиям к  электропитанию'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style1)
            ws.merge(row_num, row_num, 0, 6, style1)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.voltage == '':
            note.charakters.voltage = '-'
            st = style11
        else:
            st = style1



        row_num += 1
        columns = [
            'Напряжение питания сети, В',
            'Напряжение питания сети, В',
            note.charakters.voltage,
            '220',
            '220',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

        if note.charakters.frequency == '':
            note.charakters.frequency = '-'
            st = style11
        else:
            st = style1

        row_num += 1
        columns = [
            'Частота, Гц',
            'Частота, Гц',
            note.charakters.frequency,
            '50',
            '50',
            'соответствует',
        ]
        for col_num in range(3):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 1, st)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 3, 4, st)
            ws.merge(row_num, row_num, 5, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500

    row_num += 1
    columns = [
        'Соответствие требованиям к  микроклимату'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.temperature == '':
        note.charakters.temperature = '-'
        st1 = style11
    else:
        st1 = style1
    if facttemperature == 'указать':
        st3 = style11
    else:
        st3 = style1


    row_num += 1
    columns = [
        'Диапазон рабочих температур, °С',
        'Диапазон рабочих температур, °С',
        note.charakters.temperature,
        facttemperature,
        facttemperature,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.humidicity == '':
        note.charakters.humidicity = '-'
        st1 = style11
    else:
        st1 = style1
    if facthumid == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Относительная влажность воздуха, %',
        'Относительная влажность воздуха, %',
        note.charakters.humidicity,
        facthumid,
        facthumid,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.pressure == '':
        note.charakters.pressure = '-'
        st1 = style11
    else:
        st1 = style1

    if factpress == 'указать':
        st3 = style11
    else:
        st3 = style1

    row_num += 1
    columns = [
        'Атмосферное давление, кПа',
        'Атмосферное давление, кПа',
        note.charakters.pressure,
        factpress,
        factpress,
        'соответствует',
    ]
    for col_num in range(3):
        ws.write(row_num, col_num, columns[col_num], st1)
        ws.merge(row_num, row_num, 0, 1, st1)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], st3)
        ws.merge(row_num, row_num, 3, 4, st3)
        ws.merge(row_num, row_num, 5, 6, st3)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '2.3 Соответствие  установки на рабочем месте требованиям документации на оборудование'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.needsetplace:
        a = ''
        b = '✓'
    if not note.charakters.needsetplace:
        a = '✓'
        b = ''


    row_num += 1
    columns = [
        a,
        'Установка не требуется'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700


    row_num += 1
    columns = [
        b,
        'Требуется установка'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    if note.charakters.needsetplace:
        if not note.charakters.setplace:
            st = style11
        else:
            st = style1


        row_num += 2
        columns = [
            'Описание установки'
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style3)
            ws.merge(row_num, row_num, 0, 6)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


        row_num += 1
        columns = [
              note.charakters.setplace
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], st)
            ws.merge(row_num, row_num, 0, 6, st)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500



    row_num += 2
    columns = [
        '3. Тестирование при внедрении оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if note.charakters.expresstest:
        a = ''
        b = '✓'
    if not note.charakters.expresstest:
        a = '✓'
        b = ''

    row_num += 1
    columns = [
        a,
        'Тестирование невозможно'
    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 1
    columns = [
        b,
        'Тестирование возможно. Результаты испытаний в приложении 1'

    ]
    for col_num in range(0, 1):
        ws.write(row_num, col_num, columns[col_num], style111)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 1, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num += 2
    columns = [
        '4. Заключение по результатам верификации'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style3)
        ws.merge(row_num, row_num, 0, 6)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500


    row_num += 1
    columns = [
        f'Пригодно к эксплуатации.  Требования к установке и условиям окружающей среды соответствуют документации на оборудование.\
        \n Закреплено за помещением № {room}.\n Закреплено за ответственным пользователем: {usere}.'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style1)
        ws.merge(row_num, row_num, 0, 6, style1)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 1500

    row_num += 2
    columns = [
        '',
        '',
        'Верификацию провел:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':
        st = style10
    else:
        st = style10

    row_num += 2
    columns = [
        '',
        '',
        position,
        '',
       usere,
       usere,
       usere,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], st)
        ws.merge(row_num, row_num, 4, 6, st)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'Согласовано:'
        '',
        '',
        '',
        '',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'начальник производства'
        '',
        '',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
        'Н.Ю.Пилявская',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num += 2
    columns = [
        '',
        '',
        'заведующий АХЧ'
        '',
        '',
        'А.В.Теленков',
        'А.В.Теленков',
        'А.В.Теленков',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)
        ws.merge(row_num, row_num, 4, 6, style10)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    if usere != 'А.Б.Головкина':

        row_num += 2
        columns = [
            '',
            '',
            'инженер-химик 2 категории'
            '',
            '',
            'А.Б.Головкина',
            'А.Б.Головкина',
            'А.Б.Головкина',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style10)
            ws.merge(row_num, row_num, 4, 6, style10)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 500


    wb.save(response)
    return response

# флаг ексели отчёты и планы по приборам
# Набор вьюшек для выгрузки планов и отчетов по оборудованию в exel
# Так как планы и отчеты имеют сходную структуру. Они разделены на страницы для СИ, ИО, ВО,
# а также на помесячные суммы, то
# вначале идет общая базовая  функция.
# В ней объединено все общее для всех планов и отчетов. Базовая функция  выполняется в индивидуальных функциях


def base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE):
    """базовое шаблон представление для выгрузки планов и отчетов по СИ, ИО, ВО к которому обращаются частные представления"""

    # для выгрузки реквизитов организации
    company = CompanyCard.objects.get(pk=1)
    affirmation = f'УТВЕРЖДАЮ \n{company.positionboss}\n{company.name}\n____________/{company.nameboss}/\n«__» ________20__ г.'

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{exel_file_name}.xls"'

    serdate = request.GET['date']
    # стили
    al10 = Alignment()
    al10.horz = Alignment.HORZ_CENTER
    al10.vert = Alignment.VERT_CENTER
    al10.wrap = 1

    b1 = Borders()
    b1.left = 1
    b1.right = 1
    b1.top = 1
    b1.bottom = 1

    # заголовки жирным шрифтом, с границами ячеек
    style_headers = xlwt.XFStyle()
    style_headers.font.bold = True
    style_headers.font.name = 'Times New Roman'
    style_headers.borders = b1
    style_headers.alignment = al10

    # обычные ячейки, с границами ячеек
    style_plain = xlwt.XFStyle()
    style_plain.font.name = 'Times New Roman'
    style_plain.borders = b1
    style_plain.alignment = al10

    # обычные ячейки с датами, с границами ячеек
    style_date = xlwt.XFStyle()
    style_date.font.name = 'Times New Roman'
    style_date.borders = b1
    style_date.alignment = al10
    style_date.num_format_str = 'DD.MM.YYYY'


    # добавляем книгу и страницы
    wb = xlwt.Workbook(encoding='utf-8')
    ws1 = wb.add_sheet(f'{str1}', cell_overwrite_ok=True)
    ws2 = wb.add_sheet(f'{str2}', cell_overwrite_ok=True)
    ws3 = wb.add_sheet(f'{str3}', cell_overwrite_ok=True)
    ws4 = wb.add_sheet(f'{str4}', cell_overwrite_ok=True)
    ws5 = wb.add_sheet(f'{str5}', cell_overwrite_ok=True)
    ws6 = wb.add_sheet(f'{str6}', cell_overwrite_ok=True)

    # убираем колонтитулы
    ws1.header_str = b' '
    ws1.footer_str = b' '
    ws2.header_str = b' '
    ws2.footer_str = b' '
    ws3.header_str = b' '
    ws3.footer_str = b' '
    ws4.header_str = b' '
    ws4.footer_str = b' '
    ws5.header_str = b' '
    ws5.footer_str = b' '
    ws6.header_str = b' '
    ws6.footer_str = b' '

    # ширина столбцов СИ
    ws1.col(0).width = 2500
    ws1.col(1).width = 2500
    ws1.col(2).width = 4500
    ws1.col(3).width = 4500
    ws1.col(4).width = 2500
    ws1.col(6).width = 2500
    ws1.col(7).width = 4500
    ws1.col(7).width = 7500
    ws1.col(8).width = 7500
    ws1.col(9).width = 7500
    ws1.col(10).width = 7500
    ws1.col(11).width = 7500
    ws1.col(12).width = 7500
    ws1.col(13).width = 7500
    ws1.col(14).width = 7500
    ws1.col(15).width = 7500

    # ширина столбцов ИО
    ws2.col(0).width = 2500
    ws2.col(1).width = 2500
    ws2.col(2).width = 4500
    ws2.col(3).width = 4500
    ws2.col(4).width = 2500
    ws2.col(5).width = 4500
    ws2.col(6).width = 2500
    ws2.col(7).width = 4500
    ws2.col(8).width = 7500
    ws2.col(9).width = 7500
    ws2.col(10).width = 7500
    ws2.col(11).width = 7500
    ws2.col(12).width = 7500
    ws2.col(13).width = 7500
    ws2.col(14).width = 7500
    ws2.col(15).width = 7500

    # ширина столбцов ВО
    ws3.col(0).width = 2500
    ws3.col(1).width = 2500
    ws3.col(2).width = 4500
    ws3.col(3).width = 4500
    ws3.col(4).width = 2500
    ws3.col(5).width = 4500
    ws3.col(6).width = 2500
    ws3.col(7).width = 4500
    ws3.col(8).width = 7500
    ws3.col(9).width = 7500
    ws3.col(11).width = 7500
    ws3.col(12).width = 7500
    ws3.col(13).width = 7500
    ws3.col(14).width = 7500
    ws3.col(15).width = 7500

    # колонки для разбиивок по месяцам
    columns_month = [
        'Месяц',
        'Количество единиц оборудования',
        'Сумма, руб',
    ]

    # заголовки СИ (вынесены сюда для подсчёта длины строк ексель)
    columnsME = [
        'Внутренний номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
    ]
    columnsME = columnsME + u_headers_me
    lennME = len(columnsME)

    # заголовки ИО (вынесены сюда для подсчёта длины строк ексель)
    columnsTE = [
        'Внутренний номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
    ]
    columnsTE = columnsTE + u_headers_te
    lennTE = len(columnsTE)

    # заголовки ВО (вынесены сюда для подсчёта длины строк ексель)
    columnsHE = [
        'Внутренний номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
    ]
    columnsHE = columnsHE + u_headers_he
    lennHE = len(columnsHE)

    # записываем страницу 1 - СИ
    row_num = 0
    c = [''] * (lennME - 3)
    columns = c + [
        affirmation,
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style_plain_nobor_r)
        ws1.merge(row_num, row_num, lennME - 3, lennME - 1, style_plain_nobor_r)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1900

    row_num += 2
    columns = [
        f'{nameME}'
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style_plain_nobor_bold)
        ws1.merge(row_num, row_num, 0, lennME-1, style_plain_nobor_bold)
        ws2.row(row_num).height_mismatch = True
        ws2.row(row_num).height = 800

    # заголовки СИ
    row_num += 2
    datecolumnme = []

    # запись заголовков СИ
    for col_num in range(len(columnsME)):
        ws1.write(row_num, col_num, columnsME[col_num], style_headers)
        if 'Дата' in str(columnsME[col_num]) or 'дата' in str(columnsME[col_num]):
            datecolumnme.append(col_num)

    # данные СИ и их запись
    rows = measure_e
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in datecolumnme:
                ws1.write(row_num, col_num, row[col_num], style_date)
            else:
                ws1.write(row_num, col_num, row[col_num], style_plain)

    # подпись СИ
    row_num += 2
    columns = [
        f'Разработал: \n{company.positionmetrologequipment} _____________ /{company.namemetrologequipment}/'
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style_plain_nobor_l)
        ws1.merge(row_num, row_num, 0, lennME-1, style_plain_nobor_l)
        ws1.row(row_num).height_mismatch = True
        ws1.row(row_num).height = 1000


    # записываем страницу 2 - ИО
    # Шапка утверждаю
    row_num = 0
    c = [''] * (lennTE - 2)
    columns = c + [
        affirmation,
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style_plain_nobor_r)
        ws2.merge(row_num, row_num, lennTE - 2, lennTE - 1, style_plain_nobor_r)
        ws2.row(row_num).height_mismatch = True
        ws2.row(row_num).height = 1900

    row_num += 2
    columns = [
        f'{nameTE}'
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style_plain_nobor_bold)
        ws2.merge(row_num, row_num, 0, lennTE-1, style_plain_nobor_bold)
        ws2.row(row_num).height_mismatch = True
        ws2.row(row_num).height = 800

    # заголовки ИО
    row_num += 2
    datecolumnte = []

    # запись заголовков ИО
    for col_num in range(len(columnsTE)):
        ws2.write(row_num, col_num, columnsTE[col_num], style_headers)
        if 'Дата' in str(columnsTE[col_num]) or 'дата' in str(columnsTE[col_num]):
            datecolumnte.append(col_num)

    # данные ИО и их запись
    rows = testing_e
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in datecolumnte:
                ws2.write(row_num, col_num, row[col_num], style_date)
            else:
                ws2.write(row_num, col_num, row[col_num], style_plain)

    # подпись ИО
    row_num += 2
    columns = [
        f'Разработал: \n{company.positionmetrologequipment} _____________ /{company.namemetrologequipment}/'
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style_plain_nobor_l)
        ws2.merge(row_num, row_num, 0, lennTE-1, style_plain_nobor_l)
        ws2.row(row_num).height_mismatch = True
        ws2.row(row_num).height = 1000

    # записываем страницу 3 - ВО
    row_num = 0
    c = [''] * (lennHE - 2)
    columns = c + [
        affirmation,
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style_plain_nobor_r)
        ws3.merge(row_num, row_num, lennHE - 2, lennHE - 1, style_plain_nobor_r)
        ws3.row(row_num).height_mismatch = True
        ws3.row(row_num).height = 1900

    row_num += 2
    columns = [
        f'{nameHE}'
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style_plain_nobor_bold)
        ws3.merge(row_num, row_num, 0, lennHE-1, style_plain_nobor_bold)
        ws3.row(row_num).height_mismatch = True
        ws3.row(row_num).height = 800

    # заголовки ВО
    row_num += 2
    datecolumnhe = []

    # запись заголовков ВО
    for col_num in range(len(columnsHE)):
        ws3.write(row_num, col_num, columnsHE[col_num], style_headers)
        if 'Дата' in str(columnsHE[col_num]) or 'дата' in str(columnsHE[col_num]):
            datecolumnhe.append(col_num)

    # данные ВО и их запись
    rows = helping_e
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num in datecolumnme:
                ws3.write(row_num, col_num, row[col_num], style_date)
            else:
                ws3.write(row_num, col_num, row[col_num], style_plain)

    # подпись ВО
    row_num += 2
    columns = [
        f'Разработал: \n{company.positionmetrologequipment} _____________ /{company.namemetrologequipment}/'
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style_plain_nobor_l)
        ws3.merge(row_num, row_num, 0, lennHE-1, style_plain_nobor_l)
        ws3.row(row_num).height_mismatch = True
        ws3.row(row_num).height = 1000


    # записываем страницу 4 - подсчёт по месяцам для СИ (ПСИ)
    # заголовки ПСИ
    row_num = 0

    # запись заголовков ПСИ
    for col_num in range(len(columns_month)):
        ws4.write(row_num, col_num, columns_month[col_num], style_headers)

    # данные ПСИ и их запись
    rows = measure_e_months
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws4.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 5 - подсчёт по месяцам для ИО (ПИО)
    # заголовки ПИО
    row_num = 0

    # запись заголовков ПИО
    for col_num in range(len(columns_month)):
        ws5.write(row_num, col_num, columns_month[col_num], style_headers)

    # данные ПИО и их запись
    rows = testing_e_months
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws5.write(row_num, col_num, row[col_num], style_plain)

    # записываем страницу 6 - подсчёт по месяцам для ВО (ПВО)
    # заголовки ПВО
    row_num = 0

    # запись заголовков ПВО
    for col_num in range(len(columns_month)):
        ws6.write(row_num, col_num, columns_month[col_num], style_headers)

    # данные ПВО и их запись
    rows = helping_e_months
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws6.write(row_num, col_num, row[col_num], style_plain)

    # все сохраняем
    wb.save(response)
    return response

# флаг отчёты по поверке
def export_metroyearcust_xls(request):
    """представление для выгрузки - Список СИ и ИО прошедших поверку в указанном году только те где организатор работ - Петроаналитика"""
    serdate = request.GET['date']
    exel_file_name = f'report_inner_metro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ - поверено единиц в месяц'
    str5 = 'ИО - аттестовано единиц в месяц'
    str6 = 6


    u_headers_me = ['Номер свидетельства',
                    'Дата поверки/калибровки',
                    'Дата окончания свидетельства',
                    'Стоимость поверки, руб.',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        exclude(equipmentSM_ver__cust=True). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
        'equipmentSM_ver__price',
    ).order_by('equipmentSM_ver__date')

    u_headers_te = ['Номер аттестата',
                    'Дата аттестации',
                    'Дата окончания аттестации',
                    'Стоимость аттестации, руб.',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        exclude(equipmentSM_att__cust=True). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead',
        'equipmentSM_att__price',
    ).order_by('equipmentSM_att__date')

    u_headers_he = []
    helping_e = []

    measure_e_months = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        filter(equipmentSM_ver__price__isnull=False). \
        exclude(equipmentSM_ver__cust=True). \
        values('equipmentSM_ver__date__month'). \
        annotate(dcount=Count('equipmentSM_ver__date__month'), s=Sum('equipmentSM_ver__price')). \
        order_by(). \
        values_list(
        'equipmentSM_ver__date__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        exclude(equipmentSM_att__cust=True). \
        values('equipmentSM_att__date__month'). \
        annotate(dcount1=Count('equipmentSM_att__date__month'), s1=Sum('equipmentSM_att__price')). \
        order_by(). \
        values_list(
        'equipmentSM_att__date__month',
        'dcount1',
        's1',
    )

    helping_e_months = []
    company = CompanyCard.objects.get(pk=1)
    nameME = f'Отчет по поверке средств измерений в {company.name} за {serdate} год'
    nameTE = f'Отчет по аттестации испытательного оборудования в {company.name} за {serdate} год'
    nameHE = ''

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE
                               )


def export_metroyearprice_xls(request):
    """представление для выгрузки - Список СИ и ИО прошедших поверку в указанном году только те где
    Список СИ и ИО прошедших поверку в указанном году только где указана стоимость"""
    serdate = request.GET['date']
    exel_file_name = f'report_all_withprice_metro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ - поверено единиц в месяц'
    str5 = 'ИО - аттестовано единиц в месяц'
    str6 = 6


    u_headers_me = ['Номер свидетельства',
                    'Дата поверки/калибровки',
                    'Дата окончания свидетельства',
                    'Стоимость поверки, руб.',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        filter(equipmentSM_ver__price__isnull=False). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
        'equipmentSM_ver__price',
    ).order_by('equipmentSM_ver__date')

    u_headers_te = ['Номер аттестата',
                    'Дата аттестации',
                    'Дата окончания аттестации',
                    'Стоимость аттестации, руб.',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead',
        'equipmentSM_att__price',
    ).order_by('equipmentSM_att__date')

    u_headers_he = []
    helping_e = []

    measure_e_months = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        filter(equipmentSM_ver__price__isnull=False).\
        values('equipmentSM_ver__date__month').\
        annotate(dcount=Count('equipmentSM_ver__date__month'), s=Sum('equipmentSM_ver__price')).\
        order_by().\
        values_list(
        'equipmentSM_ver__date__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        filter(equipmentSM_att__price__isnull=False). \
        values('equipmentSM_att__date__month'). \
        annotate(dcount1=Count('equipmentSM_att__date__month'), s1=Sum('equipmentSM_att__price')). \
        order_by(). \
        values_list(
        'equipmentSM_att__date__month',
        'dcount1',
        's1',
    )

    helping_e_months = []
    company = CompanyCard.objects.get(pk=1)
    nameME = f'Отчет по поверке средств измерений в {company.name} за {serdate} год'
    nameTE = f'Отчет по аттестации испытательного оборудования в {company.name} за {serdate} год'
    nameHE = ''

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE
                               )

def export_metroyear_xls(request):
    """представление для выгрузки -
    Список СИ и ИО прошедших поверку в указанном году все, и те где НЕ указана стоимость, и поверенные поставщиком"""
    serdate = request.GET['date']
    exel_file_name = f'report_all_metro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 4
    str5 = 5
    str6 = 6


    u_headers_me = ['Номер свидетельства',
                    'Дата поверки/калибровки',
                    'Дата окончания свидетельства',
                    'Стоимость поверки, руб.',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__date__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
        'equipmentSM_ver__price',
    ).order_by('equipmentSM_ver__date')

    u_headers_te = ['Номер аттестата',
                    'Дата аттестации',
                    'Дата окончания аттестации',
                    'Стоимость аттестации, руб.',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
        'equipmentSM_att__price',
    ).order_by('equipmentSM_att__date')

    u_headers_he = []
    helping_e = []

    measure_e_months = []

    testing_e_months = []

    helping_e_months = []
    company = CompanyCard.objects.get(pk=1)
    nameME = f'Отчет по поверке средств измерений в {company.name} за {serdate} год'
    nameTE = f'Отчет по аттестации испытательного оборудования в {company.name} за {serdate} год'
    nameHE = ''

    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE
                               )

# флаг отчёты по закупке
def export_metronewyear_xls(request):
    """представление для выгрузки -
    Список купленного (введенного в эксплуатацию) СИ и ИО в указанном году"""
    serdate = request.GET['date']
    exel_file_name = f'purchased_equipment_{serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 'ВО'
    str4 = 'Количество СИ в месяц'
    str5 = 'Количество ИО в месяц'
    str6 = 'Количество ВО в месяц'


    u_headers_me = ['Стоимость',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipment__yearintoservice=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__price',
    ).order_by('equipment__date')

    u_headers_te = ['Стоимость',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipment__yearintoservice=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__price',
    ).order_by('equipment__date')

    u_headers_he = ['Стоимость',]
    helping_e = HelpingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__yearintoservice=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__price',
    ).order_by('equipment__date')

    measure_e_months = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipment__yearintoservice=serdate). \
        values('equipment__date__month'). \
        annotate(dcount=Count('equipment__date__month'), s=Sum('equipment__price')). \
        order_by(). \
        values_list(
        'equipment__date__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipment__yearintoservice=serdate). \
        values('equipment__date__month'). \
        annotate(dcount1=Count('equipment__date__month'), s1=Sum('equipment__price')). \
        order_by(). \
        values_list(
        'equipment__date__month',
        'dcount1',
        's1',
    )

    helping_e_months = HelpingEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__yearintoservice=serdate). \
        values('equipment__date__month'). \
        annotate(dcount2=Count('equipment__date__month'), s2=Sum('equipment__price')). \
        order_by(). \
        values_list(
        'equipment__date__month',
        'dcount2',
        's2',
    )
    company = CompanyCard.objects.get(pk=1)
    nameME = f'Средства измерений введённые в эксплуатацию в {company.name} за {serdate} год'
    nameTE = f'Испытательное оборудование введенное в эксплуатацию в {company.name} за {serdate} год'
    nameHE = f'Вспомогательное оборудование введенное в эксплуатацию в {company.name} за {serdate} год'


    return base_planreport_xls(request, exel_file_name,
                        measure_e, testing_e, helping_e,
                       measure_e_months, testing_e_months, helping_e_months,
                        u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE
                               )
# флаг план по поверке
def export_planmetro_xls(request):
    """представление для выгрузки плана поверки и аттестации на указанный год"""
    serdate = request.GET['date']
    exel_file_name = f'planmetro {serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ-количество поверок в месяц'
    str5 = 'ИО-кол-во аттестаций в месяц'
    str6 = 6


    u_headers_me = ['Номер текущего свидетельства',
                    'Дата окончания поверки',
                    'Месяц заказа поверки',
                    'Стоимость последней поверки, руб. (при наличии)',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
                                filter(equipment__roomschange__in=setroom). \
                                filter(equipment__personchange__in=setperson). \
                                filter(equipmentSM_ver__in=setver). \
                                filter(equipmentSM_ver__dateorder__year=serdate). \
                                values_list(
                                'equipment__exnumber',
                                'charakters__reestr',
                                'charakters__name',
                                'mod_type',
                                'equipment__lot',
                                'equipmentSM_ver__certnumber',
                                'equipmentSM_ver__datedead',
                                'equipmentSM_ver__dateorder__month',
                                'equipmentSM_ver__price',
                            ).order_by('equipmentSM_ver__dateorder__month')

    u_headers_te = ['Номер текущего аттестата',
                    'Дата окончания аттестации',
                    'Месяц заказа аттестации',
                    'Стоимость последней аттестации, руб. (при наличии)',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__dateorder__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__datedead',
        'equipmentSM_att__dateorder__month',
        'equipmentSM_att__price',
    ).order_by('equipmentSM_att__dateorder__month')

    u_headers_he = []
    helping_e = []
    measure_e_months = MeasurEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__dateorder__year=serdate).\
        values('equipmentSM_ver__dateorder__month').\
        annotate(dcount=Count('equipmentSM_ver__dateorder__month'), s=Sum('equipmentSM_ver__price')). \
        order_by().\
        values_list(
        'equipmentSM_ver__dateorder__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_att__dateorder__year=serdate).\
        values('equipmentSM_att__dateorder__month').\
        annotate(dcount=Count('equipmentSM_att__dateorder__month'), s=Sum('equipmentSM_att__price')). \
        order_by().\
        values_list(
        'equipmentSM_att__dateorder__month',
        'dcount',
        's',
    )
    helping_e_months = []
    company = CompanyCard.objects.get(pk=1)
    nameME = f'План поверки средств измерений в {company.name} за {serdate} год'
    nameTE = f'План аттестации испытательного оборудования в {company.name} за {serdate} год'
    nameHE = ''

    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE
                               )

# флаг план закупки по поверке
def export_plan_purchaesing_xls(request):
    """представление для выгрузки плана закупки по поверке и аттестации на указанный год"""
    serdate = request.GET['date']
    exel_file_name = f'plan_purchaesing_{serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 'СИ-количество в месяц'
    str5 = 'ИО-кол-во в месяц'
    str6 = 6


    u_headers_me = ['Номер текущего свидетельства',
                    'Месяц заказа замены',
                    'Стоимость оборудования',
                    ]

    measure_e = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
                                filter(equipment__roomschange__in=setroom). \
                                filter(equipment__personchange__in=setperson). \
                                filter(equipmentSM_ver__dateordernew__year=serdate). \
                                filter(equipmentSM_ver__haveorder=False). \
                                values_list(
                                'equipment__exnumber',
                                'charakters__reestr',
                                'charakters__name',
                                'mod_type',
                                'equipment__lot',
                                'equipmentSM_ver__certnumber',
                                'equipmentSM_ver__dateordernew__month',
                                'equipment__price',
                            ).order_by('equipmentSM_ver__dateordernew__month')

    u_headers_te = ['Номер текущего аттестата',
                    'Месяц заказа замены',
                    'Стоимость оборудования',
                    ]

    testing_e = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__personchange__in=setperson). \
        filter(equipmentSM_att__dateordernew__year=serdate). \
        filter(equipmentSM_att__haveorder=False). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__dateordernew__month',
        'equipment__price',
    ).order_by('equipmentSM_att__dateordernew__month')

    u_headers_he = []
    helping_e = []
    measure_e_months = MeasurEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_ver__dateordernew__year=serdate). \
        filter(equipmentSM_ver__haveorder=False). \
        values('equipmentSM_ver__dateordernew__month').\
        annotate(dcount=Count('equipmentSM_ver__dateordernew__month'), s=Sum('equipment__price')). \
        order_by().\
        values_list(
        'equipmentSM_ver__dateordernew__month',
        'dcount',
        's',
    )

    testing_e_months = TestingEquipment.objects.\
        filter(equipment__personchange__in=setperson).\
        filter(equipmentSM_att__dateordernew__year=serdate).\
        values('equipmentSM_att__dateordernew__month').\
        annotate(dcount=Count('equipmentSM_att__dateordernew__month'), s=Sum('equipment__price')). \
        filter(equipmentSM_att__haveorder=False). \
        order_by().\
        values_list(
        'equipmentSM_att__dateordernew__month',
        'dcount',
        's',
    )
    helping_e_months = []
    company = CompanyCard.objects.get(pk=1)
    nameME = f'Средства измерений - план закупки в {company.name} за {serdate} год'
    nameTE = f'Испытательное оборудование - план закупки в {company.name} за {serdate} год'
    nameHE = f'Вспомогательное оборудование - план закупки в {company.name} за {serdate} год'

    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE
                               )


def export_mustver_xls(request):
    """представление для выгрузки СИ требующих поверки и ИО требующих аттестации"""
    # выборка из ексель по поиску по дате
    serdate = request.GET['date']
    exel_file_name = f'mustveratt_{serdate}'
    str1 = 'СИ'
    str2 = 'ИО'
    str3 = 3
    str4 = 4
    str5 = 5
    str6 = 6

    queryset_get = Verificationequipment.objects.filter(haveorder=False). \
        select_related('equipmentSM').values('equipmentSM'). \
        annotate(id_actual=Max('id')).values('id_actual')
    b = list(queryset_get)
    set = []
    for i in b:
        a = i.get('id_actual')
        set.append(a)
    queryset_get1 = Verificationequipment.objects.filter(id__in=set). \
        filter(dateorder__lte=serdate).values('equipmentSM__id')
    b = list(queryset_get1)
    set1 = []
    for i in b:
        a = i.get('equipmentSM__id')
        set1.append(a)

    queryset_get0 = Attestationequipment.objects.filter(haveorder=False). \
        select_related('equipmentSM').values('equipmentSM'). \
        annotate(id_actual=Max('id')).values('id_actual')
    b = list(queryset_get0)
    set10 = []
    for i in b:
        a = i.get('id_actual')
        set10.append(a)
    queryset_get10 = Attestationequipment.objects.filter(id__in=set10). \
        filter(dateorder__lte=serdate).values('equipmentSM__id')
    b = list(queryset_get10)
    set10 = []
    for i in b:
        a = i.get('equipmentSM__id')
        set10.append(a)

    u_headers_me = [
                    'Год выпуска',
                    'Место хранения',
                    'Место поверки (предыдущей)',
                    'Сотрудник, ответственный за подготовку к поверке/аттестации',
                    'Постоянное примечание к поверке',
                    'Выписка из последних сведений о поверке',
                    ]

    measure_e = MeasurEquipment.objects.filter(id__in=set1). \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__status='Э'). \
        filter(equipmentSM_ver__in=setver). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'equipment__roomschange__roomnumber__roomnumber',
        'equipmentSM_ver__place',
        'equipment__personchange__person__username',
        'equipment__notemetrology',
        'equipmentSM_ver__extra',
    ).order_by('-equipmentSM_ver__place')

    u_headers_te = [
                    'Год выпуска',
                    'Место хранения',
                    'Место аттестации (предыдущей)',
                    'Сотрудник, ответственный за подготовку к поверке/аттестации',
                    'Постоянное примечание к аттестации',
                    'Выписка из последнего аттестата',
                    ]

    testing_e = TestingEquipment.objects.filter(id__in=set10). \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipment__status='Э'). \
        filter(equipmentSM_att__in=setatt). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipment__yearmanuf',
        'equipment__roomschange__roomnumber__roomnumber',
        'equipmentSM_att__place',
        'equipment__personchange__person__username',
        'equipment__notemetrology',
        'equipmentSM_att__extra'
    ).order_by('-equipmentSM_att__place')

    measure_e_months = []
    helping_e = []
    helping_e_months = []
    testing_e_months = []
    u_headers_he = []
    nameME = f'Средства измерений - требуется поверка  на {serdate}'
    nameTE = f'Испытательное оборудование - требуется аттестация на {serdate}'
    nameHE = ''


    return base_planreport_xls(request, exel_file_name,
                               measure_e, testing_e, helping_e,
                               measure_e_months, testing_e_months, helping_e_months,
                               u_headers_me, u_headers_te, u_headers_he,
                               str1, str2, str3, str4, str5, str6, nameME, nameTE, nameHE,
                               )

# Ниже будут быгрузки ексель для переноса в LabBook
# Поэтому: для удобства стили все далаем заново. В лаббуке стили с такими же названиями вынесены в файл exelbase
# но! кроме размера шрифта - он 11!

# блок стилей
al100 = Alignment()
al100.horz = Alignment.HORZ_CENTER
al100.vert = Alignment.VERT_CENTER
al100.rota = Alignment.ROTATION_STACKED

al10 = Alignment()
al10.horz = Alignment.HORZ_CENTER
al10.vert = Alignment.VERT_CENTER
al10.wrap = 1

al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_CENTER

al2 = Alignment()
al2.horz = Alignment.HORZ_RIGHT
al2.vert = Alignment.VERT_CENTER

al20 = Alignment()
al20.horz = Alignment.HORZ_RIGHT
al20.vert = Alignment.VERT_CENTER
al20.wrap = 1

al3 = Alignment()
al3.horz = Alignment.HORZ_LEFT
al3.vert = Alignment.VERT_CENTER
al3.wrap = 1

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

# размер шрифта
size = 11
# заголовки жирным шрифтом, с границами ячеек
style_headers = xlwt.XFStyle()
style_headers.font.bold = True
style_headers.font.name = 'Times New Roman'
style_headers.font.height = 20 * size
style_headers.borders = b1
style_headers.alignment = al10

# обычные ячейки, с границами ячеек
style_plain = xlwt.XFStyle()
style_plain.font.name = 'Times New Roman'
style_plain.font.height = 20 * size
style_plain.borders = b1
style_plain.alignment = al10

# обычные ячейки, с границами ячеек повернут на 90 градусов
style_plain_90 = xlwt.XFStyle()
style_plain_90.font.name = 'Times New Roman'
style_plain_90.font.height = 20 * size
style_plain_90.borders = b1
style_plain_90.alignment = al100


xlwt.easyxf('align: rotation 90')

# обычные ячейки, с толстыми границами ячеек
style_plain_bb = xlwt.XFStyle()
style_plain_bb.font.name = 'Times New Roman'
style_plain_bb.font.height = 20 * size
style_plain_bb.borders = b2
style_plain_bb.alignment = al10

# обычные ячейки с датами, с границами ячеек == style3
style_date = xlwt.XFStyle()
style_date.font.name = 'Times New Roman'
style_date.font.height = 20 * size
style_date.borders = b1
style_date.alignment = al10
style_date.num_format_str = 'DD.MM.YYYY г'

# обычные ячейки, с границами ячеек, c форматом чисел '0.00'  == style4
style_2dp = xlwt.XFStyle()
style_2dp.font.name = 'Times New Roman'
style_2dp.font.height = 20 * size
style_2dp.borders = b1
style_2dp.alignment = al1
style_2dp.num_format_str = '0.00'

# обычные ячейки, с границами ячеек, c форматом чисел '0.00000'  == style5
style_5dp = xlwt.XFStyle()
style_5dp.font.name = 'Times New Roman'
style_5dp.font.height = 20 * size
style_5dp.borders = b1
style_5dp.alignment = al1
style_5dp.num_format_str = '0.00000'

# обычные ячейки, с границами ячеек, c форматом чисел '0.0000'
style_4dp = xlwt.XFStyle()
style_4dp.font.name = 'Times New Roman'
style_4dp.font.height = 20 * size
style_4dp.borders = b1
style_4dp.alignment = al1
style_4dp.num_format_str = '0.0000'

# обычные ячейки, без границ  == style6
style_plain_nobor = xlwt.XFStyle()
style_plain_nobor.font.name = 'Times New Roman'
style_plain_nobor.font.height = 20 * size
style_plain_nobor.alignment = al10

# обычные ячейки, без границ  жирный шрифт размер больше на 1
style_plain_nobor_bold = xlwt.XFStyle()
style_plain_nobor_bold.font.bold = True
style_plain_nobor_bold.font.name = 'Times New Roman'
style_plain_nobor_bold.font.height = 20 * (size + 1)
style_plain_nobor_bold.alignment = al10

# обычные ячейки, без границ, сдвинуто вправо  == style7
style_plain_nobor_r = xlwt.XFStyle()
style_plain_nobor_r.font.name = 'Times New Roman'
style_plain_nobor_r.font.height = 20 * size
style_plain_nobor_r.alignment = al20

# обычные ячейки, без границ, сдвинуто влево
style_plain_nobor_l = xlwt.XFStyle()
style_plain_nobor_l.font.name = 'Times New Roman'
style_plain_nobor_l.font.height = 20 * size
style_plain_nobor_l.alignment = al3

# обычные ячейки, без границ, сдвинуто влево, c датовым форматом
style_plain_nobor_l_date = xlwt.XFStyle()
style_plain_nobor_l_date.font.name = 'Times New Roman'
style_plain_nobor_l_date.font.height = 20 * size
style_plain_nobor_l_date.alignment = al3
style_plain_nobor_l_date.num_format_str = 'DD.MM.YYYY г.'

# обычные ячейки, с границами, сдвинуто вправо  == style7
style_plain_r = xlwt.XFStyle()
style_plain_r.font.name = 'Times New Roman'
style_plain_r.font.height = 20 * size
style_plain_r.alignment.wrap = 1

pattern_black = xlwt.Pattern()
pattern_black.pattern = xlwt.Pattern.SOLID_PATTERN
pattern_black.pattern_fore_colour = 0

# чёрные ячейки
style_black = xlwt.XFStyle()
style_black.pattern = pattern_black

def get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search):

    row_num += 1
    columns = [
        f'{equipment_type}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 0, 19, style_headers)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 600

    for note in MODEL:
        try:
            person = Personchange.objects.filter(equipment__pk=note.equipment.pk).order_by('pk').last().person.username
        except:
            person = 'Ответственный за метрологическое обеспечение'

        try:
            note2 = MODEL2.objects.get(charakters__pk=note.charakters.pk)
            descriptiont0 = note2.descriptiont0
            descriptiont1 = note2.descriptiont1
            descriptiont2 = note2.descriptiont2
            commentservice = note2.commentservice
            if note2.descriptiont0:
                to0_shed = 'ежедневно'
            else:
                to0_shed = ' '
            if note2.descriptiont1:
                to1_shed = 'ежемесячно'
            else:
                to1_shed = ' '
            if note2.t2month1 == True:
                t2month1 = 'V'
            else:
                t2month1 = ' '
            if note2.t2month2 == True:
                t2month2 = 'V'
            else:
                t2month2 = ' '
            if note2.t2month3 == True:
                t2month3 = 'V'
            else:
                t2month3 = ' '
            if note2.t2month4 == True:
                t2month4 = 'V'
            else:
                t2month4 = ' '
            if note2.t2month5 == True:
                t2month5 = 'V'
            else:
                t2month5 = ' '
            if note2.t2month6 == True:
                t2month6 = 'V'
            else:
                t2month6 = ' '
            if note2.t2month7 == True:
                t2month7 = 'V'
            else:
                t2month7 = ' '
            if note2.t2month8 == True:
                t2month8 = 'V'
            else:
                t2month8 = ' '
            if note2.t2month9 == True:
                t2month9 = 'V'
            else:
                t2month9 = ' '
            if note2.t2month10 == True:
                t2month10 = 'V'
            else:
                t2month10 = ' '
            if note2.t2month11 == True:
                t2month11 = 'V'
            else:
                t2month11 = ' '
            if note2.t2month12 == True:
                t2month12 = 'V'
            else:
                t2month12 = ' '

        except:
            descriptiont0 = ' '
            descriptiont1 = ' '
            descriptiont2 = ' '
            commentservice = ' '
            t2month1 = ''
            t2month2 = ''
            t2month3 = ''
            t2month4 = ''
            t2month5 = ''
            t2month6 = ''
            t2month7 = ''
            t2month8 = ''
            t2month9 = ''
            t2month10 = ''
            t2month11 = ''
            t2month12 = ''
            to0_shed = ''
            to1_shed = ''

        t3month1 = ''
        t3month2 = ''
        t3month3 = ''
        t3month4 = ''
        t3month5 = ''
        t3month6 = ''
        t3month7 = ''
        t3month8 = ''
        t3month9 = ''
        t3month10 = ''
        t3month11 = ''
        t3month12 = ''
        t3month1f = ''
        t3month2f = ''
        t3month3f = ''
        t3month4f = ''
        t3month5f = ''
        t3month6f = ''
        t3month7f = ''
        t3month8f = ''
        t3month9f = ''
        t3month10f = ''
        t3month11f = ''
        t3month12f = ''

        # подставляем месяц плана поверки/аттестации/проверки
        try:
            note3 = MODEL3.objects.filter(equipmentSM__equipment__pk=note.equipment.pk).exclude(
                dateorder__isnull=True)

            q = note3.get(dateorder__year=year_search)
            t3month = int(q.dateorder.month)

            if t3month == 1:
                t3month1 = 'V'
            if t3month == 2:
                t3month2 = 'V'
            if t3month == 3:
                t3month3 = 'V'
            if t3month == 4:
                t3month4 = 'V'
            if t3month == 5:
                t3month5 = 'V'
            if t3month == 6:
                t3month6 = 'V'
            if t3month == 7:
                t3month7 = 'V'
            if t3month == 8:
                t3month8 = 'V'
            if t3month == 9:
                t3month9 = 'V'
            if t3month == 10:
                t3month10 = 'V'
            if t3month == 11:
                t3month11 = 'V'
            if t3month == 12:
                t3month12 = 'V'
        except:
            t3month1 = ''
            t3month2 = ''
            t3month3 = ''
            t3month4 = ''
            t3month5 = ''
            t3month6 = ''
            t3month7 = ''
            t3month8 = ''
            t3month9 = ''
            t3month10 = ''
            t3month11 = ''
            t3month12 = ''

        #  подставляем месяц факта поверки/аттестации/проверки
        try:
            note3 = MODEL3.objects.filter(equipmentSM__equipment__pk=note.equipment.pk).exclude(
                date__isnull=True)
            q = note3.get(date__year=year_search)
            t3monthf = int(q.date.month)

            if t3monthf == 1:
                t3month1f = 'V'
            if t3monthf == 2:
                t3month2f = 'V'
            if t3monthf == 3:
                t3month3f = 'V'
            if t3monthf == 4:
                t3month4f = 'V'
            if t3monthf == 5:
                t3month5f = 'V'
            if t3monthf == 6:
                t3month6f = 'V'
            if t3monthf == 7:
                t3month7f = 'V'
            if t3monthf == 8:
                t3month8f = 'V'
            if t3monthf == 9:
                t3month9f = 'V'
            if t3monthf == 10:
                t3month10f = 'V'
            if t3monthf == 11:
                t3month11f = 'V'
            if t3monthf == 12:
                t3month12f = 'V'
        except:
            t3month1f = ''
            t3month2f = ''
            t3month3f = ''
            t3month4f = ''
            t3month5f = ''
            t3month6f = ''
            t3month7f = ''
            t3month8f = ''
            t3month9f = ''
            t3month10f = ''
            t3month11f = ''
            t3month12f = ''

        row_num += 1
        columns = [
            '',
            f'{note.charakters.name}, {note.charakters.modificname}, {note.charakters.typename}',
            f'{note.charakters.name}, {note.charakters.modificname}, {note.charakters.typename}',
            f'{note.equipment.exnumber}',
            f'{note.equipment.lot}',
            '',
            'январь',
            'февраль',
            'март',
            'апрель',
            'май',
            'июнь',
            'июль',
            'август',
            'сентябрь',
            'октябрь',
            'ноябрь',
            'декабрь',
            f'{person}',
            f'{commentservice}',
        ]
        for col_num in range(7):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 1, 2, style_plain)
            ws.merge(row_num, row_num + 1, 6, 6, style_plain)
        for col_num in range(6, 18):
            ws.write(row_num, col_num, columns[col_num], style_plain_90)
            ws.merge(row_num, row_num + 1, 7, 7, style_plain_90)
            ws.merge(row_num, row_num + 1, 8, 8, style_plain_90)
            ws.merge(row_num, row_num + 1, 9, 9, style_plain_90)
            ws.merge(row_num, row_num + 1, 10, 10, style_plain_90)
            ws.merge(row_num, row_num + 1, 11, 11, style_plain_90)
            ws.merge(row_num, row_num + 1, 12, 12, style_plain_90)
            ws.merge(row_num, row_num + 1, 13, 13, style_plain_90)
            ws.merge(row_num, row_num + 1, 14, 14, style_plain_90)
            ws.merge(row_num, row_num + 1, 15, 15, style_plain_90)
            ws.merge(row_num, row_num + 1, 16, 16, style_plain_90)
            ws.merge(row_num, row_num + 1, 17, 17, style_plain_90)
        for col_num in range(18, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num + 4, 18, 18, style_plain)
            ws.merge(row_num, row_num + 6, 19, 19, style_plain)
            ws.merge(row_num, row_num + 4, 5, 5, style_plain)
            ws.merge(row_num, row_num + 6, 0, 0, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 2400


        row_num += 1
        columns = [
            '',
            'Тип ТО',
            'Объем технического обслуживания',
            '',
            '',
            '',
            'январь',
            'февраль',
            'март',
            'апрель',
            'май',
            'июнь',
            'июль',
            'август',
            'сентябрь',
            'октябрь',
            'ноябрь',
            'декабрь',
            f'{person}',
            f'{commentservice}',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 2, 4, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 500

        row_num += 1
        columns = [
            '',
            f'ТО 0',
            f'{descriptiont0}',
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            to0_shed,
            f'{person}',
            f'{commentservice}',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 2, 4, style_plain)
            ws.merge(row_num, row_num, 6, 17, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 2500

        row_num += 1
        columns = [
            '',
            f'ТО 1',
            f'{descriptiont1}',
            '',
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            to1_shed,
            f'{person}',
            f'{commentservice}',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 2, 4, style_plain)
            ws.merge(row_num, row_num, 6, 17, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 2500

        row_num += 1
        columns = [
            '',
            f'ТО 2',
            f'{descriptiont2}',
            f'{descriptiont2}',
            f'{descriptiont2}',
            '',
            t2month1,
            t2month2,
            t2month3,
            t2month4,
            t2month5,
            t2month6,
            t2month7,
            t2month8,
            t2month9,
            t2month10,
            t2month11,
            t2month12,
            f'{person}',
            f'{commentservice}',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 2, 4, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 2500

        row_num += 1
        columns = [
            '',
            f'ТО 3',
            f'{to3}',
            f'{to3}',
            f'{to3}',
            'план',
            t3month1,
            t3month2,
            t3month3,
            t3month4,
            t3month5,
            t3month6,
            t3month7,
            t3month8,
            t3month9,
            t3month10,
            t3month11,
            t3month12,
            f'Ответственный за метрологическое обеспечение',
            f'{commentservice}',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 2, 4, style_plain)
            ws.merge(row_num, row_num + 1, 1, 1, style_plain)
            ws.merge(row_num, row_num + 1, 2, 4, style_plain)
            ws.merge(row_num, row_num + 1, 18, 18, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 1300

        row_num += 1
        columns = [
            '',
            f'ТО 3',
            f'{to3}',
            f'{to3}',
            f'{to3}',
            'факт',
            t3month1f,
            t3month2f,
            t3month3f,
            t3month4f,
            t3month5f,
            t3month6f,
            t3month7f,
            t3month8f,
            t3month9f,
            t3month10f,
            t3month11f,
            t3month12f,
            f'Ответственный за метрологическое обеспечение',
            f'{commentservice}',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_plain)
            ws.merge(row_num, row_num, 2, 4, style_plain)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 1300

        row_num += 1
        columns = [
            ''
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], style_black)
            ws.merge(row_num, row_num, 0, 19, style_black)
            ws.row(row_num).height_mismatch = True
            ws.row(row_num).height = 40
    return row_num

# график тоир техобслуживания
def export_maintenance_schedule_xls(request):
    """представление для выгрузки графика ТО на указанную дату"""

    # получаем дату от пользователя
    serdate = request.GET['date']
    year_search = str(serdate)[0:4]

    # создаем выгрузку
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="TO_{serdate}.xls"'

    # добавляем книгу и страницу с названием
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(f'ТОиР СИ, ИО, ВО {serdate}', cell_overwrite_ok=True)
    ws.header_str = b''
    ws.footer_str = b''

    # ширина столбцов
    ws.col(0).width = 200
    ws.col(1).width = 2000
    ws.col(2).width = 4000
    ws.col(3).width = 2000
    ws.col(4).width = 3000
    ws.col(5).width = 2000
    ws.col(6).width = 1200
    ws.col(7).width = 1200
    ws.col(8).width = 1200
    ws.col(9).width = 1200
    ws.col(10).width = 1200
    ws.col(11).width = 1200
    ws.col(12).width = 1200
    ws.col(13).width = 1200
    ws.col(14).width = 1200
    ws.col(15).width = 1200
    ws.col(16).width = 1200
    ws.col(17).width = 1200
    ws.col(18).width = 4500
    ws.col(19).width = 4000

    # шапка
    company = CompanyCard.objects.get(pk=1)
    affirmation = f'УТВЕРЖДАЮ \n{company.positionboss}\n{company.name}\n____________/{company.nameboss}/\n«__» ________20__ г.'
    row_num = 2
    columns = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        affirmation,
        affirmation,
        affirmation,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor_r)
        ws.merge(row_num, row_num + 6, 17, 19, style_plain_nobor_r)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 2000

    row_num += 8
    columns = [
        f'График технического обслуживания и ремонта лабораторного оборудования'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_plain_nobor_bold)
        ws.merge(row_num, row_num, 0, 19, style_plain_nobor_bold)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 600


    # заголовки ТОиР
    row_num += 4
    columns = [
        '',
        'Наименование, модификация, тип',
        'Наименование, модификация, тип',
        'Внутренний номер',
        'Заводской номер',
        'Время выполнения ТОиР*',
        'I КВАРТАЛ',
        'I КВАРТАЛ',
        'I КВАРТАЛ',
        'II КВАРТАЛ',
        'II КВАРТАЛ',
        'II КВАРТАЛ',
        'III КВАРТАЛ',
        'III КВАРТАЛ',
        'III КВАРТАЛ',
        'IV КВАРТАЛ',
        'IV КВАРТАЛ',
        'IV КВАРТАЛ',
        'Ответственный за ТО',
        'Примечание',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 1, 2, style_headers)
        ws.merge(row_num, row_num, 6, 8, style_headers)
        ws.merge(row_num, row_num, 9, 11, style_headers)
        ws.merge(row_num, row_num, 12, 14, style_headers)
        ws.merge(row_num, row_num, 15, 17, style_headers)


    equipment_type = 'СИ'
    MODEL = MeasurEquipment.objects.exclude(equipment__status='С')
    MODEL2 = ServiceEquipmentME
    MODEL3 = Verificationequipment
    to3 = 'Поверка'

    get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search)

    row_num = get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search) + 1

    equipment_type = 'ИО'
    MODEL = TestingEquipment.objects.exclude(equipment__status='С')
    MODEL2 = ServiceEquipmentTE
    MODEL3 = Attestationequipment
    to3 = 'Аттестация'


    get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search)

    row_num = get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search) + 1

    equipment_type = 'ВО'
    MODEL = HelpingEquipment.objects.filter(charakters__kvasyattestation=True).exclude(equipment__status='С')
    MODEL2 = ServiceEquipmentHE
    MODEL3 = Checkequipment
    to3 = 'Проверка технических характеристик'

    get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search)

    row_num = get_rows_service_shedule(row_num, ws, MODEL, to3, equipment_type, MODEL2, MODEL3, year_search) + 1

    row_num += 2
    columns = [
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
        f'* Виды и периодичность технического обслуживания',
    ]
    for col_num in range(1, len(columns)-2):
        ws.write(row_num, col_num, columns[col_num], style_headers)
        ws.merge(row_num, row_num, 1, 17, style_headers)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 600

    row_num += 1
    columns = [
        '',
        'ТО 0',
        'Ежедневное/еженедельное ',
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        servicedesc0,
        '',
        '',
    ]
    for col_num in range(1, len(columns)-2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 3, 17, style_plain)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 3000

    row_num += 1
    columns = [
        '',
        'ТО 1',
        'Ежемесячное',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        '',
        '',
    ]
    for col_num in range(1, len(columns)-2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 3, 17, style_plain)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 3000

    row_num += 1
    columns = [
        '',
        'ТО 2',
        'Ежеквартальное',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        'В соответствии с Руководством по эксплуатации',
        '',
        '',
    ]
    for col_num in range(1, len(columns)-2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 3, 17, style_plain)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 3000

    row_num += 1
    columns = [
        '',
        'ТО 3',
        'Годовое',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        'Поверка/калибровка/аттестатция',
        '',
        '',
    ]
    for col_num in range(1, len(columns)-2):
        ws.write(row_num, col_num, columns[col_num], style_plain)
        ws.merge(row_num, row_num, 3, 17, style_plain)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 3000

    # все сохраняем
    wb.save(response)
    return response
