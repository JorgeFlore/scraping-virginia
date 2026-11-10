"""
Seguimiento de las ventanas de proceso de SGC (paso 1: validar archivo, paso 2: ejecutar carga).

Misma lógica que antes estaba dentro de carga_universo_pat.py, con estas correcciones:
  - Sin variable global screenshot_path: la captura viaja dentro de la excepción
    (ErrorCarga.screenshot), así nunca se adjunta la captura de otra empresa.
  - El reintento por ventana cerrada llamaba a comprobar_alerta() sin el parámetro
    'proceso' y fallaba siempre con TypeError. Corregido.
  - Mensajes de tiempo coherentes (90 s).
"""
import logging
import os
import time
from datetime import datetime
from time import sleep

from selenium.common.exceptions import (NoAlertPresentException, NoSuchWindowException,
                                        TimeoutException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ESPERA_MAXIMA = 90  # segundos sin avance antes de considerar el proceso congelado


class ErrorCarga(Exception):
    """Error de una empresa; puede traer la ruta de una captura de pantalla."""

    def __init__(self, mensaje, screenshot=None):
        super().__init__(mensaje)
        self.screenshot = screenshot


def capturar(driver, carpeta, motivo, empresa):
    """Guarda una captura con nombre único (empresa + motivo + hora). Devuelve la ruta o None."""
    try:
        os.makedirs(carpeta, exist_ok=True)
        ruta = os.path.join(carpeta, f"{datetime.now():%Y%m%d_%H%M%S}_{motivo}_{empresa}.png")
        driver.save_screenshot(ruta)
        return ruta
    except Exception:  # noqa: BLE001 - el navegador puede estar cerrado
        return None


def comprobar_alerta(driver, empresa, carpeta_errores, proceso):
    """Espera a que SGC abra la ventana de proceso. Si aparece un alert, es un error."""
    inicio = time.time()
    while True:
        if len(driver.window_handles) > 2:
            logging.info("[%s] Se abrió la ventana del proceso %s", empresa, proceso)
            return

        try:
            alerta = WebDriverWait(driver, 3).until(EC.alert_is_present())
            texto = alerta.text
            alerta.accept()
            sleep(2)
            msg = f"SGC mostró una alerta en el proceso {proceso}: {texto}"
            logging.error("[%s] %s", empresa, msg)
            raise ErrorCarga(msg, capturar(driver, carpeta_errores, f"alerta_p{proceso}", empresa))
        except (NoAlertPresentException, TimeoutException):
            pass
        except ErrorCarga:
            raise
        except WebDriverException:
            pass

        if time.time() - inicio > ESPERA_MAXIMA:
            msg = f"SGC no abrió la ventana del proceso {proceso} en {ESPERA_MAXIMA} s"
            logging.error("[%s] %s", empresa, msg)
            raise ErrorCarga(msg, capturar(driver, carpeta_errores, f"timeout_p{proceso}", empresa))
        sleep(1)


def _reintentar_paso(driver, proceso):
    if proceso == 1:
        sleep(5)
        driver.find_element(By.ID, "xrpnlSeleccionar_xrdbPAT_S_D").click()
        driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()
    elif proceso == 2:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "xchkSeleccionarTodos_S_D"))).click()
        sleep(2)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "xbtnEjecutar_CD"))).click()


def monitorear_proceso_archivos(driver, empresa, carpeta_errores, proceso, max_intentos=3):
    """Sigue la barra de progreso hasta que la ventana del proceso se cierra."""
    sleep(5)
    driver.switch_to.window(driver.window_handles[-1])
    anterior, sin_cambio_desde, intentos = None, None, 0

    while True:
        try:
            if len(driver.window_handles) < 3:
                logging.info("[%s] Finalizó el proceso %s", empresa, proceso)
                return

            actual = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.progress-label"))).text

            if actual != anterior:
                anterior, sin_cambio_desde = actual, time.time()
            elif time.time() - sin_cambio_desde >= ESPERA_MAXIMA:
                msg = f"El proceso {proceso} no avanza hace {ESPERA_MAXIMA} s (se presume congelado)"
                logging.error("[%s] %s", empresa, msg)
                raise ErrorCarga(msg, capturar(driver, carpeta_errores, f"congelado_p{proceso}", empresa))
            sleep(5)

        except NoSuchWindowException:
            intentos += 1
            logging.error("[%s] La ventana se cerró inesperadamente. Reintento %s/%s del proceso %s",
                          empresa, intentos, max_intentos, proceso)
            if intentos >= max_intentos:
                raise ErrorCarga(f"No se pudo recuperar la ventana del proceso {proceso} "
                                 f"en {max_intentos} intentos")
            sleep(5)
            _reintentar_paso(driver, proceso)
            comprobar_alerta(driver, empresa, carpeta_errores, proceso)  # antes faltaba 'proceso'
            driver.switch_to.window(driver.window_handles[-1])

        except TimeoutException:
            # Igual que antes: si la barra ya no existe, el proceso terminó.
            logging.info("[%s] No se encontró la barra de progreso; se asume fin del proceso %s", empresa, proceso)
            return
