from selenium.webdriver.chrome.options import Options
import os

from selenium import webdriver


def ruta_descargas():
    ruta="\\\\columbia\\cargas_masivas\\recaudacion_pac_pat\\Universos\\PAT\\"
    # ruta="C:\\Users\\diomedes.mora\\Documents\\GitHub\\PAT"
    # ruta = os.path.join(os.path.expanduser("~"), "Documents", "GitHub", "PAT")
    print(ruta)
    return ruta

ruta_descarga=ruta_descargas()

def opciones_chrome():
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("window-size=800,1050")
    options.add_argument("window-position=0,0")
    options.add_argument("log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    prefs ={
    'download.default_directory': ruta_descarga,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False,
    "plugins.always_open_pdf_externally": True,
    "credentials_enable_service" : False,
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)

    return driver

