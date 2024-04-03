from main.models import AttestationJ


RELERROR = 0.3  # относительная погрешность

ndocumentoptional = (
    ('МИ-02-2018', 'МИ-02-2018. Методика измерений  кинематической и динамической вязкости жидкости. Утверждена в ООО "Петроаналитика'),
    ('оценка', 'оценка вязкости'),
    ('ГОСТ 33-2016', 'ГОСТ 33-2016.НЕФТЬ И НЕФТЕПРОДУКТЫ. ПРОЗРАЧНЫЕ И НЕПРОЗРАЧНЫЕ ЖИДКОСТИ. Определение кинематической и динамической вязкости'))
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
sertificat9001 = 'Сертифицирован на соотвествие требованиям национального стандарта \nГОСТ Р ИСО 9001-2015 \n' \
                 'органом по сертификации СМК ООО "ACEPT Бюро" \n от 23.06.2022г., сертификат действителен ' \
                 'до 24.12.2025 г.',
affirmationprod = 'УТВЕРЖДАЮ \nНачальник производства \nООО "Петроаналитика"\n___________ /Н.Ю. Пилявская'
nameprot = 'ПРОТОКОЛ ИСПЫТАНИЙ № '
parameter = 'вязкость кинематическая'
