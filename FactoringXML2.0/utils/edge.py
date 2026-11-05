from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


def ruta_descargas():
    ruta = r"C:\Virginia\P10 - Factoring\XML"
    # ruta=r"C:\Users\manuel.rodriguez\Desktop\Scraping\FactoringXML\XML"
    return ruta

ruta_descarga = ruta_descargas()


def opciones_edge():
    # Asegúrate de definir tu ruta aquí o recibirla como parámetro
    # ruta_descarga = r"C:\Virginia\P10 - Factoring\XML" 
    
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    
    # --- NUEVOS ARGUMENTOS DE FUERZA BRUTA ---
    # Esto apaga la protección a nivel de proceso
    options.add_argument("--safebrowsing-disable-download-protection")
    options.add_argument("--safebrowsing-disable-extension-blacklist")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--no-sandbox") # A veces ayuda en entornos restringidos
    # ----------------------------------------

    prefs = {
        "download.default_directory": ruta_descarga,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
        # Agregamos XML a la lista de "nunca preguntar"
        "browser.helperApps.neverAsk.saveToDisk": "application/xml,text/xml",
    }

    options.add_experimental_option("prefs", prefs)

    service = Service(r"C:\bin\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    # --- COMANDO CDP (LA SOLUCIÓN FINAL) ---
    # Esto fuerza al navegador a permitir descargas en esa ruta sin validar seguridad
    params = {
        "behavior": "allow",
        "downloadPath": ruta_descarga
    }
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
    
    return driver
