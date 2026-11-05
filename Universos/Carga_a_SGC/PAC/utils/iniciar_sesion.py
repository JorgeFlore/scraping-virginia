
from time import sleep
import time
from selenium.webdriver.common.by import By
from utils import envio_correo
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotInteractableException, NoSuchElementException
import logging


def cargar_pagina(driver_options, url, empresa, intento_max=5, timeout=20):
    intento = 0
    while intento < intento_max:
        try:
            driver = driver_options()
            driver.set_page_load_timeout(timeout)
            driver.get(url)
            print("Pagina procesada correctamente")
            return driver
        except TimeoutException:
            print(f"Intento {intento+1}/{intento_max}: La página tardó más de {timeout} seg en cargar.")
        except WebDriverException:
            print(f"Intento {intento+1}/{intento_max}: La pagina no cargo, reintentando...")
        except Exception as e:
            print(f"Error inesperado al cargar la pagina inicial {e}")
        
        driver.quit()
        intento += 1
        sleep(3)

    mensaje = "ERROR CRITICO: No se pudo cargar la pagina inicial. Terminando el programa..."
    print(mensaje)
    envio_correo.correo(mensaje, empresa)
    exit()


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
                driver.quit()
                if reinicio == 1:
                    break                    
                cargar_pagina(driver_options, url, empresa)
                reinicio += 1
        
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
        driver.quit()
        return False  

    except Exception as e:
        logging.error(f"Error inesperado al seleccionar la empresa {empresa}: {str(e)}")
        print(f"Error inesperado al seleccionar la empresa {empresa}: {str(e)}")
        driver.quit()
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
                    driver.quit()
                    return None
                sleep(3)
        
        except Exception as e:
            print(f"No se pudo concretar el inicio de sesion, intento {intento + 1}/{intento_max}.")
         
        intento += 1
        driver.refresh()
        sleep(3)
        verificar_contenido_pagina_inicial(driver, driver_options, url, empresa)
        seleccionar_empresa(driver,empresa)
        continue 
    driver.quit()
    logging.error(f"No se pudo concretar el inicio de sesion")
    return None