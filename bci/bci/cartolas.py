from utils import chrome
from os import *
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from utils import diashabiles
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import os
from shutil import rmtree
import utils.correos as correos
import shutil
import random
import time
from selenium.webdriver.common.action_chains import ActionChains

from utils.descargas import descargar_saldos_consolidados, descargar_cartolas_historicas, descargar_depositos_efectivo, descargar_documento_banco

captura_fecha = datetime.datetime.now()
nombre_carpeta=captura_fecha.strftime('%d-%m-%Y')
empresa=''

a = date.today()
b = diashabiles.previo()

diferente_mes = a.month != b.month

dia_hoy = a.day
dia_previo = b.day


def descargar_informacion():
    screenshots_dict = {}

    ruta_descarga=chrome.ruta_descargas()
    
    ruta_completa1 = os.path.join(ruta_descarga, nombre_carpeta)
    
    if os.path.exists(ruta_completa1):
        shutil.rmtree(ruta_completa1)
        print(f"Carpeta {ruta_completa1} eliminada.")
    
    os.makedirs(ruta_completa1)
    print(f"Carpeta {ruta_completa1} creada.")

    screenshot_dir = os.path.join(ruta_descarga, nombre_carpeta, "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    empresas = ["76.215.634-2","76.850.128-9","76.215.628-8","76.215.637-7","96.703.230-1"] 
    #empresas = ["96.703.230-1"] 
    
    rut_empresa = {
        "76.215.634-2": "ADA",
        "76.850.128-9": "ATA", 
        "76.215.637-7": "ARA", 
        "76.215.628-8": "AMA",
        "96.703.230-1": "AXA" 
    }
    rut = "12708917-5"   #""   14411045-5   12708917-5
    clave = os.getenv("BCI_CLAVE")
    
    driver, espera = acceder_pagina_inicial()
    if driver and espera:
        print("Página cargada correctamente.")
    else:
        print("Página no disponible. Vuelva a ejecutar el script desde 0.")
        exit(0)
    
    inicio_sesion_exitoso = inicio_sesion(driver, rut, clave, espera)
    if not inicio_sesion_exitoso:
        print(f"No se logró iniciar sesión")
        exit(0)

    intento_maximo = 2
    intento = 1
    while True:
        if driver.current_url == "https://bel.bci.cl/LoginJSFGenerico":
            print(f"Captcha detectado. Ingrese manualmente las credenciales")
            # input("Presione Enter para continuar. ")
            sleep(30)
            if intento == intento_maximo:
                screenshot_path = os.path.join(screenshot_dir, f"error_captcha.png")
                driver.save_screenshot(screenshot_path)
                screenshots_dict[screenshot_path] = "Error en el proceso inicial"
    
                mensaje = f"No se logro ingresar a banco Bci luego de {intento} intentos."
                correos.correo(mensaje, "Sin empresa", screenshots_dict)
                exit(0)
            intento += 1
            continue 
        break

    # SE PRESUME QUE INGRESA A LA PAGINA CORRECTAMENE, PASANDO EL CAPTCHA.
    nombre_grupo = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, 'nombre-grupo')))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nombre-grupo')))
    nombre_grupo.click()

    for i in empresas:
        empresa = rut_empresa.get(i, "Empresa no encontrada") 
        print(f"Empresa: {empresa}")
        
        if empresa == "Empresa no encontrada": 
            continue

        ruta_completa = os.path.join(ruta_descarga, nombre_carpeta, empresa)

        if not os.path.exists(ruta_completa):
            os.makedirs(ruta_completa)
            print(f"Carpeta creada: {ruta_completa}")
        else:
            print(f"La carpeta ya existe: {ruta_completa}")

        cambiar_directorio_descargas(driver, ruta_completa)
        
        sleep(5)

        ####################################################SALDOS CONSOLIDADOS###################################################
        descarga_saldos_consolidados_exitosa = descargar_saldos_consolidados(driver, espera, empresa, ruta_completa, i, screenshot_dir, screenshots_dict)

        if descarga_saldos_consolidados_exitosa:
            print("Descarga de saldos consolidados completada con éxito.")
        else:
            print("Hubo un problema con la descarga de saldos consolidados.")
       
        sleep(5)

        ####################################################CARTOLA HISTORICA##################################################
        descarga_cartolas_historias_exitosa = descargar_cartolas_historicas(driver, espera, empresa, screenshot_dir, screenshots_dict)

        if descarga_cartolas_historias_exitosa:
            print("Descarga de cartolas historicas completada con éxito.")
        else:
            print("Hubo un problema con la descarga de cartolas historicas.")
       
        sleep(5)

        #######################################################DESCARGA DEPOSITOS###############################################
        try:
            descarga_depositos = [
                (By.XPATH, '//mat-list-item//*[contains(text(), "Cheques")]'),
                (By.XPATH, '//mat-list-item//*[contains(text(), "Depósitos")]'),
            ]

            for locator3 in descarga_depositos:
                element=espera.until(EC.presence_of_element_located(locator3))
                driver.execute_script("arguments[0].click();",  element)
                sleep(3)

        except:
            screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_en_calendario.png")
            driver.save_screenshot(screenshot_path)
            screenshots_dict[screenshot_path] = "Error en calendario"
            pass

        sleep(5)
        
        #######################################################EFECTIVO###############################################
        try:
            seleccionar_calendario(driver)

            efectivo = driver.find_elements(By.XPATH, "//mat-table//span[text()='Efectivo']")
            print(len(efectivo))
            if len(efectivo) == 0:
                print("No hay efectivo")
            for i in range(1,len(efectivo)+1):
                sleep(5)        
                input_fitro=driver.find_element(By.XPATH, '//*[@id="buscador"]')
                input_fitro.clear()
                input_fitro.send_keys("Efectivo")
                print(f"Archivo numero {i} descargando..")
                descargar_depositos_efectivo(driver, espera, i, empresa, screenshot_dir, screenshots_dict)
                seleccionar_calendario(driver)

        except:
            print(f"Error en el proceso efectivo")
            screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_proceso_efectivo.png")
            driver.save_screenshot(screenshot_path)
            screenshots_dict[screenshot_path] = "Error en el proceso de efectivo"
            sleep(5)
            try:
                driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            except:
                pass
            pass

        #######################################################Mismo Banco###############################################
        try:
            seleccionar_calendario(driver)
            
            mismo_banco=driver.find_elements(By.XPATH, "//mat-table//span[text()='Mismo banco']")
            print(len(mismo_banco))
            if len(mismo_banco) == 0:
                print("No hay mismo banco")
            for i in range(1,len(mismo_banco)+1):
                sleep(5)
                input_fitro=driver.find_element(By.XPATH, '//*[@id="buscador"]')
                input_fitro.clear()
                input_fitro.send_keys("Mismo")
                print(f"Archivo numero {i} descargando..")
                modal_presente = descargar_documento_banco(driver, espera, i ,empresa, screenshot_dir, screenshots_dict)
                if not modal_presente:
                    seleccionar_calendario(driver)
                
        except:
            print("Error en el proceso Mismo banco")
            screenshot_path = os.path.join(screenshot_dir, f"{empresa}_mismo_banco.png")
            driver.save_screenshot(screenshot_path)
            screenshots_dict[screenshot_path] = "Error en el proceso de Mismo banco"
            sleep(5)

        #######################################################OTRO BANCO###############################################
        try:
            seleccionar_calendario(driver)
            
            otro_banco=driver.find_elements(By.XPATH, "//mat-table//span[text()='Otro Banco']")
            print(len(otro_banco))
            if len(otro_banco) == 0:
                print("No hay otro banco")
            for i in range(1,len(otro_banco)+1):
                sleep(5)
                input_fitro=driver.find_element(By.XPATH, '//*[@id="buscador"]')
                input_fitro.clear()
                input_fitro.send_keys("Otro")
                print(f"Archivo numero {i} descargando..")
                modal_presente = descargar_documento_banco(driver, espera, i ,empresa, screenshot_dir, screenshots_dict)
                if not modal_presente:
                    seleccionar_calendario(driver)
                
        except:
            print("Error en el proceso de otro banco")
            screenshot_path = os.path.join(screenshot_dir, f"{empresa}_otro_banco.png")
            driver.save_screenshot(screenshot_path)
            screenshots_dict[screenshot_path] = "Error en el proceso de Otro banco"

            sleep(5)
            try:
                driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            except:
                pass
            pass

        sleep(5)

        ########################################DESCARGA TRANSFERENCIA##############################################################################
        try:
            menu_transferencia = [
                # (By.XPATH, '//*[@id="father_36"]/div'),
                (By.XPATH, '//*[@id="childNav_40"]/div'),
            ]
            for locator4 in menu_transferencia:
                element=espera.until(EC.presence_of_element_located(locator4))
                driver.execute_script("arguments[0].click();",  element)
                sleep(8)

            iframe_element = driver.find_element(By.XPATH, '//iframe')
            driver.switch_to.frame(iframe_element) 
            print("Descarga de transferencia completada con éxito")

            xpath_boton_filtro = "/html/body/app-root/app-mfe/app-transferencias/div/mat-sidenav-container/mat-sidenav-content/div[3]/div[2]/div[2]/bci-radio-search[1]/div/div"
            boton_filtro = espera.until(EC.element_to_be_clickable((By.XPATH, xpath_boton_filtro)))

            boton_filtro.click()
            sleep(2)

            rut_sin_puntos = empresas[0].replace('.', '')
            caja_busqueda = espera.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='chip-buscador']/div[2]/div[2]/div[1]/bci-chip/bci-input/input")))
            caja_busqueda.send_keys(rut_sin_puntos)

            empresa_seleccionada = driver.find_element(By.CLASS_NAME, "opcion")
            empresa_seleccionada.click()


 
            driver.find_element(By.XPATH, '//*[@id="descarga-excel"]/button').click()
 
            print("Descarga iniciada correctamente.")
 
            driver.switch_to.default_content()


        except:
            screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_transferencias.png")
            driver.save_screenshot(screenshot_path)
            screenshots_dict[screenshot_path] = "Error en el proceso de descarga de transferencia"
            pass
        sleep(3)

        mensaje = f"Empresa: {empresa} ejecutada."
        correos.correo(mensaje, empresa, screenshots_dict)
        
        screenshots_dict = {}


