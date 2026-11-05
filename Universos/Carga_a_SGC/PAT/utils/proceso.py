from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, WebDriverException, NoSuchWindowException, ElementClickInterceptedException

import os
import logging


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

