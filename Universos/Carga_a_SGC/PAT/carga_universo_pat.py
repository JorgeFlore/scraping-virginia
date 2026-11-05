from time import sleep
import time
from selenium.webdriver.common.by import By
from utils import chrome
from utils import envio_correo
from utils.iniciar_sesion import cargar_pagina, verificar_contenido_pagina_inicial, inicar_sesion, seleccionar_empresa
from utils.opciones_recaudacion import ingresar_opciones_recaudacion
# from utils.proceso import monitorear_proceso_archivos, comprobar_alerta
from utils.guardar_excel import guardar_excel
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, WebDriverException, NoSuchWindowException, ElementClickInterceptedException
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, WebDriverException

import os
import shutil
from os import remove
import datetime
import logging
from os import path

captura_fecha = datetime.datetime.now()
fecha_carpeta=captura_fecha.strftime('%d-%m-%Y')
ruta_descarga_archivos=chrome.ruta_descargas()
errores_PAT = os.path.join(ruta_descarga_archivos, "errores_PAT")
screenshot_path = None

ruta_archivos_procesados = os.path.join(ruta_descarga_archivos, "procesados", fecha_carpeta)

listado_empresas=['96703230_1_TBUNIVERSO.TXT', '76215634_2_TBUNIVERSO.TXT','76850128_9_TBUNIVERSO.TXT','76215637_7_TBUNIVERSO.TXT','76215628_8_TBUNIVERSO.TXT']
#'96703230_1_TBUNIVERSO.TXT','76850128_9_TBUNIVERSO.TXT','76215637_7_TBUNIVERSO.TXT','76215628_8_TBUNIVERSO.TXT'

url = "https://sgc-ade.aguasnuevas.cl/"
user = "99999111-4"
password = os.getenv("SGC_PASSWORD")

log_filname = "Log.log"
logging.basicConfig(
    filename=r"C:\Scraping\Universos\Carga_a_SGC\PAT\Log.log",
    level=logging.INFO,
    filemode="w",
    datefmt="%d-%m-%Y %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(message)s"
)



if os.path.isdir(ruta_archivos_procesados):
    shutil.rmtree(ruta_archivos_procesados)


def get_empresa(key):
    empresas = {
        "76215634_2_TBUNIVERSO.TXT": "Aguas del Altiplano",
        "76850128_9_TBUNIVERSO.TXT": "Nueva Atacama",
        "76215637_7_TBUNIVERSO.TXT": "Aguas Araucanía",
        "76215628_8_TBUNIVERSO.TXT": "Aguas Magallanes",
        "96703230_1_TBUNIVERSO.TXT": "Aguas Décima"
    }
    return empresas.get(key, "Empresa Desconocida")  


def comprobar_alerta(driver, empresa, errores_PAT, proceso):
    global screenshot_path
    try:
        max_wait_time = 90
        start_time = time.time()

        while True:
            try:
                if len(driver.window_handles) > 2:
                    print("Se ingresa a pestaña para procesar los archivos")
                    logging.info("Se ingresa a pestaña para procesar los archivos")
                    break

                try:
                    alert = WebDriverWait(driver, 3).until(EC.alert_is_present())
                    print(f"Se detectó un alert")
                    alert.accept()
                    print("Alerta cerrada exitosamente.")
                    sleep(2)
                    logging.error(f"Se detecto una alerta durante la ejecucion de {empresa}, en el proceso {proceso}")
                    raise Exception(f"Se detecto una alerta durante la ejecucion de {empresa}, en el proceso {proceso}")
                
                except (NoAlertPresentException, TimeoutException, WebDriverException):
                    print("No hay alertas activas")

                if time.time() - start_time > max_wait_time:
                    print(f"Se alcanzó el tiempo máximo de espera en el proceso {proceso} de {empresa}. La ejecución se ha detenido.")
                    screenshot_path = os.path.join(errores_PAT, f"screenshot_timeout_{empresa}.png")
                    driver.save_screenshot(screenshot_path)
                    logging.error("Se alcanzó el tiempo máximo de espera en el proceso {proceso} de {empresa}. La ejecución se ha detenido.")
                    raise Exception(f"Se alcanzó el tiempo máximo de espera en el proceso {proceso} de {empresa}. La ejecución se ha detenido.")
                
                sleep(1)

            except Exception as e:
                screenshot_path = os.path.join(errores_PAT, f"screenshot_alert_detected_{empresa}.png")
                driver.save_screenshot(screenshot_path)
                raise Exception(f"{str(e)}")

    except Exception as e:
        print(f"Error en procesar archivos: {str(e)}")
        raise Exception(f"{str(e)}")



