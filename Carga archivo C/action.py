from selenium.webdriver.common.by import By
import os
from time import sleep
import shutil
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime


def acciones(driver):
   
    driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div[3]/div/a').click()
    #Ingresando a intercambio Bases
    #driver.find_element(By.XPATH, '//*[@id="nu4"]').click()  
    #ingresando a Carga urbano
    driver.find_element(By.XPATH,'//*[@id="a_sap43"]').click()
   

def carga_archivo2(driver, empresa):
    
    # Puedes ajustar el mes actual automáticamente si quieres
    mes = datetime.now().strftime("%Y%m")
    print(mes)  # o usar datetime si quieres automatizarlo

    # Construye la ruta
    ruta = os.path.join(
         fr'C:\Virginia\P02 D2 - Carga de Archivo C\{empresa}\{mes}\A Cargar' )

    print("Buscando archivos en:", ruta)

    if not os.path.exists(ruta):
        print("La ruta no existe:", ruta)
        return

    archivos_txt = [
        f for f in os.listdir(ruta)
        if f.endswith('.txt') and os.path.isfile(os.path.join(ruta, f))
    ]

    if not archivos_txt:
        print("No se encontraron archivos .txt en la ruta:", ruta)
        return

    print("Archivos encontrados:")
    for nombre in archivos_txt:
        print(nombre)
    
     # Crear carpeta 'procesados' si no existe
    carpeta_procesados = os.path.join(ruta, "procesados")
    os.makedirs(carpeta_procesados, exist_ok=True)

    for archivo in archivos_txt:
        ruta_completa = os.path.join(ruta, archivo)
        archivo_input = driver.find_element(By.XPATH, '//*[@id="nombreArchivo"]') 
        archivo_input.send_keys(ruta_completa)
               
        boton_subir_archivo = driver.find_element(By.XPATH, '//*[@id="cargaDecretosConcesion"]')
        boton_subir_archivo.click()

        porcentaje_carga = driver.find_element(By.XPATH,'//*[@id="progress-bar"]')
        

        try:
            WebDriverWait(driver, timeout=180).until(
            lambda d: d.find_element(By.XPATH, '//*[@id="progress-bar"]').text.strip() == "100%"
        )
            print("✅ Carga completada (100%)")
        except:
            print("⚠️ Tiempo de espera agotado esperando que la carga llegue a 100%")
      
   
        print(f"Archivo cargado: {archivo}")


        ruta_destino = os.path.join(carpeta_procesados, archivo)
        shutil.move(ruta_completa, ruta_destino)
        print(f"Archivo: {archivo} movido a: {ruta_destino}")
        sleep(2)
        driver.find_element(By.ID,'btnProcesoTerminado').click()
        
        #boton_nuevo_archivo.click()
        sleep(15)


        



