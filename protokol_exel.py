from decimal import Decimal
from PIL import Image
import xlwt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from xlwt import Borders, Alignment
from django.db.models.functions import Concat
from django.db.models import Value
from metods import *

from equipment.models import *
from utils import *
from textconstants import *

#задать: Model
from clorinesalts.models import Clorinesalts
from clorinesalts.j_constants import *


Model=Clorinesalts
#стили ячеек
brd1 = Borders()
brd1.left = 1
brd1.right = 1
brd1.top = 1
brd1.bottom = 1

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

al2 = Alignment()
al2.horz = Alignment.HORZ_RIGHT
al2.vert = Alignment.VERT_CENTER

#содержимое ячейки в центре
al1 = Alignment()
al1.horz = Alignment.HORZ_CENTER
al1.vert = Alignment.VERT_CENTER

#содержимое ячейки слева
al3 = Alignment()
al3.horz = Alignment.HORZ_LEFT
al3.vert = Alignment.VERT_CENTER

#простой шрифт, без границ, выравнивание по центру
styleNnBE = xlwt.XFStyle()
styleNnBE.font.height = 20 * 8
styleNnBE.font.name = 'Times New Roman'
styleNnBE.alignment = al1
styleNnBE.alignment.wrap = 1

#простой шрифт, без границ, выравнивание по левому краю
styleNnBL = xlwt.XFStyle()
styleNnBL.font.height = 20 * 8
styleNnBL.font.name = 'Times New Roman'
styleNnBL.alignment = al3
styleNnBL.alignment.wrap = 1

#простой шрифт, обычная граница, выравнивание по центру
styleNBE = xlwt.XFStyle()
styleNBE.font.height = 20 * 8
styleNBE.font.name = 'Times New Roman'
styleNBE.alignment = al1
styleNBE.alignment.wrap = 1
styleNBE.borders = b1

#простой шрифт, обычная граница, выравнивание по левому краю
styleNBL = xlwt.XFStyle()
styleNBL.font.height = 20 * 8
styleNBL.font.name = 'Times New Roman'
styleNBL.alignment = al3
styleNBL.alignment.wrap = 1
styleNBL.borders = b1


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


