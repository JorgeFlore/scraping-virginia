from time import sleep
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging


def procesar_mes(driver, year, mes, max_intentos=2):
    intentos = 0
    while intentos < max_intentos:
        try:
            driver.get("https://loa.sii.cl/cgi_IMT/TMBCOC_MenuConsultasContribRec.cgi?dummy=1461943244650")
            sleep(3)  

            
            year_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/center/table[3]/tbody/tr[2]/td[2]/div/font/select"))
            )
            
            select = Select(year_element)

            # Seleccionar el año
            select.select_by_value(str(year))
            print(f"\nAño {year} seleccionado correctamente.")
            logging.info(f"Año {year} seleccionado correctamente.")

            # Hacer clic en el botón de consulta
            driver.find_element(By.XPATH, '//*[@id="cmdconsultar124"]').click()

            return None

        except (TimeoutException, NoSuchElementException) as e:
            intentos += 1
            print(f"Intento {intentos}/{max_intentos}: No se pudo seleccionar el año {year} en el mes {mes}. Reintentando...")
            logging.error(f"Intento {intentos}/{max_intentos}: No se pudo seleccionar el año {year} en el mes {mes}. Reintentando...")
            
            if intentos > max_intentos:
                return f"Error al cambiar el año a {year} en el mes {mes}: Página caída o elemento no encontrado. Detalle: {str(e)}"

        except WebDriverException as e:
            intentos += 1
            print(f"Intento {intentos}/{max_intentos}: Error crítico al cargar la página. Reintentando...")
            logging.error(f"Intento {intentos}/{max_intentos}: Error crítico al cargar la página. Reintentando...")
            if intentos > max_intentos:
                logging.critical(f"Error crítico al cargar la página: {str(e)}")
                return f"Error crítico al cargar la página: {str(e)}"

    return None 


