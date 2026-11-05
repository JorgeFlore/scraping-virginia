from time import sleep
import os
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from utils.procesar_mes import procesar_mes
import logging

def contar_archivos_en_carpeta(carpeta):
    return len(os.listdir(carpeta))


def descargar_archivo(driver, year, mes, carpeta_descargas, max_intentos_pagina=3, max_intentos_descarga=3):
    intentos_pagina = 0
    while intentos_pagina < max_intentos_pagina:
        try:
            titulo_pagina = driver.title.strip()

            if titulo_pagina != "INFORME ANUAL DE BOLETAS DE HONORARIOS ELECTRONICAS RECIBIDAS":
                raise WebDriverException("Pagina de INFORME ANUAL caida. No se logra concretar el proceso de descarga")

            # Intentar encontrar y hacer clic en el mes
            try:
                enlace_mes = driver.find_element(By.XPATH, f"*//td[1]/font/a[text()='{mes}']")
                enlace_mes.click()
                print(f"Se hizo clic en el mes {mes}, pasando a la página de descarga.")
                logging.info(f"Se hizo clic en el mes {mes}, pasando a la página de descarga.")

                sleep(3)
                titulo_pagina = driver.title.strip()

                if titulo_pagina != "INFORME MENSUAL DE BOLETAS RECIBIDAS":
                    raise WebDriverException("Pagina de INFORME MENSUAL caida. No se logra concretar el proceso de descarga")
                

                archivos_antes = contar_archivos_en_carpeta(carpeta_descargas)

                intentos_descarga = 0
                while intentos_descarga < max_intentos_descarga:
                    try:
                        # Hacer clic en el botón de descarga
                        driver.find_element(By.XPATH, '/html/body/div[2]/center/center/form[2]/table/tbody/tr/td[4]/input').click()

                        sleep(5)

                        # Contar archivos después de la descarga
                        archivos_despues = contar_archivos_en_carpeta(carpeta_descargas)

                        if archivos_despues > archivos_antes:
                            print(f"Descarga completada para {mes}.")
                            logging.info(f"Descarga completada para {mes}.")
                            return None
                        else:
                            logging.error(f"Intento {intentos_descarga+1}: No se descargó el archivo de {mes}. Reintentando...")
                            raise WebDriverException(f"Intento {intentos_descarga+1}: No se descargó el archivo de {mes}. Reintentando...")

                    except WebDriverException as e:
                        print(e)
                        intentos_descarga += 1
                        driver.back()
                        sleep(3)

                # Si después de 3 intentos no se descarga, lanzar error
                logging.critical(f"Error crítico: No se pudo descargar el archivo de {mes} después de {max_intentos_descarga} intentos.")
                raise WebDriverException(f"Error crítico: No se pudo descargar el archivo de {mes} después de {max_intentos_descarga} intentos.")

            except NoSuchElementException:
                print(f"No hay datos para el mes {mes}. Continuando sin error.")
                logging.info(f"No hay datos para el mes {mes}. Continuando sin error.")
                return None 

        except WebDriverException as e:
            intentos_pagina += 1
            print(f"Intento {intentos_pagina}/{max_intentos_pagina}: Error en la página. Reintentando...")
            logging.error(f"Intento {intentos_pagina}/{max_intentos_pagina}: Error en la página. Reintentando...")
            
            if intentos_pagina >= max_intentos_pagina:
                logging.critical(f"Error al descargar {mes}: {str(e)}")
                return f"Error al descargar {mes}: {str(e)}"
            procesar_mes(driver, year, mes)


def descargar_pdf(driver, pdf, carpeta_descargas, max_intentos=3):
    intentos = 0
    archivos_antes = contar_archivos_en_carpeta(carpeta_descargas)

    while intentos < max_intentos:
        try:
            pdf.click()
            # print(f"Intento {intentos+1}/{max_intentos}: Descargando pdf...")
            sleep(2)

            archivos_despues = contar_archivos_en_carpeta(carpeta_descargas)

            if archivos_despues > archivos_antes:
                print("Descarga de PDF completada con éxito.")
                logging.info("Descarga de PDF completada con éxito.")
                return True  # Éxito

            else:
                print(f"Intento {intentos+1}: No se detectó la descarga del pdf. Reintentando...")

        except WebDriverException as e:
            print(f"Intento {intentos+1}: Error al intentar descargar el PDF: {str(e)}")
            logging.error(f"Intento {intentos+1}: Error al intentar descargar el PDF: {str(e)}")

        intentos += 1
        driver.back()  # Volver atrás para reintentar la descarga
        sleep(3) 

    print("Error: No se pudo descargar el PDF después de varios intentos.")
    logging.critical("Error: No se pudo descargar el PDF después de varios intentos.")
    return False  # Falla después de los intentos permitidos



def renombrar_archivo(descargas, empresa, nombre_archivo, mes):
    extensiones = ["cgi", "xls"]
    nombres_posibles = [
        "TMBCOC_InformeMensualBheRec",
        "file_informeMensualREC"
    ]
    
    for ext in extensiones:
        for nombre_base in nombres_posibles:
            ruta_archivo = os.path.join(descargas, empresa, f"{nombre_base}.{ext}")
            if os.path.isfile(ruta_archivo):
                nueva_ruta = os.path.join(descargas, empresa, f"{nombre_archivo}_{mes}_{empresa}.xls")
                os.rename(ruta_archivo, nueva_ruta)
    
