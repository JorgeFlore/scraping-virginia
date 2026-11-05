from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils import chrome
from utils import envio_correo
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import shutil
from os import remove
from bs4 import BeautifulSoup
import pandas as pd
import os.path as path
import datetime


captura_fecha = datetime.datetime.now()
fecha_carpeta=captura_fecha.strftime('%d-%m-%Y')
ruta_descarga_archivos=chrome.ruta_descargas()

driver = chrome.opciones_chrome()
wait = WebDriverWait(driver,timeout=500)

ruta_archivos_procesados=ruta_descarga_archivos+"\\procesados\\"+fecha_carpeta+"\\"

#listado_empresas=['76850128_9_BCHILEU.TXT','76215637_7_BCHILEU.TXT','76215628_8_BCHILEU.TXT']

listado_empresas=['96703230_1_BCHILEU.TXT','76215634_2_BCHILEU.TXT','76850128_9_BCHILEU.TXT','76215637_7_BCHILEU.TXT','76215628_8_BCHILEU.TXT']

driver.get("http://sgc.aguas.local/")
sleep(10)

if os.path.isdir(ruta_archivos_procesados):
    shutil.rmtree(ruta_archivos_procesados)

for i in listado_empresas:


    
    if path.exists(ruta_descarga_archivos+"BCHILEU.TXT"):
        remove(ruta_descarga_archivos+"BCHILEU.TXT")
    if os.path.isdir(ruta_archivos_procesados):
        
       print("directorio existente")
    else:
        os.mkdir(ruta_archivos_procesados)
    try:
        match i:
                case "76215634_2_BCHILEU.TXT":
                    empresa="Aguas del Altiplano"
                case "76850128_9_BCHILEU.TXT":
                    empresa="Nueva Atacama"
                case "76215637_7_BCHILEU.TXT":
                    empresa="Aguas Araucanía"
                case "76215628_8_BCHILEU.TXT":
                    empresa="Aguas Magallanes"
                case "96703230_1_BCHILEU.TXT":
                    empresa="Aguas Décima"

        #wait = WebDriverWait(driver,60)
        #print(i)
        #print(i[0:18]+".csv")
        #def cargar_universo_pac(): 

        
        sleep(5)
        rut=driver.find_element(By.ID,'txtxUsuario_I')
        rut.clear()
        rut.send_keys(os.getenv("SGC_RUT"))
        clave=driver.find_element(By.ID,'txtxContrasena_I')
        clave.clear()
        clave.send_keys(os.getenv("SGC_PASSWORD"))


        seleccionar_empresa=wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='xddlEmpresa_I']")))
        seleccionar_empresa.click()
        sleep(3)
        select_empresa=driver.find_element(By.XPATH, f"//td[text()='{empresa}']")

        sleep(3)
        select_empresa.click()
        sleep(3)
        entrar=driver.find_element(By.ID, 'btnxEntrar')
        entrar.click()





        sleep(5)

        opciones_recaudacion=('//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1_T"]/span','//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1i2_T"]','//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1i2i0_T"]/span')


        for j in opciones_recaudacion:
            elemento = wait.until(EC.element_to_be_clickable((By.XPATH, j)))
            elemento.click()
            sleep(2)

        sleep(7)
        window_before = driver.window_handles[0]
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        sleep(10)        
        archivo = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="UploadFile_TextBox0_Input"]')))
        sleep(10) 
        shutil.copy(ruta_descarga_archivos+i, ruta_archivos_procesados+i)
        sleep(10) 
        shutil.copy(ruta_descarga_archivos+i, ruta_descarga_archivos+"\\BCHILEU.TXT")
        sleep(10) 
        remove(ruta_descarga_archivos+i)
        
        ruta=os.path.abspath(ruta_descarga_archivos+"\\BCHILEU.TXT")
        archivo.send_keys(ruta)

        sleep(10)
        check=driver.find_element(By.ID, 'xrpnlSeleccionar_xrdbPAC_S_D').click()
        siguiente=driver.find_element(By.XPATH, '//*[@id="xbtnSiguientePage1_CD"]/span').click()

        sleep(5)
        
        tabla_universo = wait.until(EC.element_to_be_clickable((By.ID, 'xgrwResultadoUniverso_DXMainTable')))
        html = driver.execute_script("return arguments[0].innerHTML;", tabla_universo)
        soup = BeautifulSoup(html,'html.parser')
        tbody = soup.find('tbody')
        
        lista_banco=[]
        lista_nombre_archivo=[]
        lista_leidos=[]
        lista_rechazados=[]
        lista_aceptados=[]
        lista_resultados=[]
        
        for l in tbody.find_all('tr'):    
            columna = l.find_all('td')
            if(columna != []):
                banco = columna[0].text.strip()
                nombre_archivo = columna[1].text.strip()
                leidos = columna[2].text.strip()
                rechazados = columna[3].text.strip()
                aceptados = columna[4].text.strip()
                resultados = columna[5].text.strip()
                
                lista_banco.append(banco)
                lista_nombre_archivo.append(nombre_archivo)
                lista_leidos.append(leidos)
                lista_rechazados.append(rechazados)
                lista_aceptados.append(aceptados)
                lista_resultados.append(resultados)
            
        dicionario={"banco":lista_banco, "nombre_archivo":lista_nombre_archivo, "leidos":lista_leidos, "rechazados":lista_rechazados, "aceptados":lista_aceptados, "resultados":lista_resultados}
        print(dicionario)
        df = pd.DataFrame(dicionario)
        try:
            df2=df
            df2.reset_index(drop=True)
            print(df2)
            print(i[0:18])
            #df2.to_csv(ruta_archivos_procesados+i[0:18]+'.csv', sep=',', encoding='utf-8',index=False)
            df2.to_excel(ruta_archivos_procesados+i[0:18]+'.xls',index=False, engine='xlwt' )

        except:
            pass
        seleccionar = wait.until(EC.element_to_be_clickable((By.ID, 'xchkSeleccionarTodos_S_D')))
        seleccionar.click()
        sleep(2)
        ejecutar= wait.until(EC.element_to_be_clickable((By.ID, 'xbtnEjecutar_CD')))
        ejecutar.click()    
        sleep(2)    
        boton_aceptar = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="xbtnAceptar"]')))
        boton_aceptar.click()        
        sleep(10)
        driver.switch_to.window(window_before)
        sleep(10)
        salir=driver.find_element(By.XPATH, '//*[@id="ctl00_barra_superior"]/img[2]').click()
        if path.exists(ruta_descarga_archivos+"\\BCHILEU.TXT"):
            remove(ruta_descarga_archivos+"\\BCHILEU.TXT")
        sleep(20)
        
    except:
        driver.quit()
        sleep(10)
        driver.get("http://sgc.aguas.local/")
        pass
driver.quit()