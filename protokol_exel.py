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

#содержимое ячейки справа
alr = Alignment()
alr.horz = Alignment.HORZ_RIGHT
alr.vert = Alignment.VERT_CENTER

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

#простой шрифт, без границ, выравнивание по правому краю
styleNnBR = xlwt.XFStyle()
styleNnBR.font.height = 20 * 8
styleNnBR.font.name = 'Times New Roman'
styleNnBR.alignment = alr
styleNnBR.alignment.wrap = 1

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

#простой шрифт, двойная граница, выравнивание по центру
styleNdBE = xlwt.XFStyle()
styleNdBE.font.height = 20 * 8
styleNdBE.font.name = 'Times New Roman'
styleNdBE.alignment = al1
styleNdBE.alignment.wrap = 1
styleNdBE.borders = b2

#шрифт курсив, без границ, выравнивание по центру
styleKnBE = xlwt.XFStyle()
styleKnBE.font.height = 20 * 8
styleKnBE.font.name = 'Times New Roman'
styleKnBE.font.italic = True
styleKnBE.alignment = al1
styleKnBE.alignment.wrap = 1




def export_protocol_xls_template(num, MATERIAL, MODEL, constitoptional, aimoptional, conclusionoptional, attcharacteristic):
    """представление для выгрузки протокола испытаний в ексель"""
    note = MODEL.objects.\
    annotate(name_rm=Concat(Value('СО '), 'name', Value('('), 'index', Value('), партия '), 'lot')).\
    annotate(performer_rm=Concat('performer__profile__userposition', Value(' '), 'performer__username')).get(pk=num)
    company = CompanyCard.objects.get(pk=1)              
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
    
    crit_K = note.crit_K
    ac = 'АЗ'
    eq_title = 'Используемое оборудование и средства измерений (основные), информация об их поверке/аттестации/ калибровке (градуировке) с указанием стандартных образцов и эталонов, примененных для этой цели (метрологическая прослеживаемость результатов измерений)',
    equipment_list = []
    try: 
        note.equipment_text
        equipment_list.append(note.equipment_text)
        
    except:
        pass
    try:
        note.equipment1
        e1 = MODEL.objects.\
        annotate(eq1=Concat('equipment1__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(' , зав. № '), 'equipment1__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        )).get(pk=num)
        equipment_list.append(e1.eq1)
    except:
        pass
    try:
        note.equipment2
        e2 = MODEL.objects.\
        annotate(eq2=Concat('equipment2__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(' , зав. № '), 'equipment1__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        )).get(pk=num)
        equipment_list.append(e2.eq2)
    except:
        pass
    try:
        note.equipment3
        e3 = MODEL.objects.\
        annotate(eq3=Concat('equipment3__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(' , зав. № '), 'equipment1__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        )).get(pk=num)
        equipment_list.append(e3.eq3)
    except:
        pass
    try:
        note.equipment4
        e4 = MODEL.objects.\
        annotate(eq4=Concat('equipment4__charakters__name',
                                        Value(' тип '), 'equipment1__charakters__typename',
                                        Value(' , зав. № '), 'equipment1__equipment__lot',
                                        Value(', свидетельство о поверке № '), 'equipment1__newcertnumber',
                                        Value(' от '), 'equipment1__newdate',
                                        Value(' действительно до '), 'equipment1__newdatedead',
                                        Value('; \n'),
                                        )).get(pk=num)
        equipment_list.append(e4.eq4)
    except:
        pass
        
    equipment_set = ' '.join(equipment_list)
        

    
    x1 = Decimal(note.x1).quantize(Decimal('1.0000'), ROUND_HALF_UP)
    x2 = Decimal(note.x2).quantize(Decimal('1.0000'), ROUND_HALF_UP)
    measureresult = note.x_avg.replace('.',',')
    acc = str(Decimal(note.factconvergence).quantize(Decimal('1.0'), ROUND_HALF_UP)).replace('.',',')
    r = str(note.repr1).replace('.',',')
    
    for i in range(len(MATERIAL)):
        if str(note.name)[0:2] == MATERIAL[i][0]:
            constit = constitoptional[i]


    for i in range(len(aimoptional)):
        if note.aim == aimoptional[i][0]:
            conclusion = conclusionoptional[i]
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{note.pk}_protocol.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('protocol', cell_overwrite_ok=True)

    ws.col(0).width = 1000
    ws.col(1).width = 5000
    ws.col(2).width = 3000
    ws.col(3).width = 3000
    ws.col(4).width = 2800
    ws.col(5).width = 2800
    ws.col(6).width = 2000
    ws.col(7).width = 2000
    ws.col(8).width = 2000
    ws.col(9).width = 2000
    ws.col(10).width = 2500
    ws.col(11).width = 2700
    ws.col(12).width = 3000
    ws.col(13).width = 3000


    Image.open(company.imglogoadress_mini.path).convert("RGB").save('logo.bmp')
    
    ws.left_margin = 0
    ws.header_str = b''
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


    ws.insert_bitmap('logo.bmp', 0, 0, 0, 5, 1.35, 0.8)


    row_num +=2
    columns = [
        nameprot,
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBE)
        ws.merge(row_num, row_num, 0, l, styleNnBE)


    row_num += 1
    dp = get_datenow()
    columns = [
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
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

    date_isp = get_dateformat(note.date)
    row_num +=1
    columns = [
        '8',
        'Дата и место проведения испытаний',
        f'{date_isp}, {company.adress}, п. {note.room.roomnumber}'
    ]
    for col_num in range(1):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

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
    ws.row(row_num).height = 400

    pressure = str(meteo.pressure).replace('.', ',')
    humidity = str(meteo.humidity).replace('.', ',')
    temperature = str(meteo.temperature).replace('.', ',')
    
    row_num +=1
    columns = [
        '12',
        'Условия проведения испытаний',
        'давление, кПа',
        pressure,
    ]
    hei = row_num + 2
    hei1 = row_num + 3
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
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '12',
        'Условия проведения испытаний',
        'температура, °С',
        temperature
    ]
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 3, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '12',
        'Условия проведения испытаний',
        'влажность, %',
        humidity
    ]
    for col_num in range(2, 3):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(3, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 3, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 400

    row_num +=1
    columns = [
        '12',
        'Средства измерения, использующиеся для мониторинга условий проведения испытаний',
        f'{meteo.equipment_meteo}\n{meteo.equipment_meteo1}.',
    ]
    hei = row_num + 3
    hei1 = row_num + 4
    for col_num in range(1, 2):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
    for col_num in range(2, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBL)
        ws.merge(row_num, row_num, 2, l, styleNBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 900

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
    ws.row(row_num).height = 300

    row_num +=3
    columns = [
        f'Страница №1\nВсего страниц 2',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBR)
        ws.merge(row_num, row_num, 0, l, styleNnBR)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700
 


    row_num +=2
    columns = [
        f'Результаты испытаний {note.name_rm}',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNBE)
        ws.merge(row_num, row_num, 0, l, styleNBE)
        
    count1=row_num
    Rep2 = str(note.Rep2).replace('.',',')

    if (note.seria == False or note.seria == '0') and note.aim != 'Мониторинг стабильности':

        row_num +=1
        columns = [
        '№',
        'Номер экземпляра',
        'Показатель, ед. изм',
        'Метод испытаний',
        eq_title,
        eq_title,
        eq_title,
        'X1',
        'X2',
        'Xср',
        'Характеристика погрешности метода испытаний (при P=0,95)',
        'Характеристика расширенной неопределенности измерений (при k=2, P=0,95)',
        'Характеристики прецизионности: повторяемость r',
        'Характеристики прецизионности: воспроизводимость R'        
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], styleNBE)
            ws.merge(row_num, row_num, 4, 6, styleNBE)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1400

        row_num +=1
    
        columns = [
            '1',
            note.numberexample,
            f'{attcharacteristic}, мг/дм3',
            note.ndocument,
            equipment_set,
            equipment_set,
            equipment_set,
            x1,
            x2,
            note.x_avg,
            '-',
            '-',
            note.repr1comma, 
            Rep2 
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], styleNBE)
            ws.merge(row_num, row_num, 4, 6, styleNBE)



    if (note.seria == False or note.seria == '0') and note.aim == 'Мониторинг стабильности':

        row_num +=1
        columns = [
        '№',
        'Номер экземпляра',
        'Показатель, ед. изм',
        'Метод испытаний',
         eq_title,
        eq_title,
        eq_title,
        'X1',
        'X2',
        'Xср',
        'Хаз',
        'К критерий',        
        'Характеристики прецизионности: повторяемость r',
        'Характеристики прецизионности: воспроизводимость R'        
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], styleNBE)
            ws.merge(row_num, row_num, 4, 6, styleNBE)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1400

        row_num +=1
    
        columns = [
            '1',
            note.numberexample,
            f'{attcharacteristic}, мг/дм3',
            note.ndocument,
            equipment_set, 
            equipment_set,
            equipment_set,
            x1,
            x2,
            note.x_avg,
            ac,
            crit_K,
            note.repr1comma, 
            Rep2 
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], styleNBE)
            ws.merge(row_num, row_num, 4, 6, styleNBE)


    count1=row_num
    
    if  note.seria != '0':

        row_num +=1
        columns = [
        '№',
        'Номер экземпляра',
        'Показатель, ед. изм',
        'Метод испытаний',
        eq_title,
        eq_title,
        eq_title,
        'X2',
        'Xср',
        'Характеристика погрешности метода испытаний (при P=0,95)',
        'Характеристика расширенной неопределенности измерений (при k=2, P=0,95)',
        'Характеристики прецизионности: повторяемость r',
        'Характеристики прецизионности: воспроизводимость R'        
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], styleNBE)
            ws.merge(row_num, row_num, 4, 6, styleNBE)
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 1400

        
        begin = row_num + 1

        
        
        a = note.seria
        qseria1 = MODEL.objects.all().filter(seria=a). \
        values_list(
        'numberexample',
        'x1',
        'x2',
        'x_avg',
        )
        
        for row in qseria1:
            row_num += 1
            for col_num in range(0, 1):
                ws.write(row_num, col_num + 1, row[col_num], styleNBE)
            for col_num in range(1, 4):
                ws.write(row_num, col_num + 6, row[col_num], styleNBE)
            counthe = row_num
                
        endy = counthe + 1
        for col_num in range(1):
            for row_num in range(begin, endy):
                ws.write(row_num, col_num, f'{row_num - 28}', styleNBE) 
                
        Rep2 = str(note.Rep2).replace('.',',')
        row_num1 = count1 + 2
        columns = [
        f'{attcharacteristic}, мг/дм3',
        note.ndocument,
        equipment_set,
        '-',
        '-',
        note.repr1comma, 
        Rep2         
        ]
        for col_num in range(3):
            ws.write(row_num1, col_num + 2, columns[col_num], styleNBE)
            ws.merge(row_num1, counthe, 2, 2, styleNBE)
            ws.merge(row_num1, counthe, 3, 3, styleNBE)
            ws.merge(row_num1, counthe, 4, 6, styleNBE)
        for col_num in range(3, 7):
            ws.write(row_num1, col_num + 7, columns[col_num], styleNBE)
            ws.merge(row_num1, counthe, 10, 10, styleNBE)
            ws.merge(row_num1, counthe, 11, 11, styleNBE)
            ws.merge(row_num1, counthe, 12, 12, styleNBE)
            ws.merge(row_num1, counthe, 13, 13, styleNBE)


        

    
    row_num +=3
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
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, 0, 1, styleNnBL)
    for col_num in range(1, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, 2, l, styleNnBL)


    row_num +=2
    columns = [
        company.prohibitet
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNdBE)
        ws.merge(row_num, row_num, 0, l, styleNdBE)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    row_num +=2
    columns = [
        'Исполнитель:'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, 0, l, styleNnBL)

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
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, 0, 2, styleNnBL)
    for col_num in range(3, 4):
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
    for col_num in range(4, len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBL)
        ws.merge(row_num, row_num, 4, 7, styleNnBL)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 600

    row_num +=1
    columns = [
        'Конец протокола испытаний'
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleKnBE)
        ws.merge(row_num, row_num, 0, l, styleKnBE)

    row_num +=12
    columns = [
        f'Страница №2\nВсего страниц 2',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], styleNnBR)
        ws.merge(row_num, row_num, 0, l, styleNnBR)
    ws.row(row_num).height_mismatch = True
    ws.row(row_num).height = 700

    wb.save(response)
    return response