def monitorear_proceso_archivos(driver, empresa, errores_PAT, proceso):
    global screenshot_path
    try:
        sleep(5)
        max_wait_time = 90
        driver.switch_to.window(driver.window_handles[-1]) 
        proceso_anterior, unchanged_start_time = None, None

        intentos = 0
        max_intentos = 3 

        while True:
            try:
                if len(driver.window_handles) < 3:
                    print(f"Finaliza el {proceso} proceso de archivos")
                    logging.info(f"Finaliza el {proceso} proceso de archivos")
                    return  
                
                proceso_actual = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.progress-label"))).text

                if proceso_anterior is not None:
                    if proceso_actual == proceso_anterior:
                        if unchanged_start_time is None:
                            unchanged_start_time = time.time() 
                        else:
                            elapsed = time.time() - unchanged_start_time
                            print(f"Tiempo transcurrido sin cambio: {elapsed:.2f} segundos")

                            if elapsed >= max_wait_time:
                                print("El proceso se ha congelado por 60 segundos, saliendo...")
                                logging.error(f"El proceso se ha congelado {proceso} por 90 segundos: Se presume un congelamiento en el proceso de archivos")
                                raise Exception(f"El proceso se ha congelado {proceso} por 90 segundos: Se presume un congelamiento en el proceso de archivos")
                    else:
                        proceso_anterior = proceso_actual
                        unchanged_start_time = None
                else:
                    proceso_anterior = proceso_actual
                    unchanged_start_time = None

                sleep(5)
            
            except NoSuchWindowException:
                intentos += 1
                print(f"Intento {intentos} de {max_intentos} para reiniciar proceso.")
                logging.error(f"La ventana se cerró inesperadamente. Reiniciando proceso {proceso}, intento {intentos} de {max_intentos}")
                
                if intentos >= max_intentos:
                    print("Se alcanzó el máximo de intentos, deteniendo ejecución.")
                    raise Exception(f"No se pudo recuperar la ventana en {max_intentos} intentos. Finalizando proceso.")

                sleep(5)

                if proceso == 1:
                    sleep(5)
                    driver.find_element(By.ID, 'xrpnlSeleccionar_xrdbPAT_S_D').click()
                    driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()
                        
                
                elif proceso == 2:
                    seleccionar = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'xchkSeleccionarTodos_S_D')))
                    seleccionar.click()
                    sleep(2)
                    ejecutar= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'xbtnEjecutar_CD')))
                    ejecutar.click()

                comprobar_alerta(driver, empresa, errores_PAT) 

            
            except TimeoutException:
                print("No se encontró el elemento en el tiempo esperado.")
                return 
    
    except Exception as e:
        print(f"Error en monitorear_proceso_archivos: {str(e)}")
        screenshot_path = os.path.join(errores_PAT, f"screenshot_error_{empresa}.png")
        try:
            driver.save_screenshot(screenshot_path)
            print(f"Se guardó el screenshot en {screenshot_path}")
        except:
            print("No se pudo tomar el screenshot porque el driver ya no está disponible.")
        
        try:
            driver.quit()
        except:
            pass
        raise Exception(f"Error crítico en monitorear proceso archivos: {str(e)}")  





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
        
        
        select_empresa = seleccionar_empresa(driver, empresa)

        if not select_empresa:
            mensaje= f"No se puede seleccionar la empresa {empresa}"
            logging.error(f"No se puede seleccionar la empresa {empresa}")
            envio_correo.correo(mensaje, empresa)
            continue

        driver = inicar_sesion(
            driver = driver,
            user = user,
            password = password,
            driver_options=chrome.opciones_chrome,
            url=url,
            empresa=empresa
        )

        if not driver:
            mensaje =f"No se logro iniciar sesion correctamente en la empresa: {empresa}"
            print(mensaje)
            logging.error(mensaje)
            envio_correo.correo(mensaje, empresa)
            continue

        sleep(5)

        ingresar_opciones_recaudacion(driver)
        
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
        remove(os.path.join(ruta_descarga_archivos, i))
        
        ruta=os.path.abspath(ruta_descarga_archivos+"\\TBUNIVERSO.TXT")
        archivo.send_keys(ruta)

        sleep(10)
        driver.find_element(By.ID, 'xrpnlSeleccionar_xrdbPAT_S_D').click()
        driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()

        comprobar_alerta(driver,empresa, errores_PAT, 1)

        monitorear_proceso_archivos(driver, empresa, errores_PAT, 1)
        
        WebDriverWait(driver, 10).until(lambda w: len(w.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        guardar_excel(driver, ruta_archivos_procesados, empresa, i)

        seleccionar = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, 'xchkSeleccionarTodos_S_D')))
        seleccionar.click()
        sleep(2)
        ejecutar= WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, 'xbtnEjecutar_CD')))
        ejecutar.click()

        sleep(2)
        comprobar_alerta(driver, empresa, errores_PAT, 2)

        monitorear_proceso_archivos(driver, empresa, errores_PAT, 2)

        WebDriverWait(driver, 10).until(lambda w: len(w.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[-1])

        sleep(2)    
        boton_aceptar = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="xbtnAceptar"]')))
        boton_aceptar.click()        
        sleep(10)
        driver.switch_to.window(window_before)
     
        salir=driver.find_element(By.XPATH, '//*[@id="ctl00_barra_superior"]/img[2]').click()
        
        if path.exists(ruta_descarga_archivos+"\\TBUNIVERSO.TXT"):
            remove(ruta_descarga_archivos+"\\TBUNIVERSO.TXT")
        
        mensaje = f"Empresa: {empresa} ha finalizado su proceso"
        envio_correo.correo(mensaje, empresa)
        screenshot_path = None
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