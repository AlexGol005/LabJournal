

def export_metroyear_xls(request):
    '''представление для выгрузки списка СИ и ИО поверка в год без учёта стоимости'''
    serdate = request.GET['date']
    qs = MeasurEquipment.objects. \
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
        'equipmentSM_ver__price',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
    ).order_by('equipmentSM_ver__date')

    qt = TestingEquipment.objects. \
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
        'equipmentSM_att__price',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
    ).order_by('equipmentSM_att__date')


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="equipment.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('СИ', cell_overwrite_ok=True)
    ws1 = wb.add_sheet('ИО', cell_overwrite_ok=True)
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws1.header_str = b'  '
    ws1.footer_str = b'c. &P '

    # ширина столбцов СИ
    ws.col(0).width = 3000
    ws.col(1).width = 3000
    ws.col(2).width = 4500
    ws.col(3).width = 3000
    ws.col(4).width = 4200
    ws.col(6).width = 2600
    ws.col(7).width = 3000
    ws.col(8).width = 3000


    # ширина столбцов ИО
    ws1.col(0).width = 3000
    ws1.col(1).width = 4500
    ws1.col(2).width = 3500
    ws1.col(3).width = 4200
    ws1.col(4).width = 4500
    ws1.col(5).width = 2600
    ws1.col(6).width = 3000
    ws1.col(7).width = 3000


    # заголовки СИ
    row_num = 0
    columns = [
                'Внутренний  номер',
                'Номер в госреестре',
                'Наименование',
                'Тип/Модификация',
                'Заводской номер',
                'Номер свидетельства',
                'Стоимость поверки, руб.',
                'Дата поверки/калибровки',
                'Дата окончания свидетельства',
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)

    rows = qs
    for row in rows:
        row_num += 1
        for col_num in range(7):
            ws.write(row_num, col_num, row[col_num], style20)
        for col_num in range(7, len(row)):
            ws.write(row_num, col_num, row[col_num], style30)


        # заголовки ИО, первый ряд
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Номер аттестата',
        'Стоимость аттестации, руб.',
        'Дата аттестации',
        'Дата окончания аттестации',
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style10)

    rows = qt
    for row in rows:
        row_num += 1
        for col_num in range(6):
            ws1.write(row_num, col_num, row[col_num], style20)
        for col_num in range(6, len(row)):
            ws1.write(row_num, col_num, row[col_num], style30)
    wb.save(response)
    return response

def export_metroyearprice_xls(request):
    '''представление для выгрузки списка СИ и ИО поверка в год с учётом стоимости'''
    serdate = request.GET['date']
    qs = MeasurEquipment.objects. \
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
        'equipmentSM_ver__price',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
    ).order_by('equipmentSM_ver__date')

    qt = TestingEquipment.objects. \
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
        'equipmentSM_att__price',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
    ).order_by('equipmentSM_att__date')

    qs1 = MeasurEquipment.objects. \
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

    qt1 = TestingEquipment.objects. \
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


    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="equipment.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('СИ', cell_overwrite_ok=True)
    ws1 = wb.add_sheet('ИО', cell_overwrite_ok=True)
    ws2 = wb.add_sheet('Количество поверок в месяц', cell_overwrite_ok=True)
    ws3 = wb.add_sheet('Количество аттестаций в месяц', cell_overwrite_ok=True)
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws1.header_str = b'  '
    ws1.footer_str = b'c. &P '
    ws2.header_str = b'  '
    ws2.footer_str = b'c. &P '
    ws3.header_str = b'  '
    ws3.footer_str = b'c. &P '

    # ширина столбцов СИ
    ws.col(0).width = 3000
    ws.col(1).width = 3000
    ws.col(2).width = 4500
    ws.col(3).width = 3000
    ws.col(4).width = 4200
    ws.col(6).width = 2600
    ws.col(7).width = 3000
    ws.col(8).width = 3000


    # ширина столбцов ИО
    ws1.col(0).width = 3000
    ws1.col(1).width = 4500
    ws1.col(2).width = 3500
    ws1.col(3).width = 4200
    ws1.col(4).width = 4500
    ws1.col(5).width = 2600
    ws1.col(6).width = 3000
    ws1.col(7).width = 3000

    # заголовки СИ
    row_num = 0
    columns = [
                'Внутренний  номер',
                'Номер в госреестре',
                'Наименование',
                'Тип/Модификация',
                'Заводской номер',
                'Номер свидетельства',
                'Стоимость поверки, руб.',
                'Дата поверки/калибровки',
                'Дата окончания свидетельства',
               ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)

    rows = qs
    for row in rows:
        row_num += 1
        for col_num in range(7):
            ws.write(row_num, col_num, row[col_num], style20)
        for col_num in range(7, len(row)):
            ws.write(row_num, col_num, row[col_num], style30)

        while col_num < 9:
            for column in columns:
                if column[0] == 'дата':
                    ws1.write(row_num, col_num, row[col_num], style_date)
                    col_num += 1
            ws1.write(row_num, col_num, row[col_num], style_plain)
            col_num += 1
        # for substring in ['Дата', 'дата', 'Даты', 'даты']:
        # заголовки ИО, первый ряд
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Номер аттестата',
        'Стоимость аттестации, руб.',
        'Дата аттестации',
        'Дата окончания аттестации',
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style10)

    rows = qt
    for row in rows:
        row_num += 1
        for col_num in range(6):
            ws1.write(row_num, col_num, row[col_num], style20)
        for col_num in range(6, len(row)):
            ws1.write(row_num, col_num, row[col_num], style30)

        # заголовки подсчёт поверок СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число поверок',
        'Сумма в месяц, руб',
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style10)

    rows = qs1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws2.write(row_num, col_num, row[col_num], style20)

    # заголовки подсчёт аттестаций СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число аттестаций',
        'Сумма в месяц, руб',
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style10)

    rows = qt1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws3.write(row_num, col_num, row[col_num], style20)



    wb.save(response)
    return response
