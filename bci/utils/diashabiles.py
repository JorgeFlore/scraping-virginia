from datetime import (date, timedelta)
import urllib3
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# import ssl_verify

http = urllib3.PoolManager()

headers = {"User-Agent": "PostmanRuntime/7.30.1"}


from datetime import date
import requests
import json
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FERIADOS_LOCAL = r"C:\Scraping\informacion_de_pago\bci\utils\feriados.json"  # ajusta ruta a tu entorno

def es_habil(d: date = date.today()) -> bool:
    """Retorna True si la fecha es hábil (ni fin de semana ni feriado)."""
    
    # Si es sábado o domingo → no hábil
    if d.weekday() > 4:
        return False

    # --- 1️⃣ Intentar API ---
    url = f"https://kansas.aguasnuevas.cl:8181/WebAPIIntegraciones/SOA/feriados?anio={d.year}&mes={d.month}&dia={d.day}"
    try:
        r = requests.get(url, headers={"User-Agent": "PostmanRuntime/7.30.1"}, verify=False, timeout=5)
        data = r.json()
        return not data.get("esFeriado", False)
    except Exception as e:
        print(f"[WARN] No se pudo consultar API de feriados: {e}")
    
    # --- 2️⃣ Si falla la API, usar JSON local ---
    if os.path.exists(FERIADOS_LOCAL):
        try:
            with open(FERIADOS_LOCAL, "r", encoding="utf-8") as f:
                feriados = json.load(f)
            feriados_anio = feriados.get(str(d.year), [])
            return d.isoformat() not in feriados_anio
        except Exception as e:
            print(f"[ERROR] No se pudo leer feriados locales: {e}")
    
    # --- 3️⃣ Si todo falla, asumir que es hábil ---
    return True



def previo(d: date = date.today()) -> date:
    delta = timedelta(days=10)

    d -= delta
    while not es_habil(d):
        d -= delta

    return d
