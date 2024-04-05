from decimal import *

def get_avg(X1: Decimal, X2: Decimal, nums: int = 6):
    """
    находит среднее арифметическое из X1 и X2 и округляет до заданного числа знаков nums
    :param X1:
    :param X2:
    :param nums: число знаков после запятой
    :return Xсреднее:
    """
    k = '1.' + nums * '0'
    avg = ((X1 + X2)/Decimal(2)).quantize(Decimal(k), ROUND_HALF_UP)
    return avg

def get_acc_measurement(X1: Decimal, X2: Decimal, nums: int = 2 ):
    """находит разницу между измерениями X1 и X2 в процентах и округляет до заданного количества знаков после запятой nums"""
    k = '1.' + nums * '0'
    acc = ((X1 - X2).copy_abs() / get_avg(X1, X2) * Decimal(100)).quantize(Decimal(k), ROUND_HALF_UP)
    return acc

def get_sec(minutes: Decimal, secundes: Decimal):
    """переводит минуты и секунды в секунды и округляет"""
    k = '1.00'
    sec = (minutes * Decimal(60) + secundes).quantize(Decimal(k), ROUND_HALF_UP)
    return Decimal(sec)

def get_abserror(x_avg: Decimal, relerror: Decimal) -> Decimal:
    """находит абсолютную погрешность исходя из Хсреднего и относительной погрешности"""
    abserror = (x_avg * relerror) / Decimal('100')
    return abserror

def get_dateformat(date):
    dateformat = str(date)
    day = dateformat[8:]
    month = dateformat[5:7]
    year = dateformat[:4]
    rdate = f'{day}.{month}.{year}'
    return rdate

    
