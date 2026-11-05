from os import *
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import time


def descargar_saldos_consolidados(driver, espera, empresa, ruta_completa, i, screenshot_dir, screenshots_dict):
    try:
        menu_cuentas = [
            (By.XPATH, '//mat-list-item//*[contains(text(), "Saldos Consolidados")]')
        ]

        sleep(3)
        for locator in menu_cuentas:
            element = espera.until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click();", element)
            sleep(10)

    except Exception as e:
        print(f"Error al abrir menú de Saldos Consolidados: {e}")
        screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_menu_cuentas.png")
        driver.save_screenshot(screenshot_path)
        screenshots_dict[screenshot_path] = "Error al abrir menú de Saldos Consolidados"
        return False  

    try:
        locators = [
                # (By.CSS_SELECTOR, "#grandchild_60005 > mat-list-item > div"),
                (By.XPATH, f"//span[@class='cursor-hover'][contains(text(), '{i}')]"),
                (By.ID, "balances-columna-cuenta"),
                (By.CSS_SELECTOR, "#cta-corriente-boton-descarga-movimientos")
            ]

        archivos_antes = len(os.listdir(ruta_completa))

        for locator in locators:
            element = espera.until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", element)
            sleep(10)

        archivos_despues = len(os.listdir(ruta_completa))

        if archivos_antes == archivos_despues:
            print("No se descargó el archivo, verificando si apareció el modal...")
            sleep(3)

            try:
                espera.until(EC.presence_of_element_located((By.XPATH, '//div[@class="toast-generico mat-elevation-z2"]')))
                print("Modal detectado. Haciendo clic en 'Descargas de movimientos'...")

                enlace_descargas = driver.find_element(By.XPATH, '//a[contains(text(), "Descargas de movimientos")]')
                enlace_descargas.click()

                tiempo_inicio = time.time()
                tiempo_maximo = 3 * 60 

                while True:
                    if time.time() - tiempo_inicio > tiempo_maximo:
                        print("Tiempo máximo de espera alcanzado. Saliendo del bucle.")
                        return False

                    try:# print("Intentando descargar desde la página de descargas...")
                        descarga_saldos_consolidados = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "(//mat-table//mat-row)[1]//mat-cell[@id='descarga-movimiento']//button")))
                        descarga_saldos_consolidados.click()
                        
                        sleep(5)

                        archivos_despues = len(os.listdir(ruta_completa))
                        if archivos_despues > archivos_antes:
                            # print("Archivo descargado correctamente.")
                            return True  
                    except:
                        print("El botón de descarga aún no está disponible, reintentando en 10 segundos...")
                        sleep(10)

            except:
                archivos_despues = len(os.listdir(ruta_completa))
                if archivos_antes == archivos_despues:
                    print("El modal no apareció. Verificar manualmente.")
                    return False
                else:
                    return True
    
    except Exception as e:
        print(f"Error durante la descarga de movimientos: {e}")
        screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_descarga_movimientos.png")
        driver.save_screenshot(screenshot_path)
        screenshots_dict[screenshot_path] = "Error durante la descarga de movimientos"
        return False  

    return True  


def descargar_cartolas_historicas(driver, espera, empresa, screenshot_dir, screenshots_dict):
    try:
        menu_cartolas_historicas = [
            (By.XPATH, '//mat-list-item//*[contains(text(), "Cartola Histórica")]'),
            (By.XPATH, '//*[@id="historical-balances-ver-cartola"]'),
            (By.XPATH, "//button[normalize-space(text())='Descarga cartola Excel']"),
        ]
        
        for locator2 in menu_cartolas_historicas:
            element = espera.until(EC.presence_of_element_located(locator2))
            driver.execute_script("arguments[0].click()", element)
            sleep(5)
        return True

    except:
        screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_menu_cartolas_historicas.png")
        driver.save_screenshot(screenshot_path)
        screenshots_dict[screenshot_path] = "Error en menu de cartolas historicas"
        return False


def descargar_depositos_efectivo(driver, espera, i, empresa, screenshot_dir, screenshots_dict):
    try:
        try:
            efectivo = espera.until(EC.presence_of_element_located((By.XPATH, f"//*[@id='contDepositos']/mat-sidenav-container/mat-sidenav-content/div[2]/div/mat-table/mat-row[{i}]/mat-cell[6]/div")))
            driver.execute_script("arguments[0].click();", efectivo)    
            espera.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='linkDescargar']"))).click()
            return True  
        
        except Exception as e:
            print(f"Error al hacer clic en 'Efectivo' o el enlace de descarga: {e}")
            screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_efectivo.png")
            driver.save_screenshot(screenshot_path)
            screenshots_dict[screenshot_path] = "Error al hacer clic en 'Efectivo' o el enlace de descarga"
            sleep(5)
            return False  

    
    except Exception as e:
        print("No hay efectivo")
        screenshot_path = os.path.join(screenshot_dir, f"{empresa}_no_hay_efectivo.png")
        driver.save_screenshot(screenshot_path)
        screenshots_dict[screenshot_path] = "No hay efectivo"
        sleep(5)
        try:
            driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
        except:
            pass
        return False


def verificar_modal_error_deposito(driver):
    try:
        modal_error = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//app-toast-generico//div[@class='texto']/h5[text()='El documento no está disponible en 360 Connect']"))
        )
        return modal_error
    except Exception as e:
        return False


def descargar_documento_banco(driver, espera, i, empresa, screenshot_dir, screenshots_dict):
    try:
        serial = driver.find_element(By.XPATH, f"//*[@id='contDepositos']/mat-sidenav-container/mat-sidenav-content/div[2]/div/mat-table/mat-row[{i}]/mat-cell[1]/div/span")
        print(serial.text)
        serial.click()
        sleep(5)

        modal_error_deposito = verificar_modal_error_deposito(driver)

        if modal_error_deposito:
            print("El documento no está disponible. Cerrando el modal...")
            close_button = driver.find_element(By.XPATH, "//app-toast-generico//div[@class='close']/i")
            close_button.click()
            sleep(5)
            return True
        else:
            modal_descarga = espera.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cont-tabla-detalle-deposito"]/mat-sidenav-container/mat-sidenav-content/div[4]/div/mat-table/mat-row/mat-cell[8]/div/mat-icon')))
            driver.execute_script("arguments[0].click();", modal_descarga)
            sleep(5)
            driver.find_element(By.XPATH, "//p[@class='linkDescargar']").click()
            sleep(5)
            driver.find_element(By.CLASS_NAME, "btn-volver").click()
            sleep(5)
            return False
            
    except Exception as e:
        print(f"Error en la descarga del documento banco")
        screenshot_path = os.path.join(screenshot_dir, f"{empresa}_error_descarga_banco.png")
        driver.save_screenshot(screenshot_path)
        screenshots_dict[screenshot_path] = "Error en la descarga del documento banco"
        sleep(5)
        return False