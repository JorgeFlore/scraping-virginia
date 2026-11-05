import os
import time
import glob
import shutil
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# IMPORTAMOS LAS FUNCIONES DESDE edge.py Y correo.py
from edge import ruta_descargas, opciones_edge
from correo import enviar_correo

# --- FUNCIONES AUXILIARES ---
def esperar_y_renombrar(ruta_descarga, nuevo_nombre, extension=".pdf", timeout=60):
    """Espera a que aparezca un PDF en la carpeta y lo renombra."""
    archivo_encontrado = None

    for _ in range(timeout):
        archivos = glob.glob(os.path.join(ruta_descarga, f"*{extension}"))
        if archivos:
            archivo_encontrado = max(archivos, key=os.path.getctime)
            break
        time.sleep(1)

    if not archivo_encontrado:
        raise FileNotFoundError("No se encontró ningún archivo PDF descargado.")

    nuevo_path = os.path.join(ruta_descarga, nuevo_nombre + extension)
    shutil.move(archivo_encontrado, nuevo_path)
    return nuevo_path

# --- 1. CARGAMOS VARIABLES ---
load_dotenv()
EMPRESAS = ["ADA",  "ASOL"]#, "ATA", "ARA", "AXA", "AMA", "AN", "ENER"]

# --- 2. CONFIGURACIÓN DEL NAVEGADOR ---
print("Preparando la configuración del navegador...")
ruta_destino = ruta_descargas()
opciones = opciones_edge(ruta_destino)
driver_path = r"C:\\bin\\msedgedriver.exe"
service = EdgeService(driver_path)

# Carpeta de capturas
capturas_dir = os.path.join(ruta_destino, "Capturas")
os.makedirs(capturas_dir, exist_ok=True)

# --- 3. BUCLE PRINCIPAL ---
for empresa in EMPRESAS:
    print("-" * 50)
    print(f"Iniciando el proceso para la empresa: {empresa}")
    hora_inicio = datetime.datetime.now().strftime("%H:%M:%S")

    driver = webdriver.Edge(service=service, options=opciones)

    try:
        # --- 3.1 LOGIN ---
        print("Navegando a la página del SII...")
        driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")

        rut = os.getenv(f"{empresa}_RUT")
        clave = os.getenv(f"{empresa}_CLAVE")

        wait = WebDriverWait(driver, 15)
        rut_field = wait.until(EC.presence_of_element_located((By.ID, "rutcntr")))
        rut_field.send_keys(rut)

        clave_field = driver.find_element(By.ID, "clave")
        clave_field.send_keys(clave)

        driver.find_element(By.ID, "bt_ingresar").click()
        print("Inicio de sesión completado.")
        time.sleep(3)

        # --- 3.2 NAVEGACIÓN ---
        print("Buscando el documento PDF...")
        driver.get("https://palena.sii.cl/cgi_rtc/RTC/RTCCertMas.cgi")

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='TIPOCONSULTA' and @value='0']"))).click()

        hoy = datetime.date.today()
        fecha_desde = (hoy - datetime.timedelta(days=5)).strftime("%d%m%Y")
        fecha_hasta = hoy.strftime("%d%m%Y")

        desde = driver.find_element(By.NAME, "DESDE")
        desde.clear()
        desde.send_keys(fecha_desde)
        driver.find_element(By.NAME, "Submit").click()

        wait.until(EC.presence_of_element_located((By.NAME, "chkAll"))).click()
        driver.find_element(By.NAME, "genera").click()

        # --- 3.2.1 VERIFICAR ERROR SERVICE UNAVAILABLE ---
        try:
            h1_text = driver.find_element(By.TAG_NAME, "h1").text
            if "Service Unavailable" in h1_text:
                print("Servicio no disponible, recargando la página...")
                driver.refresh()
                time.sleep(3)
                driver.find_element(By.NAME, "genera").click()
        except:
            pass

        # --- 3.3 CAPTURA O PDF ---
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Imprimir')]"))).click()
        except:
            screenshot_path = os.path.join(capturas_dir, f"{empresa}_{fecha_hasta}.png")
            driver.save_screenshot(screenshot_path)
            print(f"⚠️ No se encontró PDF para {empresa}, captura guardada en: {screenshot_path}")
            hora_fin = datetime.datetime.now().strftime("%H:%M:%S")

            enviar_correo(
                empresa,
                screenshot_path,
                datetime.datetime.strptime(fecha_desde, "%d%m%Y").strftime("%d-%m-%Y"),
                datetime.datetime.strptime(fecha_hasta, "%d%m%Y").strftime("%d-%m-%Y"),
                rut,
                hora_inicio,
                hora_fin,
                hay_cesiones=False
            )
            continue

        print("Descarga iniciada. Esperando a que termine...")
        time.sleep(10)

        # --- 3.4 RENOMBRAR PDF ---
        rut_sanitizado = rut.replace(".", "").replace("-", "")
        nuevo_nombre = f"CESIONES_{rut_sanitizado}_0_{fecha_desde}_{fecha_hasta}"
        ruta_pdf = esperar_y_renombrar(ruta_destino, nuevo_nombre)

        print(f"✅ Archivo guardado como: {ruta_pdf}")
        hora_fin = datetime.datetime.now().strftime("%H:%M:%S")

        enviar_correo(
            empresa,
            ruta_pdf,
            datetime.datetime.strptime(fecha_desde, "%d%m%Y").strftime("%d-%m-%Y"),
            datetime.datetime.strptime(fecha_hasta, "%d%m%Y").strftime("%d-%m-%Y"),
            rut,
            hora_inicio,
            hora_fin,
            hay_cesiones=True
        )

    except Exception as e:
        print(f"❌ Ocurrió un error al procesar {empresa}: {e}")

    finally:
        driver.quit()
        print(f"Cerrando navegador para {empresa}...")
        print("-" * 50)

print("✅ Script finalizado. Todas las empresas procesadas.")