# флаг в работе сейчас
def export_metroyearcust_xls(request):
    '''представление для выгрузки списка СИ и ИО поверка в год без поверок заказанных поставщиками'''
    serdate = request.GET['date']
    qs = MeasurEquipment.objects. \
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
        'equipmentSM_ver__price',
        'equipmentSM_ver__date',
        'equipmentSM_ver__datedead',
    ).order_by('equipmentSM_ver__date')


    qt = TestingEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value(' '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_att__in=setatt). \
        filter(equipmentSM_att__date__year=serdate). \
        exclude(equipmentSM_att__cust=True). \
        values_list(
        'equipment__exnumber',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_att__certnumber',
        'equipmentSM_att__price',
        'equipmentSM_att__date',
        'equipmentSM_att__datedead'
    ).order_by('equipmentSM_att__date')

    qs1 = MeasurEquipment.objects. \
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

    qt1 = TestingEquipment.objects. \
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

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="equipment.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('СИ', cell_overwrite_ok=True)
    ws1 = wb.add_sheet('ИО', cell_overwrite_ok=True)
    ws2 = wb.add_sheet('Количество поверок в месяц', cell_overwrite_ok=True)
    ws3 = wb.add_sheet('Количество аттестаций в месяц', cell_overwrite_ok=True)
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws1.header_str = b'  '
    ws1.footer_str = b'c. &P '
    ws2.header_str = b'  '
    ws2.footer_str = b'c. &P '
    ws3.header_str = b'  '
    ws3.footer_str = b'c. &P '

    # ширина столбцов СИ
    ws.col(0).width = 3000
    ws.col(1).width = 3000
    ws.col(2).width = 4500
    ws.col(3).width = 3000
    ws.col(4).width = 4200
    ws.col(6).width = 2600
    ws.col(7).width = 3000
    ws.col(8).width = 3000

    # ширина столбцов ИО
    ws1.col(0).width = 3000
    ws1.col(1).width = 4500
    ws1.col(2).width = 3500
    ws1.col(3).width = 4200
    ws1.col(4).width = 4500
    ws1.col(5).width = 2600
    ws1.col(6).width = 3000
    ws1.col(7).width = 3000

    # заголовки СИ
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Номер свидетельства',
        'Стоимость поверки, руб.',
        'Дата поверки/калибровки',
        'Дата окончания свидетельства',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)

    rows = qs
    for row in rows:
        row_num += 1
        for col_num in range(7):
            ws.write(row_num, col_num, row[col_num], style20)
        for col_num in range(7, len(row)):
            ws.write(row_num, col_num, row[col_num], style30)

        # заголовки ИО, первый ряд
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Номер аттестата',
        'Стоимость аттестации, руб.',
        'Дата аттестации',
        'Дата окончания аттестации',
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style10)

    rows = qt
    for row in rows:
        row_num += 1
        for col_num in range(6):
            ws1.write(row_num, col_num, row[col_num], style20)
        for col_num in range(6, len(row)):
            ws1.write(row_num, col_num, row[col_num], style30)

        # заголовки подсчёт поверок СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число поверок',
        'Сумма в месяц, руб',
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style10)

    rows = qs1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws2.write(row_num, col_num, row[col_num], style20)

    # заголовки подсчёт аттестаций СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число аттестаций',
        'Сумма в месяц, руб',
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style10)

    rows = qt1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws3.write(row_num, col_num, row[col_num], style20)

    wb.save(response)
    return response

