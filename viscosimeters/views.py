from decimal import Decimal

from django.shortcuts import render
from django.db import connection
from django.views import View
from django.http import  HttpResponse, HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from django.db.models import Max
from viscosimeters.models import Viscosimeters, Kalibration
from .forms import KalibrationViscosimetersForm

@login_required
def KalibrationViscosimetersRegView(request):
    """ выводит форму внесения калибровки вискозиметров. """
    if request.method == "POST":
        form = KalibrationViscosimetersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.performer = request.user
            order.save()
            name = form.cleaned_data.get('id_Viscosimeter')
            konstant = form.cleaned_data.get('konstant')
            messages.success(request, f'Константа {konstant} вискозиметра {name} внесена!')
            return redirect('/kalibrationviscosimetersreg/')
    else:
        form = KalibrationViscosimetersForm()

    return render(
        request,
        'viscosimeters/registration.html',
        {
            'form': form
        })

class ViscosimetersView(View):
    """ Представление, которое выводит все вискозиметры с константами. """
    def get(self, request):
        get_id_actualconstant = Kalibration.objects.select_related('id_Viscosimeter').values('id_Viscosimeter').\
            annotate(id_actualkonstant=Max('id')).values('id_actualkonstant')
        list_ = list(get_id_actualconstant)
        set = []
        for n in list_:
            set.append(n.get('id_actualkonstant'))
        viscosimeters = Kalibration.objects.select_related('id_Viscosimeter').filter(id__in=set).\
            filter(id_Viscosimeter__equipmentSM__equipment__status__exact='Э').\
            order_by('id_Viscosimeter__viscosimeterType__diameter')
        data = {'viscosimeters': viscosimeters}


        return render(request, 'viscosimeters/viscosimetersKonstants.html', data)


class ViscosimeterTypeView(View):

    def get(self, request):
        ViscosimeterTypeObjects = Viscosimeters.objects.annotate(actualkonst=Max('kalibration__id'))

        return render(request, 'viscosimeters/viscosimeterType.html', {'ViscosimeterTypeObjects': ViscosimeterTypeObjects})

# class ViscosimetersKonstantsView(View):
#     '''должна выводить список вискозиметров с актуальными константами'''
#     def get(self, request):
#         ViscosimetersObjects = Viscosimeters.objects.order_by('viscosimeterType_id')
#         return render(request, 'viscosimeters/viscosimetersKonstants.html', {'ViscosimetersObjects': ViscosimetersObjects})


class ViscosimetersHeadView(View):
    """ выводит заглавную старницу вискозиметров """
    def get(self, request):
        return render(request, 'viscosimeters/head.html')



# -------------------
import xlwt

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 3

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Имя', 'First name', 'Last name', 'Email address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
