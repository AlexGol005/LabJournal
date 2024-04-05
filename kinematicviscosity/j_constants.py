import datetime

from main.models import AttestationJ


affirmationprod = 'УТВЕРЖДАЮ \nНачальник производства \nООО "Петроаналитика"\n___________ /Н.Ю. Пилявская'
sertificat9001 = 'Сертифицирован на соотвествие требованиям национального стандарта \nГОСТ Р ИСО 9001-2015 \n' \
                 'органом по сертификации СМК ООО "ACEPT Бюро" \n от 23.06.2022г., сертификат действителен ' \
                 'до 24.12.2025 г.',
fordate = '"___" _______ "20___"',
nameprot = 'ПРОТОКОЛ ИСПЫТАНИЙ № 00/24'


RELERROR = 0.3  # относительная погрешность

ndocumentoptional = (
    ('МИ-02-2018', 'МИ-02-2018. Методика измерений  кинематической и динамической вязкости жидкости'),
    ('оценка', 'оценка вязкости'),
    ('ГОСТ 33-2016', 'ГОСТ 33-2016.НЕФТЬ И НЕФТЕПРОДУКТЫ. ПРОЗРАЧНЫЕ И НЕПРОЗРАЧНЫЕ ЖИДКОСТИ. Определение кинематической и динамической вязкости'))

aimoptional = (
    ('Мониторинг стабильности', 'Мониторинг стабильности'),
    ('Характеризация', 'Характеризация'),
    ('Межэкземплярная однородность', 'Межэкземплярная однородность'),
    ('Внутриэкземплярная однородность', 'Внутриэкземплярная однородность'),
    ('Другое', 'Другое'))
# нормативные документы

CHOICES = (
    ('да', 'Проба содержит октол/нефть'),
    ('нет', 'В пробе нет октола/нефти'),
    ('по ГОСТ 33', 'по ГОСТ 33 ("прочие нефтепродукты")'),
    ('другое', 'другое'),
)

JOURNAL = AttestationJ
journal = 'attestationJ'
URL = 'kinematicviscosity'
NAME = 'кинематика'


# для выгрузок exel
metodic = 'МИ-02-2018. Методика измерений  кинематической и динамической вязкости жидкости. Утверждена в ООО "Петроаналитика'



parameter = 'вязкость кинематическая'
constitoptional = ('Образец представляет собой смесь высоковязкого масла и среднедистиллятного топлива, разлитую  в полимерный флакон вместимостью 250 см3', 
           'Образец представляет собой стабилизированную нефть, разлитую в стеклянный флакон вместимостью 250 см3', 
           'Образец представляет собой трансформаторное масло, разлитое в  стеклянный флакон вместимостью 1000 см3', 
           'Проба представляет собой ....., разлитую в  полимерный флакон вместимостью 100 см3', 
        )
measureparameter = 'Время истечения определённого объема жидкости под влиянием силы тяжести при заданной температуре'

