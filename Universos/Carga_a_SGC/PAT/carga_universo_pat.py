"""
Carga del Universo PAT a SGC (https://sgc-ade.aguasnuevas.cl/).

Por cada empresa toma <RUT>_TBUNIVERSO.TXT desde la carpeta compartida, lo carga en SGC
(Recaudación > PAT), guarda el Excel de resultados en procesados/<fecha>/ y avisa por correo.

Los pasos en SGC (clics, ventanas, esperas) son los mismos de la versión anterior.
Cambios respecto a la versión anterior:
  - Ya NO se borra la carpeta procesados/<hoy> al iniciar (una segunda ejecución en el
    mismo día eliminaba el único respaldo de los archivos ya cargados).
  - El archivo original solo se elimina cuando SGC ya lo recibió. Si falla antes
    (página, login, menú), el archivo queda en su lugar y se reintenta en la próxima ejecución.
  - Si no llegó el archivo de una empresa, no se abre el navegador: se avisa directamente.
    Si la empresa ya se cargó hoy, no se envía aviso.
  - Un error en una empresa ya no detiene a las siguientes (driver.quit() protegido,
    sin exit() al fallar la página).
  - Captura de pantalla por empresa con nombre único (antes se podía adjuntar la de otra empresa).
  - Bloqueo para que no corran dos ejecuciones al mismo tiempo (evita cargas duplicadas).
  - Log diario en logs/ que no se sobrescribe, y correo final con el resumen de las 5 empresas.
  - Sin esperas fijas innecesarias al copiar archivos (~20 s menos por empresa).
"""
import json
import logging
import os
import shutil
import sys
from datetime import datetime
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import chrome, envio_correo
from utils.guardar_excel import guardar_excel
from utils.iniciar_sesion import (cargar_pagina, cerrar, inicar_sesion, seleccionar_empresa,
                                  verificar_contenido_pagina_inicial)
from utils.opciones_recaudacion import ingresar_opciones_recaudacion
from utils.proceso import ErrorCarga, capturar, comprobar_alerta, monitorear_proceso_archivos

# ------------------------------------------------------------------ configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL = "https://sgc-ade.aguasnuevas.cl/"
USUARIO = os.getenv("SGC_RUT", "99999111-4")
CLAVE = os.getenv("SGC_PASSWORD")

# Archivo -> nombre de la empresa en SGC (mismo orden de carga que antes)
EMPRESAS = {
    "96703230_1_TBUNIVERSO.TXT": "Aguas Décima",
    "76215634_2_TBUNIVERSO.TXT": "Aguas del Altiplano",
    "76850128_9_TBUNIVERSO.TXT": "Nueva Atacama",
    "76215637_7_TBUNIVERSO.TXT": "Aguas Araucanía",
    "76215628_8_TBUNIVERSO.TXT": "Aguas Magallanes",
}

RUTA = chrome.ruta_descargas()                       # \\columbia\...\Universos\PAT\
HOY = datetime.now()
RUTA_PROCESADOS = os.path.join(RUTA, "procesados", HOY.strftime("%d-%m-%Y"))
RUTA_ERRORES = os.path.join(RUTA, "errores_PAT")
ARCHIVO_CARGA = os.path.join(RUTA, "TBUNIVERSO.TXT")  # SGC espera este nombre
ESTADO = os.path.join(RUTA_PROCESADOS, "estado.json")
LOG_DIR = os.path.join(BASE_DIR, "logs")
BLOQUEO = os.path.join(LOG_DIR, "carga_pat.lock")
BLOQUEO_HORAS = 4


