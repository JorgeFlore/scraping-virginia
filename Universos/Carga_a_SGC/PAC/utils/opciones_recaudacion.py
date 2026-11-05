from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

def ingresar_opciones_recaudacion(driver, max_reintentos=6):
    opciones_recaudacion = (
        '//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1_T"]/span',
        '//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1i2_T"]',
        '//*[@id="ctl00_xcpnMenu_xmenMenuHor_DXI1i2i0_T"]/span'
    )

    intento = 0

    while intento < max_reintentos:
        try:
            print(f"Intento {intento + 1} de {max_reintentos}: Ingresando las opciones...")

            for j in opciones_recaudacion:
                elemento = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, j)))
                elemento.click()
                sleep(2)

            print("Se ingresaron las opciones correctamente")
            break 

        except (TimeoutException, ElementClickInterceptedException) as e:
            print(f"Error al intentar hacer clic en una opción: {e}")
            driver.refresh()  
            sleep(5)  
            intento += 1

    if intento == max_reintentos:
        raise Exception("No se pudo ingresar a las opciones después de varios intentos.")


