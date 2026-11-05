from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

def extinciones(driver, ruta_descarga):
    driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div[3]/div/a").click()  # ← Ajustar XPATH si es necesario
                                    
    log_path = os.path.join(ruta_descarga, "log_extinciones.txt")
    with open(log_path, "w", encoding="utf-8") as log:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='content']/div/div/div[2]/div[1]/ul/li[2]/a"))).click()
            print("📥 Iniciando descarga de extinciones...")
            log.write("📥 Iniciando descarga de extinciones...\n")

            sleep(3)

            # 1. Cargar sección extinciones
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "cargaDecretosExtincion"))  # ← Cambiar si tiene otro ID
            ).click()
            sleep(5)
            # 2. Aumentar grilla a 50 filas
            select_element = driver.find_element(By.ID, "dt-length-0")
            Select(select_element).select_by_value("50")
            sleep(2)
            # 3. Esperar carga de tabla
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "grillaArchivosDescargarDE"))
            )
                
            filas = driver.find_elements(By.CSS_SELECTOR, "#grillaArchivosDescargarDE tbody tr")

            if not filas:
                log.write("⚠️ No se encontraron registros en extinciones.\n")
                return

            descargados_ok = 0
            descargados_error = 0

            for i, fila in enumerate(filas, 1):
                columnas = fila.find_elements(By.TAG_NAME, "td")
                if len(columnas) < 6:
                    log.write(f"⚠️ Fila {i}: no tiene suficientes columnas.\n")
                    continue

                reintentos = 2
                exito = False

                for intento in range(1, reintentos + 1):
                    try:
                        boton = columnas[5].find_element(By.CLASS_NAME, "boton-secundario")
                        driver.execute_script("arguments[0].scrollIntoView();", boton)
                        sleep(0.5)
                        boton.click()
                        log.write(f"⬇️ Fila {i}: intento {intento} OK\n")
                        print(f"⬇️ Fila {i}: Descargando archivo (intento {intento})...")
                        exito = True
                        descargados_ok += 1
                        sleep(1.5)
                        break
                    except Exception as e:
                        log.write(f"❌ Fila {i}: Error en intento {intento}: {e}\n")
                        sleep(2)

                if not exito:
                    descargados_error += 1

            # Renombrar archivos no ZIP a .txt
            for archivo in os.listdir(ruta_descarga):
                ruta_archivo = os.path.join(ruta_descarga, archivo)
                if os.path.isfile(ruta_archivo) and not archivo.lower().endswith(".zip"):
                    nuevo_nombre = os.path.splitext(archivo)[0] + ".txt"
                    os.rename(ruta_archivo, os.path.join(ruta_descarga, nuevo_nombre))

            # Descarga masiva si aplica
            try:
                driver.find_element(By.ID, "descargaMasiva").click()
                sleep(2)
                log.write("⬇️ Descarga masiva ejecutada.\n")
            except:
                log.write("⚠️ No se encontró botón de descarga masiva.\n")

            resumen = f"\n✅ Descarga completada. OK: {descargados_ok} | Fallidos: {descargados_error}\n"
            print(resumen)
            log.write(resumen)

        except Exception as e:
            log.write(f"❌ Error general en extinciones: {e}\n")
