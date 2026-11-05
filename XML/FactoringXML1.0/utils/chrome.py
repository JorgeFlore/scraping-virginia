from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC



def ruta_descargas():
    ruta=r"C:\Virginia\P10 - Factoring\XML"
    #ruta=r"C:\Users\manuel.rodriguez\Desktop\Scraping\FactoringXML\XML"
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
    "download.extensions_to_open": "xml",
    "safebrowsing.enabled": True
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    return driver
#def opciones_chrome():
#    #driver = webdriver.Chrome(options=options)
#
#    options = Options()
#    options.set_preference("browser.download.folderList", 2)
#    options.set_preference("browser.download.manager.showWhenStarting", False)
#    options.set_preference("browser.download.dir", ruta_descarga)
#    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
#    driver = webdriver.Chrome(options=options)
#
#    return driver