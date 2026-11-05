from time import sleep
from selenium.webdriver.common.by import By
from utils import envio_correo
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import os
from bs4 import BeautifulSoup
import pandas as pd
import logging




def guardar_excel(driver, ruta_archivos_procesados, empresa, i, max_intentos=3):
    intentos = 0
    
    while intentos < max_intentos:
        try:
            tabla_universo = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'xgrwResultadoUniverso_DXMainTable'))
            )
            print("Tabla universo cargada correctamente.")
            logging.info("Tabla universo cargada correctamente")

            html = driver.execute_script("return arguments[0].innerHTML;", tabla_universo)
            soup = BeautifulSoup(html, 'html.parser')
            tbody = soup.find('tbody')

            lista_banco = []
            lista_nombre_archivo = []
            lista_leidos = []
            lista_rechazados = []
            lista_aceptados = []
            lista_resultados = []

            for l in tbody.find_all('tr'):    
                columna = l.find_all('td')
                if columna:
                    lista_banco.append(columna[0].text.strip())
                    lista_nombre_archivo.append(columna[1].text.strip())
                    lista_leidos.append(columna[2].text.strip())
                    lista_rechazados.append(columna[3].text.strip())
                    lista_aceptados.append(columna[4].text.strip())
                    lista_resultados.append(columna[5].text.strip())

            dicionario = {
                "banco": lista_banco, 
                "nombre_archivo": lista_nombre_archivo, 
                "leidos": lista_leidos, 
                "rechazados": lista_rechazados, 
                "aceptados": lista_aceptados, 
                "resultados": lista_resultados
            }

            archivos_antes = len(os.listdir(ruta_archivos_procesados))


            df = pd.DataFrame(dicionario)
            ruta_excel = os.path.join(ruta_archivos_procesados, i[0:21] + ".xlsx")

            df.to_excel(ruta_excel, index=False, engine='openpyxl')

            archivo_despues = len(os.listdir(ruta_archivos_procesados))
            if archivos_antes == archivo_despues:
                raise Exception("No se encontro archivo excel en la caperta de descarga")
            
            logging.info(f"Archivo Excel de la empresa {empresa} procesado correctamente en intento {intentos + 1}")
            print(f"Archivo Excel de la empresa {empresa} generado con éxito.")
            return True 
        
        except Exception as e:
            intentos += 1
            logging.warning(f"Error en el intento {intentos}/{max_intentos} al procesar la tabla para {empresa}. Error: {e}")
            print(f"Error en el intento {intentos}/{max_intentos} al procesar la tabla para {empresa}. Reintentando...")
            sleep(5) 
            
    mensaje = f"Se ha detectado un problema al procesar la tabla universo y generar el archivo Excel para la empresa {empresa} después de {max_intentos} intentos."
    logging.error(mensaje)
    envio_correo.correo(mensaje, empresa)