# ------------------------------------------------------------------ utilidades
def configurar_log():
    os.makedirs(LOG_DIR, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d-%m-%Y %H:%M:%S")
    raiz = logging.getLogger()
    raiz.setLevel(logging.INFO)
    for h in (logging.FileHandler(os.path.join(LOG_DIR, f"carga_pat_{HOY:%Y-%m-%d}.log"), encoding="utf-8"),
              logging.StreamHandler()):
        h.setFormatter(fmt)
        raiz.addHandler(h)


def tomar_bloqueo():
    """Evita dos ejecuciones simultáneas (tarea programada + ejecución manual)."""
    if os.path.exists(BLOQUEO):
        edad_h = (datetime.now().timestamp() - os.path.getmtime(BLOQUEO)) / 3600
        if edad_h < BLOQUEO_HORAS:
            return False
        logging.warning("Bloqueo antiguo (%.1f h) encontrado; se reemplaza", edad_h)
    with open(BLOQUEO, "w") as f:
        f.write(f"{os.getpid()} {datetime.now():%Y-%m-%d %H:%M:%S}")
    return True


def leer_estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return {}


def guardar_estado(archivo, estado, detalle=""):
    datos = leer_estado()
    datos[archivo] = {"estado": estado, "hora": datetime.now().strftime("%H:%M:%S"), "detalle": detalle}
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def respaldar(origen, archivo):
    """Copia el archivo a procesados/<hoy>/ sin pisar un respaldo anterior del mismo día."""
    destino = os.path.join(RUTA_PROCESADOS, archivo)
    if os.path.exists(destino):
        base, ext = os.path.splitext(archivo)
        destino = os.path.join(RUTA_PROCESADOS, f"{base}_{datetime.now():%H%M%S}{ext}")
    shutil.copy2(origen, destino)
    return destino


def borrar(ruta):
    try:
        if os.path.exists(ruta):
            os.remove(ruta)
    except Exception as e:  # noqa: BLE001
        logging.warning("No se pudo borrar %s: %s", ruta, e)


# ------------------------------------------------------------------ una empresa
def procesar_empresa(archivo, empresa):
    """Devuelve (estado, detalle). estado: ok | error | sin_archivo | ya_cargado."""
    origen = os.path.join(RUTA, archivo)

    if not os.path.exists(origen):
        if leer_estado().get(archivo, {}).get("estado") == "ok":
            logging.info("[%s] Ya se cargó hoy; no hay archivo nuevo.", empresa)
            return "ya_cargado", "Ya cargado hoy"
        msg = f"No se encontró el archivo {archivo} en la carpeta de Universos PAT. No se realizó la carga."
        logging.warning("[%s] %s", empresa, msg)
        envio_correo.correo(msg, empresa)
        return "sin_archivo", "No llegó el archivo"

    driver, enviado_a_sgc = None, False
    try:
        logging.info("[%s] Inicio de carga", empresa)
        driver = cargar_pagina(chrome.opciones_chrome, URL, empresa)
        if driver is None:
            raise ErrorCarga("No se pudo abrir la página de SGC")
        sleep(3)

        driver = verificar_contenido_pagina_inicial(driver, chrome.opciones_chrome, URL, empresa)
        if driver is None:
            raise ErrorCarga("La página de SGC no cargó correctamente")

        if not seleccionar_empresa(driver, empresa):
            driver = None  # seleccionar_empresa ya cerró el navegador
            raise ErrorCarga(f"No se pudo seleccionar la empresa {empresa} en SGC")

        driver = inicar_sesion(driver=driver, user=USUARIO, password=CLAVE,
                               driver_options=chrome.opciones_chrome, url=URL, empresa=empresa)
        if driver is None:
            raise ErrorCarga("No se pudo iniciar sesión en SGC")
        sleep(5)

        ingresar_opciones_recaudacion(driver)
        sleep(7)
        ventana_principal = driver.window_handles[0]
        driver.switch_to.window(driver.window_handles[1])
        sleep(7)
        campo_archivo = WebDriverWait(driver, 500).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="UploadFile_TextBox0_Input"]')))

        respaldo = respaldar(origen, archivo)
        shutil.copy2(origen, ARCHIVO_CARGA)
        logging.info("[%s] Respaldo en %s", empresa, respaldo)

        campo_archivo.send_keys(os.path.abspath(ARCHIVO_CARGA))
        sleep(10)
        driver.find_element(By.ID, "xrpnlSeleccionar_xrdbPAT_S_D").click()
        driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()
        enviado_a_sgc = True  # desde aquí SGC ya recibió el archivo

        # Paso 1: validación del archivo
        comprobar_alerta(driver, empresa, RUTA_ERRORES, 1)
        monitorear_proceso_archivos(driver, empresa, RUTA_ERRORES, 1)
        WebDriverWait(driver, 10).until(lambda w: len(w.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        excel_ok = guardar_excel(driver, RUTA_PROCESADOS, empresa, archivo)

        # Paso 2: ejecutar la carga
        WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "xchkSeleccionarTodos_S_D"))).click()
        sleep(2)
        WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "xbtnEjecutar_CD"))).click()
        sleep(2)
        comprobar_alerta(driver, empresa, RUTA_ERRORES, 2)
        monitorear_proceso_archivos(driver, empresa, RUTA_ERRORES, 2)
        WebDriverWait(driver, 10).until(lambda w: len(w.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        sleep(2)
        WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="xbtnAceptar"]'))).click()
        sleep(10)
        driver.switch_to.window(ventana_principal)
        try:
            driver.find_element(By.XPATH, '//*[@id="ctl00_barra_superior"]/img[2]').click()  # salir
        except Exception as e:  # noqa: BLE001 - la carga ya terminó; no es motivo de error
            logging.warning("[%s] No se pudo cerrar sesión en SGC: %s", empresa, e)

        borrar(origen)
        detalle = "Cargado" if excel_ok else "Cargado (no se pudo generar el Excel de resultados)"
        guardar_estado(archivo, "ok", detalle)
        mensaje = f"Empresa: {empresa} ha finalizado su proceso"
        if not excel_ok:
            mensaje += ". Atención: no se pudo generar el Excel de resultados."
        envio_correo.correo(mensaje, empresa)
        logging.info("[%s] %s", empresa, detalle)
        sleep(2)
        return "ok", detalle

    except Exception as e:  # noqa: BLE001 - se informa y se sigue con la siguiente empresa
        captura = getattr(e, "screenshot", None) or (capturar(driver, RUTA_ERRORES, "error", empresa) if driver else None)
        mensaje = f"No se pudo completar el procesamiento de la empresa {empresa} debido al siguiente error: {e}."
        if enviado_a_sgc:
            # SGC ya recibió el archivo: se retira de la carpeta (como antes) para no cargarlo dos veces.
            borrar(origen)
            mensaje += (" El archivo YA había sido enviado a SGC: revise en SGC antes de volver a cargarlo."
                        " El respaldo está en la carpeta procesados.")
        else:
            mensaje += " El archivo quedó en la carpeta y se volverá a intentar en la próxima ejecución."
        logging.error("[%s] %s", empresa, mensaje)
        guardar_estado(archivo, "error", str(e))
        envio_correo.correo(mensaje, empresa, captura)
        return "error", str(e)

    finally:
        cerrar(driver)
        borrar(ARCHIVO_CARGA)
        sleep(5)


# ------------------------------------------------------------------ principal
def main():
    configurar_log()
    if not CLAVE:
        logging.critical("Falta la variable de entorno SGC_PASSWORD")
        envio_correo.correo("No se ejecutó la carga: falta la variable de entorno SGC_PASSWORD.", "Resumen")
        return 1
    if not tomar_bloqueo():
        logging.warning("Ya hay una carga en ejecución (bloqueo %s). Se cancela esta ejecución.", BLOQUEO)
        return 0

    try:
        os.makedirs(RUTA_PROCESADOS, exist_ok=True)
        os.makedirs(RUTA_ERRORES, exist_ok=True)
        borrar(ARCHIVO_CARGA)  # restos de una ejecución interrumpida

        resultados = {}
        for archivo, empresa in EMPRESAS.items():
            resultados[empresa] = procesar_empresa(archivo, empresa)

        etiquetas = {"ok": "✅ Cargado", "error": "❌ Error", "sin_archivo": "⚠️ Sin archivo", "ya_cargado": "ℹ️ Ya cargado hoy"}
        filas = "".join(f"<tr><td>{emp}</td><td>{etiquetas[est]}</td><td>{det}</td></tr>"
                        for emp, (est, det) in resultados.items())
        resumen = ("Resumen de la carga del Universo PAT:<br><table border='1' cellspacing='0' cellpadding='4'>"
                   f"<tr><th>Empresa</th><th>Estado</th><th>Detalle</th></tr>{filas}</table>")
        if any(est != "ya_cargado" for est, _ in resultados.values()):
            envio_correo.correo(resumen, "Resumen")
        logging.info("Fin. %s", {k: v[0] for k, v in resultados.items()})
        return 0 if all(est in ("ok", "ya_cargado") for est, _ in resultados.values()) else 2
    finally:
        borrar(BLOQUEO)


if __name__ == "__main__":
    sys.exit(main())
