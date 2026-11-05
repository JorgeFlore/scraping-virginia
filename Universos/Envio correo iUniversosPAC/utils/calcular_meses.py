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

