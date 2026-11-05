from os import * 
from time import sleep
from selenium.webdriver.common.by import By
import datetime
from utils import chrome
from utils import envio_correo
from utils import calcular_meses
from utils import credenciales
from utils import descargas_archivos
from utils import procesar_mes
from glob import glob
import os
from shutil import rmtree
import logging


correos=credenciales.listar_correos()
ruta_descarga=chrome.ruta_descargas()

for archivo in glob('geckodriver.log'):
    os.remove(archivo)

captura_fecha = datetime.datetime.now()
# captura_fecha = "16/02/2025"
# captura_fecha = datetime.datetime.strptime(captura_fecha, "%d/%m/%Y")

meses = calcular_meses.calcular_meses(captura_fecha)

ayer = captura_fecha - datetime.timedelta(days=1)
dia_anterior=ayer.strftime('%d/%m/%Y')

fecha_hoy=captura_fecha.strftime('%d/%m/%Y')
nombre_carpeta=captura_fecha.strftime('%d-%m-%Y')
nombre_archivo=fecha_hoy.replace('/','')
descargas=ruta_descarga+nombre_carpeta
data_list=[]
rescatar_fecha=""


def descargar_boletas_de_honorarios():
    empresa=""
    diferencia=0
    if os.path.isdir(descargas):
        rmtree(descargas)

    empresas=credenciales.leer_csv()   
    
    for i in empresas:

        try:                    
            sleep(2)
            empresas_dict = {
                "777373099": "ASOL",
                "760454915": "ENER",
                "768501289": "ATA",
                "760386596": "AN",
                "762156342": "ADA",
                "762156377": "ARA",
                "762156288": "AMA",
                "967032301": "AXA",
            }
            empresa = empresas_dict.get(i[0], empresas_dict[i[0]])

            driver = chrome.opciones_chrome(nombre_carpeta,empresa)
            if os.path.isdir(descargas):
                mkdir(descargas+"\\"+empresa)
            else:
                mkdir(descargas)
                mkdir(descargas+"\\"+empresa)
                
            driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")

        
            print(empresa+": Procesando...")
            logging.info(empresa+": Procesando...")
            
            rut=driver.find_element(By.ID, "rutcntr")
            rut.send_keys(i[0])
    
            password=driver.find_element(By.ID, "clave")
            password.send_keys(i[1])
    
            sleep(2)
            driver.find_element(By.CSS_SELECTOR, "button.btn.btn-default").click()
            sleep(5)

            if driver.current_url == "https://zeusr.sii.cl/cgi_AUT2000/CAutInicio.cgi":
                logging.critical(f"Credenciales invalidas para {empresa}. Es posible que hayan sido actualizadas.")
                mensaje = f"Credenciales invalidas para {empresa}. Es posible que hayan sido actualizadas."
                envio_correo.correo(mensaje,empresa)
                driver.quit()
                continue


            carpeta_descargas = os.path.join(descargas, empresa)

            for (year, mes) in meses:
                
                error = procesar_mes.procesar_mes(driver, year, mes)
                if error:
                    mensaje = f"{error}"
                    envio_correo.correo(mensaje,empresa)
                    continue 

                sleep(5)

                error = descargas_archivos.descargar_archivo(driver, year, mes, carpeta_descargas)
                if error:
                    mensaje = f"\n{error}"
                    envio_correo.correo(mensaje,empresa)
                    continue 

                sleep(5) 
                descargas_archivos.renombrar_archivo(descargas, empresa, nombre_archivo, mes)
                
                sleep(5)
            

            ################################################PDF##################################################################
            numero_filas=len(driver.find_elements(By.XPATH, "//*[@class='reporte']/td[1]"))
            numero_fechas=len(driver.find_elements(By.XPATH, f"//*[@class='reporte']/td[text()='{fecha_hoy}']"))
            numero_fechas_dia_anterior=len(driver.find_elements(By.XPATH, f"//*[@class='reporte']/td[text()='{dia_anterior}']"))
            suma_fechas=numero_fechas+numero_fechas_dia_anterior
            diferencia=numero_filas-suma_fechas
            
            if(suma_fechas!=0):
                for i in reversed(range(numero_filas+1)) : 
                    if i==diferencia:
                        break
                    print(i)   
                    pdf=driver.find_element(By.XPATH, f"/html/body/div[2]/center/center/form[1]/table/tbody/tr["+str(i)+"]/td[1]/a/img")
                    rescatar_fecha=driver.find_element(By.XPATH, f"/html/body/div[2]/center/center/form[1]/table/tbody/tr["+str(i)+"]/td[4]").text
                    rescatar_fecha=str(rescatar_fecha)
                    rescatar_fecha=rescatar_fecha.replace('/','')
                    numero_doc=driver.find_element(By.XPATH, " /html/body/div[2]/center/center/form[1]/table/tbody/tr["+str(i)+"]/td[2]").text
                    nombre=driver.find_element(By.XPATH, "/html/body/div[2]/center/center/form[1]/table/tbody/tr["+str(i)+"]/td[6]").text
                    nombre=str(nombre)
                    nombre=nombre.replace('-','')
                    nombre=nombre.replace(' ','_')
                    print(rescatar_fecha)
                    
                    exito = descargas_archivos.descargar_pdf(driver, pdf, carpeta_descargas)
                    if not exito:
                        mensaje = f"Error al descargar el PDF con N de documento {numero_doc} de {nombre} en el mes de {mes}"
                        envio_correo.correo(mensaje, empresa)
                    sleep(7)
                    
                    for archivo_pdf in glob(descargas+"\\"+empresa+"\\TMBCOT_ConsultaBoletaPdf.cgi"):
                        nuevo_nombre = os.path.join(descargas, empresa, f"{rescatar_fecha}_{numero_doc}_{nombre}.pdf")
                        os.rename(archivo_pdf, nuevo_nombre)      
                        # os.rename(archivo_pdf, descargas+"\\"+empresa+"\\"+rescatar_fecha+"_"+numero_doc+"_"+nombre+".pdf")    
                        
            sleep(7)

            mensaje="<h3 style='font-weight: bold'>Los archivos descargados se encuentran en la siguiente ruta:"+" \\\\columbia\\BH\\"+nombre_carpeta+"\\"+empresa+"</h3>"
            driver.back()
            driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]/a')
            driver.quit()
            envio_correo.correo(mensaje,empresa)
        
        except:
            mensaje="<h3 style='color:red;'>Error al procesar</h3>: "+empresa
            print("No se puede procesar: "+empresa)
            envio_correo.correo(mensaje,empresa)
    
    driver.quit()




