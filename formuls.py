from decimal import *

def rounder(value: Decimal, m: str) -> Decimal:
    '''округляет числа с неизвестным количесвом знаков после точки(запятой)(value) до указанного количества знаков (m)'''
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
    abserror = str(abserror)
    index = abserror.find(".")
    int_abserror = abserror[:index]
    frac_abserror = abserror[index + 1:]
    if int(int_abserror) > 2:
        result = Decimal(abserror)
        for j in range(len(frac_abserror), 0, -1):
            k = '1.' + j * '0'
            result = Decimal(result).quantize(Decimal(k), ROUND_HALF_UP)
        result = Decimal(result).quantize(Decimal('1'), ROUND_HALF_UP)
        return Decimal(result)
    if int(int_abserror) == 2 or int(int_abserror) == 1:
        result = Decimal(abserror)
        for j in range(len(frac_abserror), 0, -1):
            k = '1.' + j * '0'
            result = Decimal(result).quantize(Decimal(k), ROUND_HALF_UP)
        return Decimal(result)
    if int(int_abserror) == 0:
        i = 0
        while i < len(frac_abserror):
            if int(frac_abserror[i]) == 0:
                i += 1
            elif 0 < int(frac_abserror[i]) <= 2:
                result = Decimal(abserror)
                frac_index = i + 2
                for j in range(len(frac_abserror), frac_index - 1, -1):
                    k = '1.' + j * '0'
                    result = Decimal(result).quantize(Decimal(k), ROUND_HALF_UP)
                return Decimal(result)
            elif int(frac_abserror[i]) > 2:
                result = Decimal(abserror)
                frac_index = i + 1
                for j in range(len(frac_abserror), frac_index - 1, -1):
                    k = '1.' + j * '0'
                    result = Decimal(result).quantize(Decimal(k), ROUND_HALF_UP)
                return Decimal(result)




