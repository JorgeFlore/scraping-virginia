from time import sleep
import time
from selenium.webdriver.common.by import By
from utils import chrome
from utils import envio_correo
from utils.iniciar_sesion import cargar_pagina, verificar_contenido_pagina_inicial, inicar_sesion
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, ElementNotInteractableException, NoSuchElementException, TimeoutException, WebDriverException, NoSuchWindowException, ElementClickInterceptedException

import os
import shutil
from os import remove
from bs4 import BeautifulSoup
import pandas as pd
import os.path as path
import datetime
import logging

captura_fecha = datetime.datetime.now()
fecha_carpeta=captura_fecha.strftime('%d-%m-%Y')
ruta_descarga_archivos=chrome.ruta_descargas()
errores_PAT = os.path.join(ruta_descarga_archivos, "errores_PAT")
screenshot_path = None

ruta_archivos_procesados = os.path.join(ruta_descarga_archivos, "procesados", fecha_carpeta)

listado_empresas=['96703230_1_TBUNIVERSO.TXT','76850128_9_TBUNIVERSO.TXT','76215637_7_TBUNIVERSO.TXT','76215628_8_TBUNIVERSO.TXT','76215634_2_TBUNIVERSO.TXT']

url = "https://sgc-araqa.aguasnuevas.cl/"
user = "99999111-4"
password = os.getenv("SGC_PASSWORD")


if os.path.isdir(ruta_archivos_procesados):
    shutil.rmtree(ruta_archivos_procesados)


def get_empresa(key):
    empresas = {
        "76215634_2_TBUNIVERSO.TXT": "Aguas del Altiplano",
        # "76850128_9_TBUNIVERSO.TXT": "Nueva Atacama",
        "76215637_7_TBUNIVERSO.TXT": "Aguas Araucanía",
        "76215628_8_TBUNIVERSO.TXT": "Aguas Magallanes",
        # "96703230_1_TBUNIVERSO.TXT": "Aguas Décima"
    }
    return empresas.get(key, "Empresa Desconocida")  


def procesar_archivos(driver, empresa, errores_PAT):

    try:
        sleep(10)
        driver.find_element(By.ID, 'xrpnlSeleccionar_xrdbPAT_S_D').click()
        driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()
        
        max_wait_time = 60
        start_time = time.time()

        while True:
            try:
                if len(driver.window_handles) > 2:
                    print("Se ingresa a pestaña para procesar los archivos")
                    logging.info("Se ingresa a pestaña para procesar los archivos")
                    break

                # Verificar si hay una alerta
                try:
                    alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
                    print(f"Se detectó un alert")
                    alert.accept()
                    print("Alerta cerrada exitosamente.")
                    sleep(2)
                    raise Exception(f"Se detectó una alerta durante la ejecución de {empresa}. La ejecución se ha detenido.")
                
                except (NoAlertPresentException, TimeoutException, WebDriverException):
                    print("No hay alertas activas")

                # Verificar tiempo de espera máximo
                if time.time() - start_time > max_wait_time:
                    print(f"Se alcanzó el tiempo máximo de espera en el proceso de {empresa}. La ejecución se ha detenido.")
                    screenshot_path = os.path.join(errores_PAT, "screenshot_timeout.png")
                    driver.save_screenshot(screenshot_path)
                    raise Exception(f"Se alcanzó el tiempo máximo de espera en el proceso de {empresa}. La ejecución se ha detenido.")
                
                sleep(1)

            except Exception as e:
                screenshot_path = os.path.join(errores_PAT, "screenshot_modal_detected.png")
                driver.save_screenshot(screenshot_path)
                print(f"Error al verificar el estado del proceso: {str(e)}")
                raise Exception(f"Error al verificar el estado del proceso de archivos")

    except Exception as e:
        print(f"Error en procesar_archivos: {str(e)}")
        raise Exception(f"Error crítico en procesar_archivos: {str(e)}")



