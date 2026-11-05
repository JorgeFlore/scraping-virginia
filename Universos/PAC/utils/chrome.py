from selenium.webdriver.chrome.options import Options
import os

from selenium import webdriver


#ruta2=r"\\columbia\BH"

#ruta2=os.path.join(os.getcwd(), "descargas")



def ruta_descargas():
    ruta="\\\\columbia\\cargas_masivas\\recaudacion_pac_pat\\Universos\\PAC\\"
    #ruta=os.path.join(os.getcwd(), "descargas\\")
    return ruta

ruta_descarga=ruta_descargas()

def opciones_chrome():
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_experimental_option("prefs", {
    #    
    #  "download.default_directory": r"\\texas\\RECUPERACION REPORTES CONTABILIDAD\\BH_Scraping\\Boletas de honorarios\\"+fecha+"\\"+empresa
    #  })
    #C:\\Users\\manuel.rodriguez\\Desktop\\Scraping\\Boletas de honorarios\\descargas
    prefs ={
    #'download.default_directory': r"\\texas\\RECUPERACION REPORTES CONTABILIDAD\\BH_Scraping\\Boletas de honorarios\\"+fecha+"\\"+empresa,
    'download.default_directory': ruta_descarga,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False,
    "plugins.always_open_pdf_externally": True,
    #"download.default_directory": r"\\texas\\RECUPERACION REPORTES CONTABILIDAD\\BH_Scraping\\Boletas de honorarios\\"+fecha+"\\"+empresa
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)

    return driver

