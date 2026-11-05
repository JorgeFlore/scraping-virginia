from datetime import date
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime
from utils import chrome
from utils import envio_correo
from utils import credenciales
from nuevoArchivo import monitor_directory

from glob import glob
import os

driver = chrome.opciones_chrome()
ahora = datetime.datetime.utcnow()
ayer = ahora - datetime.timedelta(days=5)
primerDia=ayer.strftime('%d/%m/%Y')
primerDia=primerDia.replace('/','')
horaActual = datetime.datetime.now()

fechaActual = date.today()
fechaEnTexto = fechaActual.strftime('%d/%m/%Y')
fechaActualFormateada=fechaEnTexto.replace('/','')
empresa=""

def descargar_xml():
    fechaHora=str(fechaActualFormateada)+" "+str(horaActual.hour)+" "+str(horaActual.minute)+" "+str(horaActual.second)
    empresas=credenciales.leer_csv()   
 
    for i in empresas:
        try:
            
            driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")
            sleep(2)
            match i[0]:
                    case "777373099":
                        empresa="ASOL"
                    case "762156342":
                        empresa="ADA"
                    case "762156377":
                        empresa="ARA"
                    case "967032301":
                        empresa="AXA"
                    case "760454915":
                        empresa="ENER"
                    case "768501289":
                        empresa="ATA"
                    case "760386596":
                        empresa="AN"
                    case "762156288":
                        empresa="AMA"
                        
            print(empresa+": Procesando...")
            try:

                rut=driver.find_element(By.ID, "rutcntr")
                rut.send_keys(i[0])
                password=driver.find_element(By.ID, "clave")
                password.send_keys(i[1])
                sleep(2)
                driver.find_element(By.CSS_SELECTOR, "button.btn.btn-default").click()
                sleep(5)
            except Exception as e:
                print(f"Error en autenticación de {empresa}: {e}")
                envio_error(empresa, fechaHora)
                continue
                
            try:

                driver.get("https://palena.sii.cl/cgi_rtc/RTC/RTCConsultaCesionesHtml.cgi")
                sleep(3)
                check=driver.find_element(By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table[2]/tbody/tr[2]/td/table/tbody/tr[2]/td/input").click()
                desde=driver.find_element(By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input")
                desde.clear()
                desde.send_keys(primerDia)
                hasta=driver.find_element(By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/input")
                hasta.clear()
                hasta.send_keys(fechaActualFormateada)
                driver.find_element(By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/p/input").click()
                sleep(3)
            except Exception as e:
                print(f"Error navegando en {empresa}: {e}")
                envio_error(empresa, fechaHora)
                continue
                
            try:
                body=driver.find_element(By.XPATH, "/html/body")
                if body.get_attribute('innerHTML')=="<br>Error al leer datos(-999)" or body.get_attribute('innerHTML')=="Error 500":

                    if monitor_directory(driver):

                        sleep(3)                    
                        print(empresa+" Procesado!")
                        driver.back()
                        driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]').click()
                        sleep(5)
                    else:
                        mensaje="No Se ha realizado la descarga del XML con 10 intentos de: "+empresa
                        envio_correo.correo(mensaje,empresa)
                        continue

                
                else:
                    driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]').click()
                    sleep(5)
                mensaje="Se ha realizado la descarga del XML de: "+empresa
                envio_correo.correo(mensaje,empresa)
            
            except Exception as e:
                print(f"Error no carga el body {e} ")
                envio_error(empresa,fechaHora)
        
        except Exception as e:
            print(f"Error general {e}")
            envio_error(empresa, fechaHora)
           
           
    driver.quit()
    
def envio_error(empresa, fechaHora):
    print(empresa+": NO procesado, error en el sitio web de SII")
    ruta_imagen = fr"C:\Virginia\P10 - Factoring\XML\Errores\{empresa}_{fechaHora}_error.png"
    driver.save_screenshot(ruta_imagen)
    mensaje="NO procesado, error en el sitio web de SII al descargar: "+empresa
    envio_correo.correo(mensaje,empresa, ruta_imagen)
