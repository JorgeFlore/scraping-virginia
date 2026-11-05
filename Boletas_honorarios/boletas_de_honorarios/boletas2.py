from os import * 
from datetime import date
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime
from utils import chrome
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from glob import glob
import os
from shutil import rmtree



for archivo in glob('*.log'):
    os.remove(archivo)

ruta_descarga=r"\\texas\RECUPERACION REPORTES CONTABILIDAD\\BH_Scraping\\Boletas de honorarios"
ruta2=r"\\columbia\\BH"

#fechaEnTexto = fechaActual.strftime('%d/%m/%Y')

hoy = datetime.datetime.utcnow()
nombre_carpeta=hoy.strftime('%d-%m-%Y')
captura_fecha=hoy.strftime('%Y/%m/%d')
#fecha_hoy=hoy.strftime('%d/%m/%Y')
fecha_hoy='29/02/2024'
nombre_archivo=captura_fecha.replace('/','')

empresa=""

descargas = os.path.abspath('descargas', nombre_carpeta)




def descargar_boletas_de_honorarios():
    if os.path.isdir(descargas):
        rmtree(descargas)
    empresas = ['768501289','760386596','762156342','762156377','762156288','760454915','967032301']
    clave = [c.strip() for c in os.getenv("SII_CLAVES", "").split(",") if c.strip()]


    
    for i,j in zip(empresas,clave):      
            sleep(2)
            match i:
                    case "760454915":
                        empresa="ENER"
                    case "768501289":
                        empresa="ATA"
                    case "760386596":
                        empresa="AN"
                    case "762156342":
                        empresa="ADA"
                    case "762156377":
                        empresa="ARA"
                    case "762156288":
                        empresa="AMA"
                    case "967032301":
                        empresa="AXA"


            sleep(10)
            driver = chrome.opciones_chrome(nombre_carpeta,empresa)
            if os.path.isdir(ruta2, "descargas\\"+nombre_carpeta):
                mkdir(ruta2, "descargas\\"+nombre_carpeta+"\\"+empresa)
            else:
                mkdir(ruta2, "descargas\\"+nombre_carpeta)
                mkdir(ruta2, "descargas\\"+nombre_carpeta+"\\"+empresa)
                
            driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")

            

            print(empresa+": Procesando...")
            rut=driver.find_element(By.ID, "rutcntr")
            rut.send_keys(i)
    
            password=driver.find_element(By.ID, "clave")
            password.send_keys(j)
    
            sleep(2)
            driver.find_element(By.CSS_SELECTOR, "button.btn.btn-default").click()
            sleep(5)
    
            try:
                driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary").click()
            except:
                #body.get_attribute('innerHTML')=="Error 500":
                pass
            
            
            
            driver.get("https://loa.sii.cl/cgi_IMT/TMBCOC_MenuConsultasContribRec.cgi?dummy=1461943244650")
            sleep(3)
            
            #2024
            driver.find_element(By.XPATH, '//*[@id="cmdconsultar124"]').click()
            sleep(2)
            try:
                driver.find_element(By.XPATH, "*//table/tbody/tr[3]/td[1]/font/a[text()='ENERO']").click()
                driver.find_element(By.XPATH, "/html/body/div[3]/center/center/form[2]/table/tbody/tr/td[4]/input").click()
            except:
                pass

            sleep(2)
            for archivo in glob(os.path.join(os.getcwd(), "descargas\\"+nombre_carpeta+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.xls")):
                os.rename(archivo, os.path.join(os.getcwd(), "descargas\\"+nombre_carpeta+"\\"+empresa+"\\"+nombre_archivo+"_ENERO_"+empresa+".xls"))
            
            driver.back()
            try:
                driver.find_element(By.XPATH, '/html/body/div[3]/center/table[2]/tbody/tr[6]/td/table/tbody/tr[4]/td[1]/font/a').click()
                driver.find_element(By.XPATH, '/html/body/div[3]/center/center/form[2]/table/tbody/tr/td[4]/input').click()
                #driver.find_element(By.XPATH, "//table/tbody/tr[26]/td[1]/a/img").click()
                print(driver.find_element(By.XPATH, "//table/tbody/tr[26]/td[1]/a/img"))
                #//table/tbody/tr[26]/td[4]
            except:
                pass
            sleep(3)
            #fecha_capturada=driver.find_element(By.XPATH, "//table/tbody/tr/td[text()='"+str(fecha_hoy)+"']")
            #driver.find_element(By.XPATH, "//table/tbody/tr/td[1]/a/img").click()
            
            #print(fecha_capturada)

            #identificador=True
            #contador=4
            #/table/tbody/tr[3]/td[4]
            #while identificador==True:                
            #    fecha_capturada=driver.find_element(By.XPATH, "//table/tbody/tr["+str(contador)+"]/td["+str(contador)+"]").text
            #    contador+=1
            #    if fecha_capturada=='29/02/2024':
            #        print()
            #        identificador=False
            #
            #print(contador)

            
            for archivo in glob(os.path.join(ruta_descarga, empresa, 'TMBCOC_InformeMensualBheRec.xls')):
                os.rename(archivo, os.path.join(ruta_descarga, empresa, f'{nombre_archivo}_FEBRERO_{empresa}.xls'))
            
            for pdf in glob(os.path.join(os.getcwd(), "descargas\\"+nombre_carpeta+"\\"+empresa+"\\TMBCOT_ConsultaBoletaPdf.cgi")):
                os.rename(pdf, os.path.join(os.getcwd(), "descargas\\"+nombre_carpeta+"\\"+empresa+"\\"+nombre_archivo+"_FEBRERO_"+empresa+".pdf"))
            
            
            driver.back()
            sleep(2)
            try:
                driver.find_element(By.XPATH, '/html/body/div[3]/center/table[2]/tbody/tr[6]/td/table/tbody/tr[5]/td[1]/font/a').click()
                driver.find_element(By.XPATH, '/html/body/div[3]/center/center/form[2]/table/tbody/tr/td[4]/input').click()
            except:
                #body.get_attribute('innerHTML')=="Error 500":
                pass

            sleep(3)
            for archivo in glob(os.path.join(os.getcwd(), "descargas\\"+nombre_carpeta+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.xls")):
                os.rename(archivo, os.path.join(os.getcwd(), "descargas\\"+nombre_carpeta+"\\"+empresa+"\\"+nombre_archivo+"_MARZO_"+empresa+".xls"))
            driver.back()
            sleep(5)
            
            driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]/a')
            driver.quit()
        
    
    
    driver.quit()
    
    

