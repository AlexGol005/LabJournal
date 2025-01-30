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
    if abserror > K + 1:
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
    if abserror >= K+1:
        abserror = Decimal(abserror).quantize(Decimal('1'), ROUND_HALF_UP)
        certifiedValue = Decimal(avg).quantize(Decimal('1'), ROUND_HALF_UP)
        if abserror <= 29:
            return certifiedValue
        if abserror > 29:
            abserror = str(abserror)
            if int(abserror[0]) <= K:
                certifiedValue = (str(certifiedValue)[: -(len(abserror) - 2)]) + '.' + str(certifiedValue)[-(len(abserror) - 2):]
                certifiedValue = Decimal(certifiedValue).quantize(Decimal('1'), ROUND_HALF_UP)
                tail = (len(abserror) - 2) * '0'
                certifiedValue = str(certifiedValue) + tail
                return Decimal(certifiedValue)
            if int(abserror[0]) > K:
                certifiedValue = (str(certifiedValue)[: -(len(abserror) - 1)]) + '.' + str(certifiedValue)[-(len(abserror) - 1):]
                certifiedValue = Decimal(certifiedValue).quantize(Decimal('1'), ROUND_HALF_UP)
                tail = (len(abserror) - 1) * '0'
                certifiedValue = str(certifiedValue) + tail
                return Decimal(certifiedValue)
    abserror = str(abserror)
    index = abserror.find(".")
    if index > 0:
        frac_abserror = abserror[index + 1:]
        j = len(frac_abserror)
        k = '1.' + j * '0'
        certifiedValue = avg.quantize(Decimal(k), ROUND_HALF_UP)
        return certifiedValue

def get_ex_uncertainty_measuremetod(sigma_pr, reproductivity, k=2):
    '''считает расширенную неопределенность методики измерений исходя из к-коэф охвата, показателя правильности методики, воспроизводимости'''
    uncertainty_measuremetod = Decimal(k) * (((Decimal(reproductivity)/Decimal(2.77))**Decimal(2) + Decimal(sigma_pr)**Decimal(2))**Decimal(0.5))
    return uncertainty_measuremetod

def get_crit_K(uncertainty_rm, uncertainty_measuremetod):
    '''критерий К исходя  из неопределенности СО и методики'''
    crit_K = ((Decimal(uncertainty_rm)**Decimal(2) + uncertainty_measuremetod**Decimal(2))**Decimal(0.5)).quantize(Decimal('1.0'), ROUND_HALF_UP)
    return crit_K


def get_round_significant_figures(value: Decimal, n: int) -> Decimal:
    '''округляет число value до n значащих цифер. Значащие цифры числа - это все цифры в его записи, начиная с первой ненулевой слева.'''
    str_value = str(value)
    a = str_value.find('.')
    b = str_value.find(',')
    
    if a == -1 and b == -1:
        result = value
        
    if a != -1 or b != -1:
        if a != -1:
            point_index = a
        if b != -1:
            point_index = b 

        if value < 1:
            pass
        
        if value > 1 and point_index < n:
            i = 0
            while str_value[i] == 0 or str_value[i] == ',' or str_value[i] == '.':
                i += 1
            else:
                c = str_value[i]
                d = str_value.find(c)
        
        e = d + n + 2
        str_value_cut = str_value[:e]
        fractional_part = str_value_cut[point_index+1:]
        len_fractional_part = len(fractional_part)
        j = len_fractional_part - 1
        k = '1.' + j * '0'
        result = Decimal(value).quantize(Decimal(k), ROUND_HALF_UP)

        if value > 1 and point_index >= n:
            result = Decimal(value).quantize(Decimal('1'), ROUND_HALF_UP)

    return result

    

                
                
            
        
        
        
            


            
            
        
    




        
         
        
