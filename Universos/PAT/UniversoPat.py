import os
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from datetime import date
from utils import chrome
from utils import envio_correo

ruta_descarga=chrome.ruta_descargas()
driver = chrome.opciones_chrome()


fechaActual = date.today()
fechaEnTexto = fechaActual.strftime('%m/%d/%y')
fechaEnTexto=fechaEnTexto.replace('/','')
fechaActualFormateada=fechaEnTexto.replace('/','')
print(fechaEnTexto)

ADA="30374126_BASEINSTDECARGO"
ATA="34813361_BASEINSTDECARGO"
ARA="30374517_BASEINSTDECARGO"
AMA="30374339_BASEINSTDECARGO"
AXA="27992048_BASEINSTDECARGO"


empresa=""
empresas = ['96703230_1']
usuario = ['adm_27992048']

#empresas = ['96703230_1']
#usuario = ['adm_27992048']


driver.get("https://transdata.cl/transdata/")

for i,j in zip(empresas,usuario):   

     match i:
        case "76850128_9":
            empresa="Nueva Atacama"
        case "76215634_2":
            empresa="Aguas del Altiplano"
        case "76215637_7":
            empresa="Aguas Araucania"
        case "76215628_8":
            empresa="Aguas Magallanes" 
        case "96703230_1":
            empresa="Aguas Decima" 
    
     try: 
    
          usuario=driver.find_element(By.NAME,"j_username")
          usuario.send_keys(j)
          sleep(2.5)
          
          password=driver.find_element(By.NAME,"j_password")
          if empresa == "Nueva Atacama":
              password.send_keys(os.getenv("UNIVERSO_PAT_PASSWORD_NVATACAMA"))
          else:        
            password.send_keys(os.getenv("UNIVERSO_PAT_PASSWORD"))
          driver.find_element(By.CLASS_NAME, "boton").click()
          sleep(1.5)
          driver.find_element(By.ID, "btn_122").click()
          sleep(1.5)
          driver.find_element(By.NAME, "idComercio").click()
          driver.find_element(By.CLASS_NAME, "boton").click()
          driver.find_element(By.XPATH, "/html/body/div/div[4]/ul/li[4]/a").click()

          sleep(3)

          input=''
          contador=1
          identificador=True
          texto=''

          while identificador==True:
              texto=driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[1]').text
              #print(texto[0:23])
              if texto[0:24]==ADA:
                  print(texto[0:24])
                  print(contador)
                  input=driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[4]/input')
                  input.send_keys(i+"_TBUNIVERSO.TXT")
                  sleep(0.5)
                  driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[5]/input').click()
                  driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[4]/a[4]/span').click()
                  identificador=False

              elif texto[0:24]==ARA:
                   input=driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[4]/input')
                   input.send_keys(i+"_TBUNIVERSO.TXT")
                   sleep(0.5)
                   driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[5]/input').click()
                   driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[4]/a[4]/span').click()
                   identificador=False
              elif texto[0:24]==AMA:
                   input=driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[4]/input')
                   input.send_keys(i+"_TBUNIVERSO.TXT")
                   sleep(0.5)
                   driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[5]/input').click()
                   driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[4]/a[4]/span').click()
                   identificador=False
              elif texto[0:24]==ATA:
                   input=driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[4]/input')
                   input.send_keys(i+"_TBUNIVERSO.TXT")
                   sleep(0.5)
                   driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[5]/input').click()
                   driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[4]/a[4]/span').click()
                   identificador=False
              elif texto[0:24]==AXA:
                   input=driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[4]/input')
                   input.send_keys(i+"_TBUNIVERSO.TXT")
                   sleep(0.5)
                   driver.find_element(By.XPATH, '/html/body/div/div[5]/div/div/form/div/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr['+str(contador)+']/td[5]/input').click()
                   driver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[4]/a[4]/span').click()
                   identificador=False
              contador+=1
              sleep(5)
          #driver.find_element(By.XPATH, "*//span[text()='Cerrar sesión']/..")
          #driver.quit()
          
          mensaje="Se ha realizado la descarga de: "+i+"_TBUNIVERSO.TXT"
          #envio_correo.correo(mensaje,empresa,ruta_descarga+"\\")
          
     except:
          mensaje="Ha ocurrido un error al descargar el archivo universo de "+empresa
         # envio_correo.correo(mensaje,empresa," ")
          driver.save_screenshot("Errores/"+j+" "+fechaActualFormateada+" error.png") 
driver.quit()