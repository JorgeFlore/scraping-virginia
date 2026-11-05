from datetime import datetime

def calcular_mes1(date):
    meses = ("ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE")
    
    mes = meses[date.month - 3]
    mensaje = mes

    return mensaje


def calcular_mes2(date):
    meses = ("ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE")
    
    mes = meses[date.month - 2]
    mensaje = mes

    return mensaje


def calcular_mes3(date):
    meses = ("ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE")
    
    mes = meses[date.month - 1]
    mensaje = mes

    return mensaje



def calcular_meses(date):
    meses = ("ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE")
    
    meses_previos = []
    
    año_actual = date.year
    mes_actual = date.month
    for i in range(1, 4): 
        mes_prev = mes_actual - i
        
        # Si el mes es menor que 1 (enero), pasamos al año anterior
        if mes_prev < 0:
            año_anterior = año_actual - 1 
        else:
            año_anterior = año_actual
        
        # Agregar el año y mes a la lista
        meses_previos.append((año_anterior, meses[mes_prev]))
        
    return meses_previos[::-1] 



