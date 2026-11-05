from selenium.webdriver.chrome.options import Options
from os import *
import os
from selenium import webdriver




fecha_recibida=''
empresa_recibida=''

def ruta_descargas():

    ruta="\\\\columbia\\cargas_masivas\\recaudacion_pac_pat\\Universos\\PAT\\"
       
    return ruta

ruta_descarga=ruta_descargas()





def opciones_chrome(fecha_recibida,empresa_recibida):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--no-sandbox')      
    prefs ={
    'download.default_directory': ruta_descarga+fecha_recibida+'\\'+empresa_recibida,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False,
    "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)

    return driver