# флаг куплено за год

def export_metronewyear_xls(request):
    '''представление для выгрузки списка оборудования купленного за год'''
    serdate = request.GET['date']
    qs = MeasurEquipment.objects. \
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

    qt = TestingEquipment.objects. \
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

    qh = HelpingEquipment.objects. \
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

    qs1 = MeasurEquipment.objects. \
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

    qt1 = TestingEquipment.objects. \
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

    qh1 = HelpingEquipment.objects. \
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

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{serdate} purchased equipment.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('СИ купленные', cell_overwrite_ok=True)
    ws1 = wb.add_sheet('ИО купленные', cell_overwrite_ok=True)
    ws2 = wb.add_sheet('Количество СИ в месяц', cell_overwrite_ok=True)
    ws3 = wb.add_sheet('Количество ИО в месяц', cell_overwrite_ok=True)
    ws4 = wb.add_sheet('ВО купленное', cell_overwrite_ok=True)
    ws5 = wb.add_sheet('Количество ВО в месяц', cell_overwrite_ok=True)
    ws.header_str = b'  '
    ws.footer_str = b' '
    ws1.header_str = b'  '
    ws1.footer_str = b' '
    ws2.header_str = b'  '
    ws2.footer_str = b''
    ws3.header_str = b'  '
    ws3.footer_str = b''
    ws4.header_str = b'  '
    ws4.footer_str = b''
    ws5.header_str = b'  '
    ws5.footer_str = b''


    # ширина столбцов СИ
    ws.col(0).width = 3000
    ws.col(1).width = 3000
    ws.col(2).width = 4500
    ws.col(3).width = 3000
    ws.col(4).width = 4200
    ws.col(6).width = 2600
    ws.col(7).width = 3000
    ws.col(8).width = 3000

    # ширина столбцов ИО
    ws1.col(0).width = 3000
    ws1.col(1).width = 4500
    ws1.col(2).width = 3500
    ws1.col(3).width = 4200
    ws1.col(4).width = 4500
    ws1.col(5).width = 2600
    ws1.col(6).width = 3000
    ws1.col(7).width = 3000

    # ширина столбцов ВО
    ws4.col(0).width = 3000
    ws4.col(1).width = 4500
    ws4.col(2).width = 3500
    ws4.col(3).width = 4200
    ws4.col(4).width = 4500
    ws4.col(5).width = 2600
    ws4.col(6).width = 3000
    ws4.col(7).width = 3000

    # заголовки СИ
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Стоимость',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)

    rows = qs
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], style20)

        # заголовки ИО, первый ряд
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Стоимость',
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style10)

    rows = qt
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws1.write(row_num, col_num, row[col_num], style20)


    # заголовки ВО, первый ряд
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Стоимость',
    ]
    for col_num in range(len(columns)):
        ws4.write(row_num, col_num, columns[col_num], style10)

    rows = qh
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws4.write(row_num, col_num, row[col_num], style20)

    # заголовки подсчёт по месяцам СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число единиц',
        'Сумма в месяц, руб',
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style10)

    rows = qs1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws2.write(row_num, col_num, row[col_num], style20)

    # заголовки подсчёт по месяцам ИО
    row_num = 0
    columns = [
        'Месяц',
        'Число единиц',
        'Сумма в месяц, руб',
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style10)

    rows = qt1
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws3.write(row_num, col_num, row[col_num], style20)

        # заголовки подсчёт по месяцам ВО
        row_num = 0
        columns = [
            'Месяц',
            'Число единиц',
            'Сумма в месяц, руб',
        ]
        for col_num in range(len(columns)):
            ws5.write(row_num, col_num, columns[col_num], style10)

        rows = qh1
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws5.write(row_num, col_num, row[col_num], style20)

    wb.save(response)
    return response


