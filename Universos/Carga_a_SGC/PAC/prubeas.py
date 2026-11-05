
from time import sleep
import time
from selenium.webdriver.common.by import By
from utils import chrome
from utils import envio_correo
from utils.iniciar_sesion import cargar_pagina, verificar_contenido_pagina_inicial, verificar_input, inicar_sesion
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

import os
import shutil
from os import remove
from bs4 import BeautifulSoup
import pandas as pd
import os.path as path
import datetime


def cargar_pagina(driver_options, url, intento_max=5, timeout=20):
    intento = 0
    while intento < intento_max:
        try:
            driver = driver_options()
            driver.set_page_load_timeout(timeout)
            driver.get(url)
            print("Pagina procesada correctamente")
            driver.quit()
            return driver
        except TimeoutException:
            print(f"Intento {intento+1}/{intento_max}: La página tardó más de {timeout} seg en cargar.")
        except WebDriverException:
            print(f"Intento {intento+1}/{intento_max}: La pagina no cargo, reintentando...")
        except Exception as e:
            print(f"Error inesperado al cargar la pagina inicial {e}")
        
        driver.quit()
        intento += 1
        sleep(3)

while True:
    cargar_pagina(
        driver_options=chrome.opciones_chrome,
        url="https://sgc-araqa.aguasnuevas.cl/",
        # url="https://sgc-ara.aguasnuevas.cl/",
    )