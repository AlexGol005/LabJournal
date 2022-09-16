from kinematicviscosity.models import *
from main.models import AttestationJ


RELERROR = 0.3  # относительная погрешность

ndocumentoptional = (
    ('МИ-02-2018', 'МИ-02-2018'),
    ('оценка', 'оценка вязкости'),
    ('ГОСТ 33', 'ГОСТ 33'))  # нормативные документы

CHOICES = (
    ('да', 'Проба содержит октол/нефть'),
    ('нет', 'В пробе нет октола/нефти'),
    ('другое', 'другое'),
)

JOURNAL = AttestationJ
URL = 'kinematicviscosity'
NAME = 'кинематика'