def export_protocol_xls_template(request, pk):
    """представление для выгрузки протокола испытаний в ексель"""
    company = CompanyCard.objects.get(pk=1)
    note = Model.objects.\
        annotate(name_rm=Concat(Value('СО '), 'name', Value('('), 'index', Value('), партия '), 'lot')).\
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

    x1 = Decimal(note.x1).quantize(Decimal('1.0000'), ROUND_HALF_UP)
    x2 = Decimal(note.x2).quantize(Decimal('1.0000'), ROUND_HALF_UP)
    measureresult = note.x_avg.replace('.',',')
    acc = str(Decimal(note.factconvergence).quantize(Decimal('1.0'), ROUND_HALF_UP)).replace('.',',')
    r = str(note.repr1).replace('.',',')
    
    for i in range(len(MATERIAL)):
        if note.name == MATERIAL[i][0]:
            constit = constitoptional[i]


    for i in range(len(aimoptional)):
        if note.aim == aimoptional[i][0]:
            conclusion = conclusionoptional[i]
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}_protocol.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('protocol', cell_overwrite_ok=True)

    ws.col(0).width = 1700
    ws.col(1).width = 5000
    ws.col(2).width = 3000
    ws.col(3).width = 3000
    ws.col(4).width = 3000
    ws.col(5).width = 3000
    ws.col(6).width = 3000
    ws.col(7).width = 3000
    ws.col(8).width = 3000
    ws.col(9).width = 3000
    ws.col(10).width = 3000
    ws.col(11).width = 3000
    ws.col(12).width = 3500
    ws.col(13).width = 3500


    


    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    ws.insert_bitmap('logo.bmp', 0, 0)
    ws.left_margin = 0
    ws.header_str = b'&F c. &P  '
    ws.footer_str = b' '


    row_num = 1
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
        affirmationprod,
        affirmationprod,
    ]
    l = len(columns) - 1
    af = len(columns) - 2
    for col_num in range(af, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, af, l , styleNnBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 900


    row_num +=1
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
        'М.П.',
        '',
        fordate,
        fordate,
        ]
    mp = len(columns) - 4
    mp1 = mp + 1
    for col_num in range(mp, mp1):
        ws.write(row_num, col_num, columns[col_num], styleNnBE)
    for col_num in range(af, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, af, l, styleNnBE)

    row_num +=2
    columns = [
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
        nameprot,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBE)
        ws.merge(row_num, row_num, 0, l, styleNnBE)


    row_num += 1
    dp = get_datenow()
    columns = [
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
        f'от   {dp}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBE)
        ws.merge(row_num, row_num, 0, l, styleNnBE)

    row_num +=1
    columns = [
        note.name_rm,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBE)
        ws.merge(row_num, row_num, 0, l, styleNnBE)

    row_num +=1
    columns = [
        '1',
        'Полное наименование организации',
        'Общество с ограниченной ответственностью “Петроаналитика” (ООО "Петроаналитика")'
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '2',
        'Номер аттестата аккредитации и сертификата',
        'Сертификат № QMS44386 на соответствие требованиям ISO 9001:2015 и сертификат № Q-A01.19.02b на соответствие требованиям ГОСТ Р ИСО 9001–2015, выданные органом по сертификации систем менеджмента качества ООО «АСЕРТ Бюро» '
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '3',
        'Юридический адрес',
        '190020, Российская Федерация, город Санкт-Петербург, улица Бумажная, дом 17, литер А, офис 472 '
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '4',
        'Почтовый адрес',
        '190020, Российская Федерация, город Санкт-Петербург, улица Бумажная, дом 17, литер А, офис 472 '
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '5',
        'Контактный телефон/факс',
        '+7 (812) 447-95-10'
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '6',
        'E-mail',
        'info@petroanalytica.ru'
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '7',
        'Заказчик',
        'Общество с ограниченной ответственностью “Петроаналитика”'
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '8',
        'Дата и место проведения испытаний',
        f'{note.date}, {company.adress}, п. {note.room.roomnumber}'
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '9',
        'Описание объекта/образца испытаний',
        constit,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '10',
        'Отбор проб',
        'не проводился',
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '11',
        'Метод испытаний',
         note.ndocument,
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '12',
        'Условия проведения испытаний',
        'давление, кПа',
        'давление',
    ]
    hei = row_num + 3
    hei1 = row_num + 4
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
        ws.merge(row_num, hei1, 0, 0, styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, hei, 1, 1, styleNBE)
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 3, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '12',
        'Условия проведения испытаний',
        'температура, °С',
        'f'
    ]
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 3, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '12',
        'Условия проведения испытаний',
        'влажность, %',
        'wwer'
    ]
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 3, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '12',
        'Средства измерения, использующиеся для мониторинга условий проведения испытаний',
        'ch ch',
    ]
    hei = row_num + 3
    hei1 = row_num + 4
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

    row_num +=1
    columns = [
        '13',
        'Испытатель',
        note.performer_rm
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500
 



    row_num +=7
    columns = [
        '3 Испытатель: ',
        '3 Испытатель: ',
        f'{note.performer.profile.userposition} {note.performer_rm}',
    ]
    for col_num in range(2):
        ws.write(row_num, col_num, columns[col_num], style6)
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
    columns = [
        f'Результаты испытаний {note.name_rm}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
        ws.merge(row_num, row_num, 0, l, styleNBE)
        
    
    


    row_num +=1
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
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 2, 7, style7)

    row_num +=1
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
        ws.merge(row_num, row_num, 0, 1, style6)
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], style7)
    for col_num in range(3, 6):
        ws.write(row_num, col_num, columns[col_num], style7)
        ws.merge(row_num, row_num, 3, 5, style7)
    for col_num in range(6, 7):
        ws.write(row_num, col_num, columns[col_num], style2)
    for col_num in range(7, 8):
        ws.write(row_num, col_num, columns[col_num], style7)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 500

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
    rx = row_num + 1
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
        ws.merge(row_num, rx, 1, 1, style7)
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


 

    row_num +=1
    columns = [
        '9 Метод измерений/методика \n измерений:  ',
        '9 Метод измерений/методика \n измерений:  ',
        note.ndocument,
        note.ndocument,
        note.ndocument,
        note.ndocument,
        note.ndocument,
        note.ndocument,
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
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
        f'В соответствии с {note.ndocument}',
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
        f'Испытание {note.name_rm} по {note.ndocument}'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style8)
        ws.merge(row_num, row_num, 0, 7, style8)
    count1=row_num





    if (note.seria == False or note.seria == '0') and note.aim != 'Мониторинг стабильности':

        row_num +=1
        columns = [
        'Аттестуемая характеристика',
        'Аттестуемая характеристика',
        'Номер экземпляра',
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
    
        columns = [
            attcharacteristic,
            attcharacteristic,
            note.numberexample,
            x1,
            x2,
            measureresult,
            acc,
            r,
        ]
        for col_num in range(2):
            ws.write(row_num, col_num, columns[col_num], style8)
            ws.merge(row_num, row_num, 0, 1, style8)
        for col_num in range(2, 3):
            ws.write(row_num, col_num, columns[col_num], style11)
        for col_num in range(3, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style8)


    if (note.seria == False or note.seria == '0') and note.aim == 'Мониторинг стабильности':

        row_num +=1
        columns = [
        'Аттестуемая характеристика',
        'Аттестуемая характеристика',
        'Аттестованное значение, Хатт, мг/дм3',
        'Измеренное значение Х1, мг/дм3 ',
        'Измеренное значение Х2, мг/дм3 ',
        'Измеренное значение Хср, мг/дм3 ',
        'Разница между Хср и Хатт, мг/дм3. ',
        'Норматив контроля, К, мг/дм3 ',
        ]
        for col_num in range(2):
            ws.write(row_num, col_num, columns[col_num], style9)
            ws.merge(row_num, row_num, 0, 1, style9)
        for col_num in range(1, len(columns)):
            ws.write(row_num, col_num, columns[col_num], style9)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1050
    
        row_num +=1
    
        columns = [
            attcharacteristic,
            attcharacteristic,
            note.x_cv,
            x1,
            x2,
            measureresult,
            note.cv_convergence,
            note.crit_K,
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
        'factconvergencecomma',
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
        note.repr1comma,
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
