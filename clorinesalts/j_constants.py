constitoptional = ('Образец представляет собой раствор хлорид-ионов в смеси органического растворителя и минерального масла, разлитую  в полимерный флакон вместимостью 250 см3', 
           'Образец представляет собой стабилизированную нефть, разлитую в стеклянный флакон вместимостью 250 см3', 
           'Проба представляет собой ....., разлитую в  полимерный флакон вместимостью 100 см3', 
        )




metodic = 'ГОСТ 21534-2021. НЕФТЬ. Методы определения содержания хлористых солей'

from main.models import AttestationJ

JOURNAL = AttestationJ
journal = 'attestationJ'
URL = 'clorinesalts'
NAME = 'хлористые соли'


conclusionoptional = (
    ('Контроль повторяемости результатов измерений кинематической вязкости удовлетворителен, так как расхождение между результатами измерений содержания хлористых солей в условиях повторяемости не превышает норматив контроля'),
    ('Контроль повторяемости результатов измерений кинематической вязкости удовлетворителен, так как расхождение между результатами измерений содержания хлористых солей в условиях повторяемости не превышает норматив контроля'),
    ('Результаты подчинены нормальному распределению, выбросы отсутствуют, партия признана однородной'),
    ('Результаты подчинены нормальному распределению, выбросы отсутствуют, партия признана однородной'),
    ('Другое', 'Другое'))
conclusion = 'Контроль повторяемости результатов измерений содержания хлористых солей удовлетворителен, '
parameter = 'Содержание хлористых солей'
attcharacteristic = 'Содержание хлористых солей'
measureparameter = 'Содержание хлористых солей'
