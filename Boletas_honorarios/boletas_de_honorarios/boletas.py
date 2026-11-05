from os import * 
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime
from utils import chrome
# from utils.chrome import  ruta_descargas, opciones_chrome
from utils import envio_correo
from utils import calcular_meses
from utils import credenciales
from glob import glob
import os
from shutil import rmtree
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

correos=credenciales.listar_correos()
ruta_descarga=chrome.ruta_descargas()

for archivo in glob('geckodriver.log'):
    os.remove(archivo)

# captura_fecha = datetime.datetime.now()
captura_fecha = "13/02/2025"
captura_fecha = datetime.datetime.strptime(captura_fecha, "%d/%m/%Y")
mes1=calcular_meses.calcular_mes1(captura_fecha)
mes2=calcular_meses.calcular_mes2(captura_fecha)
mes3=calcular_meses.calcular_mes3(captura_fecha)

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
    #empresas = ['967032301']
    # (claves SII retiradas del repositorio: leer desde credenciales_sii.csv o variables de entorno)

    empresas=credenciales.leer_csv()   
    
    #for row in data_list:
    #    print(row[0])S
    #    print(row[1])

    
    for i in empresas:

        try:                    
            lista_archivos=[]
            sleep(2)
            match i[0]:
                    case "760454915":
                        empresa="ENER"
                    case "768501289":
                        empresa="ATA"
                    # case "760386596":
                    #     empresa="AN" #Volver a descomentar
                    #case "762156342":
                    #    empresa="ADA"
                    case "762156377":
                        empresa="ARA"
                    case "762156288":
                        empresa="AMA"
                    # case "967032301":
                    #     empresa="AXA" #Volver a descomentar

            
            driver = chrome.opciones_chrome(nombre_carpeta,empresa)
            if os.path.isdir(ruta_descarga+nombre_carpeta):
                mkdir(ruta_descarga+nombre_carpeta+"\\"+empresa)
            else:
                mkdir(ruta_descarga+nombre_carpeta)
                mkdir(ruta_descarga+nombre_carpeta+"\\"+empresa)
                
            driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")

        
            print(empresa+": Procesando...")
            rut=driver.find_element(By.ID, "rutcntr")
            rut.send_keys(i[0])
    
            password=driver.find_element(By.ID, "clave")
            password.send_keys(i[1])
    
            sleep(2)
            driver.find_element(By.CSS_SELECTOR, "button.btn.btn-default").click()
            sleep(5)
            
            
            driver.get("https://loa.sii.cl/cgi_IMT/TMBCOC_MenuConsultasContribRec.cgi?dummy=1461943244650")
            sleep(3)


            
            if mes1 in ('NOVIEMBRE', 'DICIEMBRE'):

                    # Espera a que el desplegable del año esté presente
                    año = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/center/table[3]/tbody/tr[2]/td[2]/div/font/select"))
                    )

                    # Seleccionar el año 2024
                    select = Select(año)
                    select.select_by_value("2024")
                    print("Año 2024 seleccionado correctamente.")

                    driver.find_element(By.XPATH, '//*[@id="cmdconsultar124"]').click()

            ##############################################PRIMER EXCEL############################################################
            try:
                     
                    # Haz clic en el enlace correspondiente al mes
                driver.find_element(By.XPATH, "*//td[1]/font/a[text()='"+mes1+"']").click()
                driver.find_element(By.XPATH, '/html/body/div[3]/center/center/form[2]/table/tbody/tr/td[4]/input').click()
                print("Descargando: ",mes1)

            except Exception as e:
                    print("Ocurrió un error:", e)
            sleep(7)
            #import os.path
            if os.path.isfile(os.path.join(descargas+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.cgi")): 
                for excel in glob(os.path.join(descargas+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.cgi")):
                    os.rename(excel, os.path.join(descargas+"\\"+empresa+"\\"+nombre_archivo+"_"+mes1+"_"+empresa+".xls"))
                driver.back()
            

            #año 2025
            driver.find_element(By.XPATH, "/html/body/div[3]/center/table[2]/tbody/tr[6]/td/form/table/tbody/tr/td[1]/div/font/input").click()
            select.select_by_value("2025")
            driver.find_element(By.XPATH, '//*[@id="cmdconsultar124"]').click()
            sleep(7)

            ##############################################SEGUNDO EXCEL############################################################
            try:
                driver.find_element(By.XPATH, "*//td[1]/font/a[text()='"+mes2+"']").click()
                driver.find_element(By.XPATH, '/html/body/div[3]/center/center/form[2]/table/tbody/tr/td[4]/input').click()
                print("Descargando: ",mes2)
                
            except:
                pass
            sleep(7)   
            
            if os.path.isfile(os.path.join(descargas+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.cgi")): 
                for excel in glob(descargas+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.cgi"):
                    os.rename(excel, descargas+"\\"+empresa+"\\"+nombre_archivo+"_"+mes2+"_"+empresa+".xls")
                driver.back()
            
            ##Anio 2025
            sleep(7)


            ##############################################TERCER EXCEL############################################################
            try:
                driver.find_element(By.XPATH, "*//td[1]/font/a[text()='"+mes3+"']").click()
                driver.find_element(By.XPATH, '/html/body/div[3]/center/center/form[2]/table/tbody/tr/td[4]/input').click()
                print("Descargando: ",mes3)
            except:
                pass

            sleep(7)
            if os.path.isfile(os.path.join(descargas+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.cgi")): 
                for excel3 in glob(descargas+"\\"+empresa+"\\TMBCOC_InformeMensualBheRec.cgi"):
                    os.rename(excel3, descargas+"\\"+empresa+"\\"+nombre_archivo+"_"+mes3+"_"+empresa+".xls")
            
            sleep(10)
            ################################################PDF##################################################################
            numero_filas=len(driver.find_elements(By.XPATH, "//*[@class='reporte']/td[1]"))
            numero_fechas=len(driver.find_elements(By.XPATH, f"//*[@class='reporte']/td[text()='{fecha_hoy}']"))
            numero_fechas_dia_anterior=len(driver.find_elements(By.XPATH, f"//*[@class='reporte']/td[text()='{dia_anterior}']"))
            suma_fechas=numero_fechas+numero_fechas_dia_anterior
            diferencia=numero_filas-suma_fechas
            
            #dia_prueba="14/03/2024"
            #try:
            #    pdf2=driver.find_element(By.XPATH, f"//*[@class='reporte']/td[text()='{dia_prueba}']")
            #    for i in pdf2:
            #        i.click()
            #except Exception:
            #    print(pdf2.text)
            if(suma_fechas!=0):
                for i in reversed(range(numero_filas+1)) : 
                    if i==diferencia:
                        break
                    print(i)    
                    pdf=driver.find_element(By.XPATH, f"/html/body/div[3]/center/center/form[1]/table/tbody/tr["+str(i)+"]/td[1]/a/img")
                    rescatar_fecha=driver.find_element(By.XPATH, f"//table/tbody/tr["+str(i)+"]/td[4]").text
                    rescatar_fecha=str(rescatar_fecha)
                    rescatar_fecha=rescatar_fecha.replace('/','')
                    numero_doc=driver.find_element(By.XPATH, "//table/tbody/tr["+str(i)+"]/td[2]").text
                    nombre=driver.find_element(By.XPATH, "//table/tbody/tr["+str(i)+"]/td[6]").text
                    nombre=str(nombre)
                    nombre=nombre.replace('-','')
                    nombre=nombre.replace(' ','_')
                    print(rescatar_fecha)
                    pdf.click()
                
                    sleep(7)
                    for archivo_pdf in glob(descargas+"\\"+empresa+"\\TMBCOT_ConsultaBoletaPdf.cgi"):
                        os.rename(archivo_pdf, descargas+"\\"+empresa+"\\"+rescatar_fecha+"_"+numero_doc+"_"+nombre+".pdf")                
                    
            
            #for archivos_excel in glob(ruta_descarga+"\\"+nombre_carpeta+"\\"+empresa+"\\"+"*.xls"):
            #    lista_archivos.append(archivos_excel)
            contenido = os.listdir(ruta_descarga+"\\"+nombre_carpeta+"\\"+empresa)

            for elemento in contenido:
                ruta_completa = os.path.join(ruta_descarga+"\\"+nombre_carpeta+"\\"+empresa, elemento)
                if os.path.isfile(ruta_completa):  # miramos si es fichero
                    lista_archivos.append(elemento)
                #print(lista_archivos)
                        
            sleep(7)
            
            mensaje="<h3 style='font-weight: bold'>Los archivos descargados se encuentran en la siguiente ruta:"+" \\\\columbia\\BH\\"+nombre_carpeta+"\\"+empresa+"</h3>"
            driver.back()
            driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]/a')
            driver.quit()
          #  envio_correo.correo(mensaje,empresa)
        except:
            lista_archivos=[]
            mensaje="<h3 style='color:red;'>Error al procesar</h3>: "+empresa
            #envio_correo.correo(mensaje,empresa)
            print("No se puede procesar: "+empresa)
        
    
    
    driver.quit()



    


