from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime
import os

def concesiones(driver, ruta_descarga):
    log_path = os.path.join(ruta_descarga, "log_concesiones.txt")
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"📥 Inicio descarga de concesiones: {datetime.now()}\n")

        exitosos = 0
        fallidos = 0

        try:
            driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div[3]/div/a").click()
            print("📥 Iniciando descarga de concesiones...")

            sleep(3)

            # 1. Cargar Listado Decretos de Concesión
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "cargaDecretosConcesion"))
            ).click()
            sleep(5)

            # 1.2. Aumentar filas mostradas
            select_element = driver.find_element(By.ID, "dt-length-0")
            dropdown = Select(select_element)
            dropdown.select_by_value("50")
            sleep(5)

            # 2. Esperar carga de tabla
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "grillaArchivosDescargarDC"))
            )
            sleep(5)

            # 3. Obtener filas
            filas = driver.find_elements(By.CSS_SELECTOR, "#grillaArchivosDescargarDC tbody tr")
            if not filas:
                print("⚠️ No se encontraron registros en concesiones.")
                log_file.write("⚠️ No se encontraron registros en concesiones.\n")
                return

            for i, fila in enumerate(filas, 1):
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) < 6:
                    print(f"⚠️ Fila {i} no tiene suficientes columnas.")
                    log_file.write(f"⚠️ Fila {i} sin columnas suficientes\n")
                    continue

                boton = columnas[5].find_element(By.CLASS_NAME, "boton-secundario")
                descarga_exitosa = False

                for intento in range(3):
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                        sleep(1.5)
                        driver.execute_script("arguments[0].click();", boton)
                        print(f"✅ Fila {i}: Descarga exitosa en intento {intento + 1}")
                        log_file.write(f"✅ Fila {i}: Descarga exitosa en intento {intento + 1}\n")
                        exitosos += 1
                        descarga_exitosa = True
                        break
                    except Exception as e:
                        print(f"⚠️ Fila {i}: Error en intento {intento + 1}: {e}")
                        log_file.write(f"⚠️ Fila {i}: Error intento {intento + 1}: {e}\n")
                        sleep(1.5)

                if not descarga_exitosa:
                    print(f"❌ Fila {i}: Falló la descarga tras 3 intentos.")
                    log_file.write(f"❌ Fila {i}: Falló descarga tras 3 intentos.\n")
                    fallidos += 1

            # 4. Descarga Masiva
            try:
                driver.find_element(By.ID, "descargaMasiva").click()
                sleep(2)
                print("📦 Descarga masiva ejecutada.")
                log_file.write("📦 Descarga masiva ejecutada.\n")
            except Exception as e:
                print(f"⚠️ Error al hacer clic en descarga masiva: {e}")
                log_file.write(f"⚠️ Error al hacer clic en descarga masiva: {e}\n")

            print("✅ Proceso de descarga completado.")
            log_file.write(f"✅ Total OK: {exitosos}, ❌ Fallidos: {fallidos}\n")

        except Exception as e:
            print(f"❌ Error general en concesiones: {e}")
            log_file.write(f"❌ Error general: {e}\n")

# Renombrar archivos no .zip agregando .txt
    for archivo in os.listdir(ruta_descarga):
        ruta_archivo = os.path.join(ruta_descarga, archivo)

        if os.path.isfile(ruta_archivo):
            nombre, extension = os.path.splitext(archivo)

            # Si no tiene extensión o no es .zip, y no termina en .txt, renombrar
            if extension.lower() != ".zip" and not archivo.lower().endswith(".txt"):
                nuevo_nombre = f"{archivo}.txt"
                nueva_ruta = os.path.join(ruta_descarga, nuevo_nombre)

                try:
                    os.rename(ruta_archivo, nueva_ruta)
                    print(f"📄 Renombrado: {archivo} → {nuevo_nombre}")
                except Exception as e:
                    print(f"⚠️ Error al renombrar {archivo}: {e}")
