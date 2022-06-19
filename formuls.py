from decimal import *

K = 2  #(двойка из правила двойки)

def rounder(value: Decimal, m: str) -> Decimal:
    '''каскадно округляет числа с неизвестным количесвом знаков после точки(запятой)(value) до указанного количества знаков (m)'''
    st = str(value)
    index = st.find(".")
    frac_abserror = st[index + 1:]
    nst = '1.' + (len(m) - 2) * '0'
    n = len(nst) - 2
    print(n)
    for j in range(len(frac_abserror), n, -1):
        k = '1.' + j * '0'
        value = value.quantize(Decimal(k), ROUND_HALF_UP)
        print(value)
    value = value.quantize(Decimal(m), ROUND_HALF_UP)
    return Decimal(value)

def mrerrow(abserror) -> Decimal:
    '''округляет абсолютную погрешность в соответствии с правилами метрологии (правило двойки)'''
    if abserror > K:
        return Decimal(abserror).quantize(Decimal('1'), ROUND_HALF_UP)
    abserror = str(abserror)
    index = abserror.find(".")
    if index > 0:
        int_abserror = abserror[:index]
        frac_abserror = abserror[index + 1:]
        if int(int_abserror) in range(1, K + 1):
            result = Decimal(abserror).quantize(Decimal('1.0'), ROUND_HALF_UP)
            return Decimal(result)
        if int(int_abserror) == 0:
            i = 0
            while i < len(frac_abserror):
                if int(frac_abserror[i]) == 0:
                    i += 1
                if 0 < int(frac_abserror[i]) <= 2:
                    frac_index = i + 2
                    k = '1.' + frac_index * '0'
                    result = Decimal(abserror).quantize(Decimal(k), ROUND_HALF_UP)
                    return result
                if int(frac_abserror[i]) > 2:
                    frac_index = i + 1
                    k = '1.' + frac_index * '0'
                    result = Decimal(abserror).quantize(Decimal(k), ROUND_HALF_UP)
                    return result
    if index <= 0:
        result = Decimal(abserror).quantize(Decimal('1.0'), ROUND_HALF_UP)
        return result

def  numberDigits(avg: Decimal, abserror: Decimal) -> Decimal:
    '''округляет АЗ СО в соответствии с абсолютной погрешностью
    abserror: абсолютная погрешность
    avg: среднее из 2 измерений без округления
    return: АЗ СО в формате Decimal
    '''
    if abserror > K+1:
        certifiedValue = Decimal(avg).quantize(Decimal(1), ROUND_HALF_UP)
        return certifiedValue
    abserror = str(abserror)
    index = abserror.find(".")
    if index > 0:
        frac_abserror = abserror[index + 1:]
        j = len(frac_abserror)
        k = '1.' + j * '0'
        certifiedValue = avg.quantize(Decimal(k), ROUND_HALF_UP)
        return certifiedValue


