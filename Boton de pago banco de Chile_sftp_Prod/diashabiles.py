"""
Determina si una fecha es día hábil usando la API interna de feriados.
"""
import json
import logging
import time
from datetime import date, timedelta

import requests
import urllib3

import config

log = logging.getLogger(__name__)

if not config.FERIADOS_VERIFICAR_SSL:
    # El certificado de kansas es interno: se evita ensuciar el log con la advertencia
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {"User-Agent": "PostmanRuntime/7.30.1"}


class ErrorFeriados(Exception):
    """No se pudo consultar la API de feriados."""


def _consultar_api(d: date):
    url = config.FERIADOS_URL.format(anio=d.year, mes=d.month, dia=d.day)
    ultimo_error = None
    for intento in range(1, config.FERIADOS_REINTENTOS + 1):
        try:
            r = requests.get(
                url,
                headers=HEADERS,
                verify=config.FERIADOS_VERIFICAR_SSL,
                timeout=config.FERIADOS_TIMEOUT,
            )
            return json.loads(r.content)
        except (requests.RequestException, ValueError) as e:
            ultimo_error = e
            log.warning("API feriados intento %s/%s falló: %s", intento, config.FERIADOS_REINTENTOS, e)
            if intento < config.FERIADOS_REINTENTOS:
                time.sleep(3)
    raise ErrorFeriados(f"No se pudo consultar la API de feriados para {d}: {ultimo_error}")


def es_feriado(d: date) -> bool:
    # La API responde con "error" cuando la fecha NO es feriado (comportamiento original)
    return "error" not in _consultar_api(d)


def es_habil(d: date = None) -> bool:
    d = d or date.today()
    if d.weekday() > 4:
        return False
    return not es_feriado(d)


def previo(d: date = None) -> date:
    """Día hábil anterior a d."""
    d = d or date.today()
    for _ in range(15):
        d -= timedelta(days=1)
        if es_habil(d):
            return d
    raise ErrorFeriados("No se encontró un día hábil en los 15 días anteriores")
