from datetime import datetime, timedelta, date

def contar_dias_habiles_atras(dias_habiles):
    feriados = ['18-09-2024', '19-09-2024', '20-09-2024', '31-10-2024', '01-11-2024', '25-12-2024'] 
    # Obtener la fecha actual
    fecha_inicio = date.today()
    
    # Convertir las fechas de feriados a objetos date
    feriados = [datetime.strptime(fecha, '%d-%m-%Y').date() for fecha in feriados]
    
    # Contador de días hábiles
    contador = 0
    fecha_actual = fecha_inicio
    
    # Iterar hasta contar los días hábiles requeridos
    while contador < dias_habiles:
        #print("Fecha actual: ", fecha_actual.strftime('%d-%m-%Y'))
        fecha_actual -= timedelta(days=1)
        if fecha_actual.weekday() < 5 and fecha_actual not in feriados:  # Lunes a viernes y no feriados
            contador += 1
    
    return fecha_actual.strftime('%d-%m-%Y')

# Ejemplo de uso
dias_habiles = 5

print(contar_dias_habiles_atras(dias_habiles))  # Salida: 2024-09-02 (puede variar según la fecha actual)