def guardar_excel(driver, ruta_archivos_procesados, empresa, i, max_intentos=3):
    intentos = 0
    
    while intentos < max_intentos:
        try:
            tabla_universo = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'xgrwResultadoUniverso_DXMainTable'))
            )
            print("Tabla universo cargada correctamente.")
            logging.info("Tabla universo cargada correctamente")

            html = driver.execute_script("return arguments[0].innerHTML;", tabla_universo)
            soup = BeautifulSoup(html, 'html.parser')
            tbody = soup.find('tbody')

            lista_banco = []
            lista_nombre_archivo = []
            lista_leidos = []
            lista_rechazados = []
            lista_aceptados = []
            lista_resultados = []

            for l in tbody.find_all('tr'):    
                columna = l.find_all('td')
                if columna:
                    lista_banco.append(columna[0].text.strip())
                    lista_nombre_archivo.append(columna[1].text.strip())
                    lista_leidos.append(columna[2].text.strip())
                    lista_rechazados.append(columna[3].text.strip())
                    lista_aceptados.append(columna[4].text.strip())
                    lista_resultados.append(columna[5].text.strip())

            dicionario = {
                "banco": lista_banco, 
                "nombre_archivo": lista_nombre_archivo, 
                "leidos": lista_leidos, 
                "rechazados": lista_rechazados, 
                "aceptados": lista_aceptados, 
                "resultados": lista_resultados
            }

            archivos_antes = len(os.listdir(ruta_archivos_procesados))


            df = pd.DataFrame(dicionario)
            ruta_excel = os.path.join(ruta_archivos_procesados, i[0:21] + ".xlsx")

            df.to_excel(ruta_excel, index=False, engine='openpyxl')

            archivo_despues = len(os.listdir(ruta_archivos_procesados))
            if archivos_antes == archivo_despues:
                raise Exception("No se encontro archivo excel en la caperta de descarga")
            
            logging.info(f"Archivo Excel de la empresa {empresa} procesado correctamente en intento {intentos + 1}")
            print(f"Archivo Excel de la empresa {empresa} generado con éxito.")
            return True 
        
        except Exception as e:
            intentos += 1
            logging.warning(f"Error en el intento {intentos}/{max_intentos} al procesar la tabla para {empresa}. Error: {e}")
            print(f"Error en el intento {intentos}/{max_intentos} al procesar la tabla para {empresa}. Reintentando...")
            sleep(5) 
            
    mensaje = f"Se ha detectado un problema al procesar la tabla universo y generar el archivo Excel para la empresa {empresa} después de {max_intentos} intentos."
    logging.error(mensaje)
    envio_correo.correo(mensaje, empresa)


log_filname = "Log.log"
logging.basicConfig(
    filename=log_filname,
    level=logging.INFO,
    filemode="w",
    datefmt="%d-%m-%Y %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(message)s"
)


