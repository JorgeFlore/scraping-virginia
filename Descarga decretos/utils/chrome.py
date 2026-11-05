from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def opciones_chrome(ruta_descarga):
    options = Options()

    # Crear un perfil temporal (evita que Chrome recuerde contraseñas)
    user_data_dir = os.path.abspath("chrome_profile_temp")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    prefs = {
        "download.default_directory": ruta_descarga,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 1,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    options.add_argument("--start-maximized")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    return driver
