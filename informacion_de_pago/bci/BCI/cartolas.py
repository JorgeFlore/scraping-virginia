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


captura_fecha = datetime.datetime.now()
nombre_carpeta=captura_fecha.strftime('%d-%m-%Y')
empresa=''







a = date.today()
b = diashabiles.previo()

diferente_mes = a.month != b.month

dia_hoy = a.day
dia_previo = b.day

def descargar_informacion():

    ruta_descarga=chrome.ruta_descargas()
    
    #empresas = ["76.850.128-9"]
    empresas = ["76.215.634-2","76.850.128-9","76.215.637-7","76.215.628-8","96.703.230-1"]
    if os.path.isdir(ruta_descarga+nombre_carpeta):
        rmtree(ruta_descarga+nombre_carpeta)
    
    
    for i in empresas:  
        match i:
            case "76.850.128-9":
                empresa="ATA"
            case "76.215.634-2":
                empresa="ADA"
            case "76.215.637-7":
                empresa="ARA"
            case "76.215.628-8":
                empresa="AMA"
            case "96.703.230-1":
                empresa="AXA"
    
        driver = chrome.opciones_chrome(nombre_carpeta,empresa)
        espera=WebDriverWait(driver,100)
        driver.get("https://www.bci.cl/empresas")
        banco_en_linea=driver.find_element(By.CLASS_NAME, 'btn_login.btn.btn-success.btn-lg.btn-rounded')
        banco_en_linea.click()
        rut=driver.find_element(By.NAME, 'rut_aux')
        sleep(2)
        rut.send_keys(os.getenv("BCI_RUT"))
        clave=driver.find_element(By.ID, 'clave_aux')
        clave.send_keys(os.getenv("BCI_CLAVE"))
        ingresar=driver.find_element(By.CLASS_NAME, 'submit.btn.btn_borde_green.mdb-text-green.btn-rounded.shadow-0')
        ingresar.click()
        #sleep(5)
        nombre_grupo=espera.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nombre-grupo')))
        nombre_grupo.click()
        
        
        if os.path.isdir(ruta_descarga+nombre_carpeta):
            #mkdir(ruta_descarga+nombre_carpeta)
            mkdir(ruta_descarga+nombre_carpeta+'\\'+empresa)
        else:
            mkdir(ruta_descarga+nombre_carpeta)
            mkdir(ruta_descarga+nombre_carpeta+'\\'+empresa)
            
    
        sleep(10)
        
    
        
        ####################################################SALDOS CONSOLIDADOS###################################################
        try:
            menu_cuentas = [
                    (By.XPATH, '//mat-list-item//*[contains(text(), "Cuentas")]'),
                    (By.XPATH, '//mat-list-item//*[contains(text(), "Saldos Consolidados")]')]
           
            sleep(3)
            for locator in menu_cuentas:
                element=espera.until(EC.presence_of_element_located(locator))
                #sleep(5)
                driver.execute_script("arguments[0].click();",  element)
                sleep(10)
                
        except:
            driver.save_screenshot(empresa+" error menu_cuentas.png")
            pass    
        try:
            locators = [
                (By.CSS_SELECTOR, "#grandchild_60005 > mat-list-item > div"),
                (By.XPATH, f"//span[@class='cursor-hover'][contains(text(), '{i}')]"),
                (By.ID, "balances-columna-cuenta"),
                (By.CSS_SELECTOR, "#cta-corriente-boton-descarga-movimientos")
            ]
    
            for locator1 in locators:
                element2=espera.until(EC.presence_of_element_located(locator1))
                driver.execute_script("arguments[0].click()", element2)
                sleep(10)
                #element = driver.find_element(*locator)
                #driver.execute_script("arguments[0].click()", element)
                


        except:
            driver.save_screenshot(empresa+" error descarga-movimientos.png")
            pass
        ####################################################################################################################################################
        sleep(10)  
        
        
        ####################################################CARTOLA HISTORICA##################################################
        try:
            menu_cartolas_historicas = [
                (By.XPATH, '//mat-list-item//*[contains(text(), "Cuentas")]'),
                (By.XPATH, '//mat-list-item//*[contains(text(), "Cartola Histórica")]'),
                 (By.XPATH, '//*[@id="historical-balances-ver-cartola"]'),
                  (By.XPATH, "//button[normalize-space(text())='Descarga cartola Excel']"),
                ]
            for locator2 in menu_cartolas_historicas:
                element=espera.until(EC.presence_of_element_located(locator2))
                driver.execute_script("arguments[0].click()", element)
                sleep(3)
        except:
            driver.save_screenshot(empresa+" error menu_cartolas_historicas")
            pass 
        
        
        #####################################################################################################################################################
        sleep(10)
    
        #######################################################DESCARGA DEPOSITOS###############################################
        try:
        
            descarga_depositos = [
                (By.XPATH, '//mat-list-item//*[contains(text(), "Cuentas")]'),
                    (
                       By.XPATH, '//mat-list-item//*[contains(text(), "Depósitos")]'),]
                
            #sleep(3)
    
            for locator3 in descarga_depositos:
                element=espera.until(EC.presence_of_element_located(locator3))
                driver.execute_script("arguments[0].click();",  element)
                sleep(3)

            #sleep(5)     
        except:
            driver.save_screenshot(empresa+" error en calendario.png")
            pass  
        
        

    
    
    
        sleep(5)
        
        
        
        try:
            #######################################################EFECTIVO###############################################
            calendario=espera.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='chip-calendario']")))
            calendario.click()
            if diferente_mes:
                espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Previous month"]'))).click()
                sleep(2)
            espera.until(EC.element_to_be_clickable((By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_previo}')]"))).click()
            if diferente_mes:
                espera.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 'button[aria-label="Next month"]'))).click()
            espera.until(EC.element_to_be_clickable((
                By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_hoy}')]"))).click()
            sleep(6) 
            efectivo=espera.until(EC.element_to_be_clickable((By.XPATH, "//mat-table//span[text()='Efectivo']/../../..//mat-icon")))
            efectivo.click()
            #sleep(6)
            espera.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='linkDescargar']"))).click()
            #sleep(6)

        except:
            print("no hay efectivo")
            driver.save_screenshot(empresa+" no hay efectivo.png")
            sleep(5)
            try:
                driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            except:
                pass
            pass
        ###########################################################################################################
            
            
            
        try:   
            #######################################################Mismo Banco###############################################
            calendario=espera.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='chip-calendario']")))
            calendario.click()
            if diferente_mes:
                espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Previous month"]'))).click()
                sleep(2)
            espera.until(EC.element_to_be_clickable((By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_previo}')]"))).click()
            if diferente_mes:
                espera.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 'button[aria-label="Next month"]'))).click()
            espera.until(EC.element_to_be_clickable((
                By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_hoy}')]"))).click()
            sleep(6) 
            
            mismo_banco=driver.find_elements(By.XPATH, "//mat-table//span[text()='Mismo banco']")
            print(len(mismo_banco))
            for i in range(1,len(mismo_banco)+1):
                sleep(6)    
                input_fitro=driver.find_element(By.XPATH, '//*[@id="buscador"]')
                input_fitro.clear()
                input_fitro.send_keys("Mismo")
                print(i)
                serial=driver.find_element(By.XPATH, "//*[@id='contDepositos']/mat-sidenav-container/mat-sidenav-content/div[2]/div/mat-table/mat-row["+str(i)+"]/mat-cell[1]/div/span")
                print(serial.text)
                serial.click()
                sleep(6)
                driver.find_element(By.XPATH, '//*[@id="cont-tabla-detalle-deposito"]/mat-sidenav-container/mat-sidenav-content/div[4]/div/mat-table/mat-row/mat-cell[8]/div/mat-icon').click()
                sleep(6)
                driver.find_element(By.XPATH, "//p[@class='linkDescargar']").click()
                sleep(6)
                driver.find_element(By.CLASS_NAME, "btn-volver").click()
                sleep(6)
                seleccionar_calendario()
                sleep(6)
        except:
            print("error Mismo banco")
            driver.save_screenshot(empresa+" Mismo banco.png")
            sleep(5)
            #driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            try:
                driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            except:
                pass
            pass
            #################################################################################################################################################
        try:
        #######################################################OTRO BANCO###############################################    
            calendario=espera.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='chip-calendario']")))
            calendario.click()
            if diferente_mes:
                espera.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Previous month"]'))).click()
                sleep(2)
            espera.until(EC.element_to_be_clickable((By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_previo}')]"))).click()
            if diferente_mes:
                espera.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, 'button[aria-label="Next month"]'))).click()
            espera.until(EC.element_to_be_clickable((
                By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_hoy}')]"))).click()
            sleep(6) 
            #seleccionar_calendario()
            otro_banco=driver.find_elements(By.XPATH, "//mat-table//span[text()='Otro Banco']")
            print(len(otro_banco))
            for i in range(1,len(otro_banco)+1):
                sleep(6)    
                input_fitro=driver.find_element(By.XPATH, '//*[@id="buscador"]')
                input_fitro.clear()
                input_fitro.send_keys("Otro")
                print(i)
                serial=driver.find_element(By.XPATH, "//*[@id='contDepositos']/mat-sidenav-container/mat-sidenav-content/div[2]/div/mat-table/mat-row["+str(i)+"]/mat-cell[1]/div/span")
                print(serial.text)
                serial.click()
                sleep(6)
                driver.find_element(By.XPATH, '//*[@id="cont-tabla-detalle-deposito"]/mat-sidenav-container/mat-sidenav-content/div[4]/div/mat-table/mat-row/mat-cell[8]/div/mat-icon').click()
                sleep(6)
                driver.find_element(By.XPATH, "//p[@class='linkDescargar']").click()
                sleep(6)
                driver.find_element(By.CLASS_NAME, "btn-volver").click()
                sleep(6)
                seleccionar_calendario()
                sleep(6)
                
        except:
            print("error otro banco")
            driver.save_screenshot(empresa+" otro banco.png")
            sleep(5)
            #driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            try:
                driver.find_element(By.XPATH, '//*[@id="toastGenerico"]/div/div[3]/i').click()
            except:
                pass
            pass
        
        #################################################################################################################################################
        
        ##########################################################################################################################################################################
        sleep(10)
    
    
            ########################################DESCARGA TRANSFERENCIA##############################################################################
        try:
           menu_transferencia = [
                (By.XPATH, '//*[@id="father_36"]/div'),
                (By.XPATH, '//*[@id="childNav_40"]/div'),
                 (By.XPATH, '//*[@id="descarga-excel"]/button/span')]
           for locator4 in menu_transferencia:
                element=espera.until(EC.presence_of_element_located(locator4))
                driver.execute_script("arguments[0].click();",  element)
                sleep(10)
            #element = driver.find_element(By.CSS_SELECTOR, "#childNav_40 > div")
            #driver.execute_script("arguments[0].click()", element)
        #
            #driver.find_element(By.CLASS_NAME, "btn-descargar").click()
                
        except:
            driver.save_screenshot(empresa+" error transferencias.png")
            pass 
        sleep(3)
        try:
            driver.find_element(By.XPATH, '//*[@id="btn-cerrar-sesion"]')
            driver.quit()
        except:
            driver.quit()
            
            
        
        ##########################################################################################################################################################################
        #correos.envio_correo(ruta_descarga,nombre_carpeta,empresa)


#@classmethod 
    def seleccionar_calendario():
        sleep(3)
        calendario=driver.find_element(By.XPATH, "//div[@class='chip-calendario']")
        driver.execute_script("arguments[0].click();",  calendario)
        sleep(10)
        if diferente_mes:
            dia_mes_anterior=driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Previous month"]')
            driver.execute_script("arguments[0].click();",  dia_mes_anterior)
            sleep(2)
        sleep(6)
        dia_anterior=driver.find_element(By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_previo}')]")
        driver.execute_script("arguments[0].click();",  dia_anterior)
        sleep(6)
        if diferente_mes:
            dia_actual_mes=driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next month"]')
            driver.execute_script("arguments[0].click();",  dia_actual_mes)
            sleep(6)
        dia_actual=driver.find_element(By.XPATH, f"//tbody[@class='mat-calendar-body']//tr//td//div[contains(text(), '{dia_hoy}')]")
        driver.execute_script("arguments[0].click();",  dia_actual)
        #return driver
        sleep(6)
        
        
        
    
    
                
    #    def seleccionar_empresa(i):
    