for i in listado_empresas:

    if path.exists(ruta_descarga_archivos+"TBUNIVERSO.TXT"):
        remove(ruta_descarga_archivos+"TBUNIVERSO.TXT")
    if os.path.isdir(ruta_archivos_procesados):
        
       print("directorio existente")
    else:
        os.mkdir(ruta_archivos_procesados)
    
    try:
        empresa = get_empresa(i)
        
        if empresa == "Empresa Desconocida":
            print(f"No se encontro la empresa con identificador {i}")
            continue
        
        print(f"\nEmpresa ejecutandose {empresa}")
        
        driver = cargar_pagina(
            driver_options=chrome.opciones_chrome,
            url=url,
            # url="https://sgc-ara.aguasnuevas.cl/",
            empresa=empresa
        )
        sleep(3)

        driver = verificar_contenido_pagina_inicial(
            driver=driver,
            driver_options=chrome.opciones_chrome,
            url=url,
            empresa=empresa
        )
        
        if not driver:
            logging.error(f"La página de la empresa {empresa} no logro cargar correctamente")
            
            mensaje = f"ERROR: La pagina de la empresa '{empresa}' no cargó correctamente. Continuando con la siguiente empresa.. "
            print(mensaje)
            envio_correo.correo(mensaje, empresa)
            continue
        
        sleep(5)
        try:
            select_empresa = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, f"//td[text()='{empresa}']")))
            select_empresa.click()
            logging.info(f"Seleccionada la empresa {empresa} correctamente.")
        
        except (NoSuchElementException, ElementNotInteractableException, TimeoutException):
            logging.info(f"No se puede seleccionar la empresa {empresa} no esta disponible en el selector")
            print(f"No se puede seleccionar la empresa {empresa}, no esta disponible en el selector")
            driver.quit()
            continue

        except Exception as e:
            logging.error(f"Error inesperado al seleccionar la empresa {empresa}: {str(e)}")
            print(f"Error inesperado al seleccionar la empresa {empresa}: {str(e)}")
            driver.quit()
            continue

        driver = inicar_sesion(
            driver = driver,
            user = user,
            password = password,
        )

        if not driver:
            mensaje =f"No se logro iniciar sesion correctamente en la empresa: {empresa}"
            print(mensaje)
            logging.error(mensaje)
            envio_correo.correo(mensaje, empresa)
            continue

        sleep(5)

        opciones_recaudacion=(
            '//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1_T"]/span',
            '//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1i2_T"]',
            '//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1i2i0_T"]/span'
        )

        max_reintentos = 3
        intento = 0

        while intento < max_reintentos:
            try:
                print(f"Intento {intento + 1} de {max_reintentos}: Ingresando las opciones...")

                for j in opciones_recaudacion:
                    elemento = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, j)))
                    elemento.click()
                    sleep(2)

                print("Se ingresaron las opciones correctamente")
                break 

            except (TimeoutException, ElementClickInterceptedException) as e:
                print(f"Error al intentar hacer clic en una opción: {e}")
                driver.refresh()  
                sleep(5)  
                intento += 1

        if intento == max_reintentos:
            raise Exception("No se pudo ingresar a las opciones después de varios intentos.")

        
        sleep(7)
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        sleep(7)        
        archivo = WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH, '//*[@id="UploadFile_TextBox0_Input"]')))
        sleep(7) 
        shutil.copy(os.path.join(ruta_descarga_archivos, i), os.path.join(ruta_archivos_procesados, i))
        sleep(7) 
        shutil.copy(os.path.join(ruta_descarga_archivos, i), os.path.join(ruta_descarga_archivos, "TBUNIVERSO.TXT"))
        sleep(7) 
        # remove(os.path.join(ruta_descarga_archivos, i))
        
        ruta=os.path.abspath(ruta_descarga_archivos+"\\TBUNIVERSO.TXT")
        archivo.send_keys(ruta)

        procesar_archivos(driver,empresa, errores_PAT)

        # sleep(10)
        # check=driver.find_element(By.ID, 'xrpnlSeleccionar_xrdbPAT_S_D').click()
        
        # siguiente=driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()
        
        # max_wait_time = 60
        # start_time = time.time()

        # while True:
            # try:
            #     if len(driver.window_handles) > 2:
            #         print("Se ingresa a pestaña para procesar los archivos")
            #         logging.info("Se ingresa a pestaña para procesar los archivos")
            #         break

            #     try:
            #         alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
            #         print(f"Se detectó un alert")
            #         alert.accept() 
            #         print("Alerta cerrada exitosamente.")
            #         sleep(2)
            #         raise Exception(f"Se detecto una alerta durante la ejecucion de {empresa}. La ejecucion se ha detenido.") 
                    
            #     except (NoAlertPresentException, TimeoutException, WebDriverException):
            #         print("No hay alertas activas")
                
            #     if time.time() - start_time > max_wait_time:
            #         print(f"Se alcanzó el tiempo máximo de espera en el proceso de {empresa}. La ejecución se ha detenido.")
            #         screenshot_path = os.path.join(errores_PAT, "screenshot_timeout.png")
            #         driver.save_screenshot(screenshot_path)
            #         raise Exception(f"Se alcanzo el tiempo maximo de espera en el proceso de {empresa}. La ejecucion se ha detenido.")
                
            #     sleep(1)
            
            # except Exception as e:
            #     screenshot_path = os.path.join(errores_PAT, "screenshot_modal_detected.png")
            #     driver.save_screenshot(screenshot_path)
            #     print(f"Error al verificar el estado del proceso: {str(e)}")
            #     raise Exception(f"{str(e)}")
        
        sleep(3)
        max_wait_time = 60
        start_time = time.time()
        driver.switch_to.window(driver.window_handles[-1])
       
        proceso_anterior, unchanged_start_time = None, None

        while True:
            try:
                if len(driver.window_handles) < 3:
                    print("Finaliza 1er proceso de archivos")
                    break
                
                proceso_actual = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.progress-label"))).text
                # print("Elemento encontrado:", proceso_actual)

                if proceso_anterior is not None:
                    if proceso_actual == proceso_anterior:
                        # print("Proceso anterior y actual son iguales")
                        
                        if unchanged_start_time is None:
                            unchanged_start_time = time.time()
                            # print("Iniciando contador de congelamiento...")
                        else:
                            elapsed = time.time() - unchanged_start_time
                            print(f"Tiempo transcurrido sin cambio: {elapsed:.2f} segundos")

                            if elapsed >= max_wait_time:
                                print("El proceso se ha congelado por 60 segundos, saliendo... ")
                                raise Exception("El proceso se ha congelado por 60 segundos: Se presunta un congelamiento en el proceso de archivos")
                    else:
                        # print("El proceso ha cambiando, reseteando contador...")
                        proceso_anterior = proceso_actual
                        unchanged_start_time = None
                else:
                    # print("Primera iteración, estableciendo proceso anterior.")
                    proceso_anterior = proceso_actual
                    unchanged_start_time = None

                sleep(1)
            except NoSuchWindowException:
                print("La ventana se cerró inesperadamente.")
                procesar_archivos(driver, empresa, errores_PAT)
                 
            
            except TimeoutException:
                print("No se encontró el elemento en el tiempo esperado.")
                break   
        try:
            driver.switch_to.window(driver.window_handles[-1])
        except Exception as e:
            print(f"Error al cambiar de ventana: {e}")
            raise

        guardar_excel(driver, ruta_archivos_procesados, empresa, i)

        seleccionar = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, 'xchkSeleccionarTodos_S_D')))
        seleccionar.click()
        sleep(2)
        ejecutar= WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, 'xbtnEjecutar_CD')))
        ejecutar.click()    
        sleep(2)    
        boton_aceptar = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="xbtnAceptar"]')))
        boton_aceptar.click()        
        sleep(10)
        driver.switch_to.window(window_before)
        sleep(10)
        salir=driver.find_element(By.XPATH, '//*[@id="ctl00_barra_superior"]/img[2]').click()
        
        if path.exists(ruta_descarga_archivos+"\\TBUNIVERSO.TXT"):
            remove(ruta_descarga_archivos+"\\TBUNIVERSO.TXT")
        
        mensaje = f"Empresa: {empresa} ha sido procesada correctamente"
        envio_correo.correo(mensaje, empresa)
        sleep(10)
        driver.quit()
        sleep(5)
        
    except Exception as e:
        logging.critical(f"No se pudo completar el proceso de la empresa {empresa}")

        print(f"Error global {str(e)}")
        driver.quit()
        sleep(5)
        mensaje=f"No se pudo completar el procesamiento de la empresa {empresa} debido al siguiente error: {str(e)}."
        envio_correo.correo(mensaje, empresa, screenshot_path)
        pass

# driver.quit()