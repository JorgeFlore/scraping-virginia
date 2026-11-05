from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
from selenium.webdriver.common.by import By
from datetime import date
import os
from glob import glob
from utils import chrome
from utils import envio_correo


ruta_descarga=chrome.ruta_descargas()
driver = chrome.opciones_chrome()
wait = WebDriverWait(driver,300)


empresa=""
empresas = [' 96.703.230-1 ',' 76.215.634-2 ',' 76.850.128-9 ',' 76.215.637-7 ',' 76.215.628-8 ']
rut = ['96703230_1','76215634_2','76850128_9','76215637_7','76215628_8']
#empresas = ' 76.215.634-2 ',' 76.850.128-9 ',' 76.215.637-7 ',' 96.703.230-1 ',' 76.215.628-8 '
#rut =['76215634_2','76850128_9','76215637_7','96703230_1',]

driver.get("https://login.portalempresas.bancochile.cl/bancochile-web/empresa/login/index.html#/login")

fechaActual = date.today()
fechaEnTexto = fechaActual.strftime('%d/%m/%Y')
fechaActualFormateada=fechaEnTexto.replace('/','')

usuario = wait.until(EC.element_to_be_clickable((By.ID,"iduserName")))
usuario.send_keys(os.getenv("UNIVERSO_PAC_USUARIO"))
usuario=driver.find_element(By.ID,"iduserName")
#usuario
password=driver.find_element(By.NAME,"password")
password.send_keys(os.getenv("UNIVERSO_PAC_PASSWORD"))
driver.find_element(By.ID, "idIngresar").click()





for i,j in zip(empresas, rut):
    match i:
        case " 76.850.128-9 ":
            empresa="Nueva Atacama"
        case " 76.215.634-2 ":
            empresa="Aguas del Altiplano"
        case " 76.215.637-7 ":
            empresa="Aguas Araucania"
        case " 76.215.628-8 ":
            empresa="Aguas Magallanes"
        case " 96.703.230-1 ":
            empresa="Aguas Décima"

    try:    
        
        seleccionar_empresa=wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='input-selector']/div[2]")))
        seleccionar_empresa.click()

        xpath = f"//span[text()='{i}']/.."
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", element)

        sleep(5)

        opciones = ("nivel1-5000","nivel2-5400","nivel3-5422")
        
        for op in opciones:
            el = wait.until(EC.element_to_be_clickable((By.ID, op)))
            el.click()


        descarga_universo=wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main-portal"]/section/div/div[1]/div/div[2]/div/div[2]/div[3]/file-download/a')))
        descarga_universo.click()

        sleep(20)

        for archivo in glob(ruta_descarga+"\\Universo Conv.*.txt"):
            os.rename(archivo, ruta_descarga+"\\"+j+"_BCHILEU.TXT")

        mensaje="Se ha realizado la descarga de: "+j+"_BCHILEU.TXT"
        #envio_correo.correo(mensaje,empresa,ruta_descarga+"\\")

    except:
        mensaje="Ha ocurrido un error al descargar el archivo universo de "+empresa
        #envio_correo.correo(mensaje,empresa," ")
        print("Error al procesar "+i)
        driver.save_screenshot("C:\\Scraping\\Universos\\PAT\\utils\\Error en sitio.png")

driver.quit()     