
from time import sleep
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotInteractableException, NoSuchElementException
import logging


def cerrar(driver):
    """Cierra el navegador sin lanzar error si ya estaba cerrado."""
    if driver is None:
        return
    try:
        driver.quit()
    except Exception:  # noqa: BLE001
        pass


def cargar_pagina(driver_options, url, empresa, intento_max=5, timeout=20):
    """Abre el navegador en la URL. Devuelve el driver o None (antes hacía exit() y detenía todas las empresas)."""
    for intento in range(1, intento_max + 1):
        driver = None
        try:
            driver = driver_options()
            driver.set_page_load_timeout(timeout)
            driver.get(url)
            logging.info("[%s] Página de SGC cargada", empresa)
            return driver
        except TimeoutException:
            logging.warning("[%s] Intento %s/%s: la página tardó más de %s s", empresa, intento, intento_max, timeout)
        except Exception as e:  # noqa: BLE001
            logging.warning("[%s] Intento %s/%s: no se pudo abrir la página: %s", empresa, intento, intento_max, e)
        cerrar(driver)
        sleep(3)
    logging.error("[%s] No se pudo cargar la página inicial de SGC", empresa)
    return None



def verificar_contenido_pagina_inicial(driver, driver_options, url, empresa, intento_max=3):
    intento = 0
    reinicio = 0
    while intento < intento_max:
        try:
            seleccionar_empresa= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xddlEmpresa_I']")))
            seleccionar_empresa.click()
            return driver
        
        except Exception:
            print(f"No se cargo correctamente la pagina de inicio intento: {intento + 1}/{intento_max}. Reiniciando proceso...")
            try:
                driver.refresh()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xddlEmpresa_I']")))  
                print("Página recargada. Reintentando el proceso de inicio de sesión.")
            
            except Exception:
                print("No se pudo recargar la página dentro del tiempo esperado. Intentando reiniciar el proceso.")
                cerrar(driver)
                if reinicio == 1:
                    break
                driver = cargar_pagina(driver_options, url, empresa)  # antes se perdía este driver nuevo
                reinicio += 1
                if driver is None:
                    break
        
        intento += 1
        continue 

    return None



def seleccionar_empresa(driver, empresa):

    sleep(5)  

    try:
        select_empresa = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//td[text()='{empresa}']"))
        )
        select_empresa.click()
        logging.info(f"Seleccionada la empresa {empresa} correctamente.")

        sleep(1)
        contenedor_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "login")))
        contenedor_login.click()
        sleep(1)

    except (NoSuchElementException, ElementNotInteractableException, TimeoutException):
        cerrar(driver)
        return False  

    except Exception as e:
        logging.error(f"Error inesperado al seleccionar la empresa {empresa}: {str(e)}")
        print(f"Error inesperado al seleccionar la empresa {empresa}: {str(e)}")
        cerrar(driver)
        return False  

    return True  



def verificar_input(element, expected_value):
    sleep(0.5)
    if element.get_attribute('value') == expected_value:
        return True
    return False



def inicar_sesion(driver, user, password, driver_options, url, empresa, intento_max=4):
    intento = 0
    while intento < intento_max:
        try:
            user_input=driver.find_element(By.ID,'txtxUsuario_I')
            password_input=driver.find_element(By.ID,'txtxContrasena_I')
            
            user_input.clear()
            user_input.send_keys(user)
            
            if not verificar_input(user_input, user):
                print("El input user no se llenó correctamente.")
                raise Exception("El input user no se llenó correctamente.")
            
            password_input.clear()
            password_input.send_keys(password)
            
            if not verificar_input(password_input, password):
                print("El input password no se llenó correctamente.")
                raise Exception("El input password no se llenó correctamente.")
            
            print("Credenciales ingresadas correctamente.")

            inicial_html = driver.execute_script("return document.documentElement.outerHTML")
        
            sleep(3)

            try:
                boton_entrar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnxEntrar')))
                boton_entrar.click()
                print("Botón 'Entrar' clickeado correctamente.")
            except Exception as e:
                print(f"El botón 'Entrar' no estaba listo para hacer clic.")
                raise Exception("El botón 'Entrar' no está listo para hacer clic.")

            sleep(3)
            timeout = 30
            start_time = time.time()


            while True:
                nuevo_html = driver.execute_script("return document.documentElement.outerHTML")

                if inicial_html != nuevo_html:
                    print("Ingreso a la nueva pestaña")
                    return driver
            
                if time.time() - start_time > timeout:
                    print("Se alcanzo el tiempo maximo de espera, posiblemente se congelo el inicio de sesion")
                    cerrar(driver)
                    return None
                sleep(3)
        
        except Exception as e:
            print(f"No se pudo concretar el inicio de sesion, intento {intento + 1}/{intento_max}.")
         
        intento += 1
        try:
            driver.refresh()
            sleep(3)
        except Exception:  # noqa: BLE001
            pass
        driver = verificar_contenido_pagina_inicial(driver, driver_options, url, empresa)
        if driver is None or not seleccionar_empresa(driver, empresa):
            logging.error("No se pudo volver a la pantalla de login para reintentar")
            return None
        continue
    cerrar(driver)
    logging.error(f"No se pudo concretar el inicio de sesion")
    return None