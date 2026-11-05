import os
import time
import requests
import pandas as pd
from datetime import datetime
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CARPETA_LOCAL = r"C:\Virginia\P02 D2 - Carga de Archivo C"

def configurar_logging(empresa):
    fecha_actual = datetime.now().strftime("%d%m%Y")
    carpeta_empresa = os.path.join(CARPETA_LOCAL, "Logs", empresa.upper())
    os.makedirs(carpeta_empresa, exist_ok=True)
    log_file = os.path.join(carpeta_empresa, f"log_{fecha_actual}.log")
    
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    return carpeta_empresa


def descargar_log_directo(driver, id_archivo, nombre_archivo_tabla, carpeta_empresa):
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url_log = f"https://sap.subsidios.ministeriodesarrollosocial.gob.cl/api/descargar-log/{id_archivo}/URBANO"

    response = session.get(url_log)

    if response.status_code == 200:
        nombre_final = f"log_{nombre_archivo_tabla}"
        ruta_destino = os.path.join(carpeta_empresa, nombre_final)
        with open(ruta_destino, 'wb') as f:
            f.write(response.content)
        logging.info(f"Log descargado y guardado en: {ruta_destino}")
        return nombre_final
    else:
        logging.error(f"Error al descargar log {id_archivo}. Código: {response.status_code}")
        return None


def extraer_tabla_y_guardar_excel(driver, empresa):
    fecha = datetime.now().strftime("%d%m%Y")
    
    # Crear carpeta dinámica por empresa y configurar logging
    carpeta_empresa = configurar_logging(empresa)

    nombre_archivo = f"reporte_{empresa.lower()}_{fecha}.xlsx"
    ruta_completa = os.path.join(carpeta_empresa, nombre_archivo)

    logs_descargados = []
    data = []

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="archivosCargados"]/a'))
                                                            
        ).click()

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="listaCargaArchivos_wrapper"]/div[2]'))
            )
        except: pass

        if empresa == "ARA":
            select_element = driver.find_element(By.ID, "dt-length-0")
            dropdown = Select(select_element)
            dropdown.select_by_value("100")
            time.sleep(3)

        filas = driver.find_elements(By.XPATH, "//table[@id='listaCargaArchivos']/tbody/tr")

        for fila in filas:
            try:
                celdas = fila.find_elements(By.TAG_NAME, "td")
                if len(celdas) >= 6:
                    time.sleep(1)
                    fecha_val = celdas[0].text.strip()
                    nombre = celdas[1].text.strip()
                    total = celdas[2].text.strip()
                    errores = celdas[3].text.strip()
                    time.sleep(2)
                    data.append([fecha_val, nombre, total, errores])

                    if errores.isdigit() and int(errores) > 0:
                        boton = celdas[5].find_element(By.CLASS_NAME, "boton-secundario")
                        id_boton = boton.get_attribute("id")
                        id_archivo = id_boton.replace("descargar", "")

                        log_guardado = descargar_log_directo(driver, id_archivo, nombre, carpeta_empresa)
                        if log_guardado:
                            logs_descargados.append(log_guardado)

            except NoSuchElementException:
                logging.warning(f"No se encontró botón en fila con nombre: {nombre}")
            except Exception as e:
                logging.error(f"Error procesando fila: {e}")

        if data:
            df = pd.DataFrame(data, columns=["Fecha", "Nombre", "Total", "Errores"])
            df.to_excel(ruta_completa, index=False)
            logging.info(f"Archivo Excel generado en: {ruta_completa}")
            return nombre_archivo, logs_descargados
        else:
            logging.warning("No se encontraron datos en la tabla.")
            return None, []

    except TimeoutException as e:
        logging.error(f"Error de tiempo de espera: {e}")
        return None, []
