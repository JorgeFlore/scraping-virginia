import os
from selenium.webdriver.firefox.options import Options
from datetime import date
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import datetime

#from selenium.webdriver.chrome.options import Options




options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", r"C:\Virginia\P10 - Factoring\XML")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
driver = webdriver.Firefox(options=options)


#options = Options()
#options.add_argument("start-maximized")
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option('useAutomationExtension', False)
#options.add_experimental_option("prefs", {
#  "download.default_directory": r"C:\Users\manuel.rodriguez\Desktop\git\AWS_Scraping\Factoring\XML"
#  })
#driver = webdriver.Chrome(options=options)
#driver.maximize_window()



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
    #empresas=ENER,ATA,AN,ADA,ARA,AMA
    empresas = ['768501289','760386596','762156342','762156377','762156288','760454915','967032301']
    clave = [c.strip() for c in os.getenv("SII_CLAVES", "").split(",") if c.strip()]
    fechaHora=str(fechaActualFormateada)+" "+str(horaActual.hour)+" "+str(horaActual.minute)+" "+str(horaActual.second)
    for i,j in zip(empresas,clave):
        try:
            
            driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")
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
            #driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]').click()
            try:
                body=driver.find_element(By.XPATH, "/html/body")
                if body.get_attribute('innerHTML')=="<br>Error al leer datos(-999)" or body.get_attribute('innerHTML')=="":
                    while body.get_attribute('innerHTML')=="<br>Error al leer datos(-999)" or body.get_attribute('innerHTML')=="":
                            driver.save_screenshot("C:\\Virginia\\P10 - Factoring\\XML\\Errores\\"+empresa+" "+fechaHora+" error en descarga.png")
                            print("Error -999 del sitio, volviendo a procesar "+empresa+"...")
                            sleep(2)
                            driver.back()
                            sleep(2)
                            driver.find_element(By.XPATH, "/html/body/form/div/table[2]/tbody/tr/td/p/input").click()
                            body=driver.find_element(By.XPATH, "/html/body")
                            sleep(3)
                            print(empresa+" Procesado!")
                    driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]').click()
                    sleep(7)
                else:
                    driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]').click()
                    sleep(7)
            except:
                driver.find_element(By.XPATH, '//*[@id="conAutenticaCerrar"]').click()
        except:
            print(empresa+": NO procesado, error en el sitio web de SII")
            driver.save_screenshot("C:\\Virginia\\P10 - Factoring\\XML\\Errores\\"+empresa+" "+fechaHora+" error en el sitio.png")
    
    
    driver.quit()
    
    

    