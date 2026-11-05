from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

edge_driver_path = r"C:\Scraping\Descarga decretos\msedgedriver.exe"  # Asegúrate de que este sea el path correcto a tu msedgedriver.exe
service = Service(executable_path=edge_driver_path)

                
def opciones_edge(ruta_descarga):
    options = Options()

    # Configurar descarga sin preguntar
    prefs = {
        "download.default_directory": ruta_descarga,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    driver = webdriver.Edge(options=options)
    return driver
