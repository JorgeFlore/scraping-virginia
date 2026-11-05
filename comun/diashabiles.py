"""
Días hábiles (versión única compartida).

Reemplaza las copias de diashabiles.py que había en cada carpeta.
Misma API y mismo comportamiento que antes:
  - es_habil(d)  -> True si d no es sábado/domingo ni feriado
  - previo(d)    -> día hábil anterior a d
  - today()      -> date.today()

Único cambio: la consulta a la API de feriados tiene timeout (antes podía
quedarse colgada indefinidamente si el servidor no respondía).
"""
import json
from datetime import date, timedelta

import requests
import urllib3

# El certificado de kansas es interno (se consulta con verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FERIADOS_URL = "https://kansas.aguasnuevas.cl:8181/WebAPIIntegraciones/SOA/feriados?{anio}&{mes}&{dia}"
HEADERS = {"User-Agent": "PostmanRuntime/7.30.1"}
TIMEOUT = 30  # segundos


def es_habil(d: date = None) -> bool:
    d = d or date.today()
    if d.weekday() > 4:
        return False

    url = FERIADOS_URL.format(anio=d.year, mes=d.month, dia=d.day)
    r = requests.get(url, headers=HEADERS, verify=False, timeout=TIMEOUT)

    # La API responde con "error" cuando la fecha NO es feriado
    return "error" in json.loads(r.content)


def previo(d: date = None) -> date:
    d = d or date.today()
    delta = timedelta(days=1)
    d -= delta
    while not es_habil(d):
        d -= delta
    return d


def today(d: date = None) -> date:
    return date.today()
