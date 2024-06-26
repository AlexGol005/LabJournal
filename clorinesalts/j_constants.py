MATERIAL = (('СС-ТН-ПА', 'СС-ТН-ПА'),
           ('ХСН-ПА-1', 'ХСН-ПА-1'),
           ('ХСН-ПА-2', 'ХСН-ПА-2'),
           ('ГК-ПА-2', 'ГК-ПА-2'),
           ('др', 'др'))

MATERIAL1 = (('СС', 'СС'),
           ('ХС', 'ХС'),
           ('ГК', 'ГК'),
           ('др', 'др'))

constitoptional = ('Образец представляет собой стабилизированную нефть, разлитую в стеклянный флакон вместимостью 250 см3',
           'Образец представляет собой раствор хлорид-ионов в смеси органического растворителя и минерального масла, разлитую  в полимерный флакон вместимостью 250 см3'
           , 
          'Образец представляет собой стабилизированный газовый конденсат, разлитый в стеклянный флакон вместимостью 250 см3', 
           
           'Проба представляет собой ....., разлитую в  полимерный флакон вместимостью 100 см3', 
        )


GSO = 'ГСО 4391-88 "Стандартный образец состава натрия хлористого 1-го разряда", партия 4'

metodic = 'ГОСТ 21534-2021. НЕФТЬ. Методы определения содержания хлористых солей (метод А)'
ndocumentoptional = (
    ('ГОСТ 21534-2021. НЕФТЬ. Методы определения содержания хлористых солей (метод А)', 'ГОСТ 21534-2021. НЕФТЬ. Методы определения содержания хлористых солей  (метод А)'),
 )

from main.models import AttestationJ

JOURNAL = AttestationJ
journal = 'attestationJ'
URL = 'clorinesalts'
NAME = 'хлористые соли'
shortdocs = 'ГОСТ 21534-2021'

conclusionoptional = (
    ('Контроль стабильности партии удовлетворителен, так как расхождение между измеренным и аттестованным значением содержания хлористых солей не превышает критерий К.'),
    ('Контроль повторяемости результатов измерений удовлетворителен, так как расхождение между результатами измерений содержания хлористых солей в условиях повторяемости не превышает норматив контроля'),
    ('Результаты подчинены нормальному распределению, выбросы отсутствуют, партия признана однородной'),
    ('Результаты подчинены нормальному распределению, выбросы отсутствуют, партия признана однородной'),
    ('Другое', 'Другое'))

parameter = 'Содержание хлористых солей'
attcharacteristic = 'Содержание хлористых солей'
measureparameter = 'Содержание хлористых солей'


DOCUMENTS = (('ГОСТ 21534-2021. НЕФТЬ. Методы определения содержания хлористых солей', 'ГОСТ 21534-2021. НЕФТЬ. Методы определения содержания хлористых солей (метод А)'),
             )

CHOICES = (('до 10 мг/л включ.', 'до 10 мг/л включ.'),
           ('10 - 50 мг/л', '10 - 50 мг/л'),
           ('50 - 200 мг/л', '50 - 200 мг/л'),
           ('200 - 1000 мг/л', '200 - 1000 мг/л'),   )
roptional = (('1.5', '1.5'),
           ('3.0', '3.0'),
           ('6.0', '6.0'),
           ('25.0', '25.0'),   )
Roptional =  (('4.2', '4.2'),
           ('8.5', '8.5'),
           ('18.0', '18.0'),
           ('79.3', '79.3'),   )
CDoptional = (('2.8', '2.8'),
           ('5.7', '5.7'),
           ('12.2', '12.2'),
           ('53.9', '53.9'),   )

sigma_pr_optional = (
           ('0.037', '0.037'),
           ('0.333', '0.333'),
           ('1.7', '1.7'),  
           ('10.3', '10.3'),
           )

buroptional = (('Бюретка  ГОСТ 29251 2-го класса точности вместимостью 5 см3 с ценой деления 0,02 см3, внутренний номер 15', 'Бюретка  ГОСТ 29251 2-го класса точности вместимостью 5 см3 с ценой деления 0,02 см3. Внутренний номер 15;'),
           ('Бюретка  ГОСТ 29251 2-го класса точности вместимостью 10 см3 с ценой деления 0,05 см3, внутренний номер 37', 'Бюретка  ГОСТ 29251 2-го класса точности вместимостью 10 см3 с ценой деления 0,05 см3. Внутренний номер 37;'),
           ('Бюретка  ГОСТ 29251 2-го класса точности вместимостью 10 см3 с ценой деления 0,05 см3, внутренний номер', 'Бюретка  ГОСТ 29251 2-го класса точности вместимостью 10 см3 с ценой деления 0,05 см3. Внутренний номер 33;'),
           ('Бюретка  ГОСТ 29251 2-го класса точности вместимостью 10 см3 с ценой деления 0,05 см3, внутренний номер', 'Бюретка  ГОСТ 29251 2-го класса точности вместимостью 10 см3 с ценой деления 0,05 см3. Внутренний номер 36;'),   )
   

relerroroptional = (('1.0', '1.0'),
           ('5', '5'),
           ('2', '2'),
           ('3', '3'),
           ('0', '0'))