# флаг планы на следующий год
def export_planmetro_xls(request):
    '''представление для выгрузки плана поверки и аттестации на следующий год'''
    serdate = request.GET['date']
    qs = MeasurEquipment.objects. \
        annotate(mod_type=Concat('charakters__typename', Value('/ '), 'charakters__modificname'),
                 manuf_country=Concat('equipment__manufacturer__country', Value(', '),
                                      'equipment__manufacturer__companyName')). \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__dateorder__year=serdate). \
        values_list(
        'equipment__exnumber',
        'charakters__reestr',
        'charakters__name',
        'mod_type',
        'equipment__lot',
        'equipmentSM_ver__certnumber',
        'equipmentSM_ver__price',
        'equipmentSM_ver__dateorder__month',
    ).order_by('equipmentSM_ver__dateorder__month')

    qt = TestingEquipment.objects. \
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
        'equipmentSM_att__price',
        'equipmentSM_att__dateorder__month',
    ).order_by('equipmentSM_att__dateorder__month')

    qount_plan_verific = MeasurEquipment.objects. \
        filter(equipment__personchange__in=setperson). \
        filter(equipment__roomschange__in=setroom). \
        filter(equipmentSM_ver__in=setver). \
        filter(equipmentSM_ver__dateorder__year=serdate). \
        values('equipmentSM_ver__date__month'). \
        annotate(dcount=Count('equipmentSM_ver__date__month'), s=Sum('equipmentSM_ver__price')). \
        order_by(). \
        values_list(
        'equipmentSM_ver__date__month',
        'dcount',
        's',
    )

    qount_plan_att = TestingEquipment.objects. \
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



    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="pov_att_plan {serdate}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('СИ', cell_overwrite_ok=True)
    ws1 = wb.add_sheet('ИО', cell_overwrite_ok=True)
    ws2 = wb.add_sheet('Количество поверок в месяц', cell_overwrite_ok=True)
    ws3 = wb.add_sheet('Количество аттестаций в месяц', cell_overwrite_ok=True)
    ws.header_str = b'  '
    ws.footer_str = b'c. &P '
    ws1.header_str = b'  '
    ws1.footer_str = b'c. &P '
    ws2.header_str = b'  '
    ws2.footer_str = b'c. &P '
    ws3.header_str = b'  '
    ws3.footer_str = b'c. &P '

    # ширина столбцов СИ
    ws.col(0).width = 3000
    ws.col(1).width = 3000
    ws.col(2).width = 4500
    ws.col(3).width = 3000
    ws.col(4).width = 4200
    ws.col(6).width = 2600
    ws.col(7).width = 3000
    ws.col(8).width = 3000

    # ширина столбцов ИО
    ws1.col(0).width = 3000
    ws1.col(1).width = 4500
    ws1.col(2).width = 3500
    ws1.col(3).width = 4200
    ws1.col(4).width = 4500
    ws1.col(5).width = 2600
    ws1.col(6).width = 3000
    ws1.col(7).width = 3000

    # заголовки СИ
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Номер в госреестре',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Номер текущего свидетельства',
        'Стоимость последней поверки, руб. (при наличии)',
        'Месяц заказа поверки',
    ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], style10)

    rows = qs
    for row in rows:
        row_num += 1
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, row[col_num], style20)


        # заголовки ИО, первый ряд
    row_num = 0
    columns = [
        'Внутренний  номер',
        'Наименование',
        'Тип/Модификация',
        'Заводской номер',
        'Номер аттестата',
        'Стоимость последней аттестации, руб. (при наличии)',
        'Месяц заказа аттестации',
    ]
    for col_num in range(len(columns)):
        ws1.write(row_num, col_num, columns[col_num], style10)

    rows = qt
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws1.write(row_num, col_num, row[col_num], style20)

        # заголовки подсчёт поверок СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число поверок',
    ]
    for col_num in range(len(columns)):
        ws2.write(row_num, col_num, columns[col_num], style10)

    rows = qount_plan_verific
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws2.write(row_num, col_num, row[col_num], style20)

    # заголовки подсчёт аттестаций СИ
    row_num = 0
    columns = [
        'Месяц',
        'Число аттестаций',
    ]
    for col_num in range(len(columns)):
        ws3.write(row_num, col_num, columns[col_num], style10)

    rows = qount_plan_att
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws3.write(row_num, col_num, row[col_num], style20)

    wb.save(response)
    return response