def cambiar_directorio_descargas(driver, ruta_completa):
    directorio_descargas = os.path.join(ruta_completa)
    
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",  # Permitir la descarga
        "downloadPath": directorio_descargas  # Cambiar la ruta de descargas
    })


def acceder_pagina_inicial(max_intentos=5):
    intentos = 0
    while intentos < max_intentos:
        try:
            driver = chrome.opciones_chrome()
            espera = WebDriverWait(driver, 60)
            
            driver.get("https://www.bci.cl/empresas")

            time.sleep(random.uniform(3, 6))
            
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn_login.btn.btn-success.btn-lg.btn-rounded'))
            )
            
            return driver, espera
        
        except Exception as e:
            print(f"Intento {intentos+1} fallido: {e}")
            intentos += 1
            driver.quit()
            if intentos < max_intentos:
                print("Reintentando en 5 segundos...")
                sleep(5)
            else:
                print("Número máximo de intentos alcanzado. No se pudo acceder a la página.")
                return False, False


def inicio_sesion(driver, rut, clave, espera, max_intentos=3) -> bool:
    intentos = 0
    while intentos < max_intentos:
        try:
            banco_en_linea = espera.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn_login.btn.btn-success.btn-lg.btn-rounded'))
            )
            banco_en_linea.click()
            action = ActionChains(driver)
            action.move_by_offset(random.randint(50, 150), random.randint(50, 150)).perform()
            time.sleep(random.uniform(1, 3))

            rut_input = espera.until(
                EC.visibility_of_element_located((By.ID, 'rut_aux'))
            )
            rut_input.send_keys(rut)

            # for char in rut:
            #     rut_input.send_keys(char) 
            #     time.sleep(random.uniform(0.3, 0.5)) 
            
            clave_input = espera.until(
                EC.visibility_of_element_located((By.ID, 'clave_aux'))
            )
            clave_input.send_keys(clave)

            # for char in clave:
            #     clave_input.send_keys(char) 
            #     time.sleep(random.uniform(0.3, 0.5))

            time.sleep(random.uniform(1, 3))
            ingresar_button = espera.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'submit.btn.btn_borde_green.mdb-text-green.btn-rounded.shadow-0'))
            )
            ingresar_button.click()

            print("Login exitoso")
            return True

        except Exception as e:
                intentos += 1
                print(f"Error en el login (Intento {intentos}/{max_intentos})")
                
                if intentos < max_intentos:
                    print(f"Reintentando en 5 segundos... ({intentos}/{max_intentos})")
                    driver.refresh() 
                    sleep(5) 
                else:
                    print("Número máximo de intentos alcanzado. No se pudo realizar el login.")
                    return False 


def seleccionar_calendario(driver):
    sleep(3)
    calendario=driver.find_element(By.XPATH, "//div[@class='chip-calendario']")
    driver.execute_script("arguments[0].click();",  calendario)
    sleep(3)
    if diferente_mes:
        dia_mes_anterior=driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Previous month"]')
        driver.execute_script("arguments[0].click();",  dia_mes_anterior)
        sleep(2)
    sleep(3)
    dia_anterior=driver.find_element(By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_previo}')]")
    driver.execute_script("arguments[0].click();",  dia_anterior)
    sleep(3)
    if diferente_mes:
        dia_actual_mes=driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next month"]')
        driver.execute_script("arguments[0].click();",  dia_actual_mes)
        sleep(3)
    dia_actual=driver.find_element(By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_hoy}')]")
    driver.execute_script("arguments[0].click();",  dia_actual)
    sleep(3)