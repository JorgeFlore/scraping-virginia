from datetime import date, timedelta
import json
import requests

from datetime import date
import requests
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FERIADOS_LOCAL = r"C:\Scraping\Envio correo informacion Pago BCI\utils\feriados.json"  # ajusta ruta a tu entorno

from datetime import date, timedelta
import json
import os

FERIADOS_LOCAL = r"C:\Users\jorge.flores\Documents\GitHub\Aws_scraping_conciliacion_bancaria\utils\feriados.json"  # ajusta ruta a tu entorno

def es_habil(d: date = date.today()) -> bool:
    """Retorna True si la fecha es hábil (ni fin de semana ni feriado)."""

    # Si es sábado o domingo → no hábil
    if d.weekday() > 4:
        return False

    # --- Usar JSON local de feriados ---
    if os.path.exists(FERIADOS_LOCAL):
        try:
            with open(FERIADOS_LOCAL, "r", encoding="utf-8") as f:
                feriados = json.load(f)
            feriados_anio = feriados.get(str(d.year), [])
            # Si la fecha está en la lista → es feriado (no hábil)
            return d.isoformat() not in feriados_anio
        except Exception as e:
            print(f"[ERROR] No se pudo leer feriados locales: {e}")
            # Si falla la lectura, asumimos que es hábil
            return True
    else:
        print(f"[WARN] No se encontró archivo de feriados en: {FERIADOS_LOCAL}")
        return True


def previo(d: date = date.today()) -> date:
    delta = timedelta(days=1)

    d -= delta
    while not es_habil(d):
        d -= delta

    return d
