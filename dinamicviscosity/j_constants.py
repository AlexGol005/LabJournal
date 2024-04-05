from main.models import AttestationJ


CHOICES = (
    ('да', 'Проба содержит октол/нефть'),
    ('нет', 'В пробе нет октола/нефти'),
    ('другое', 'другое'),
)

DENSITYE = (
    ('денсиметром', 'денсиметром'),
    ('пикнометром', 'пикнометром'),
)

DOCUMENTS = (('МИ-02-2018', 'МИ-02-2018'),)

RELERROR = 0.3  # относительная погрешность СО из описания типа

JOURNAL = AttestationJ
journal = 'attestationJ'
URL = 'dinamicviscosity'
NAME = 'динамика'

measureparameter = 'плотность'
