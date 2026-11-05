from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
import json


def ruta_descargas():
    """Define y retorna la ruta de descarga."""
    return r"C:\Virginia\P10 - Factoring\PDF"


def opciones_edge(directorio_descarga):
    """Configura y retorna el objeto de opciones de Edge."""
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    # Configuración para impresión silenciosa en PDF
    app_state = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }

    prefs = {
        "download.default_directory": directorio_descarga,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "printing.print_preview_sticky_settings.appState": json.dumps(app_state),  # JSON válido
        "savefile.default_directory": directorio_descarga
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument("--kiosk-printing")  # imprime directo sin cuadro de diálogo

    return options
