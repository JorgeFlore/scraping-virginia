from selenium.webdriver.chrome.options import Options
from os import *
import os
from selenium import webdriver
from fake_useragent import UserAgent
import random


fecha_recibida=''
empresa_recibida=''

def ruta_descargas():

    ruta="\\\\columbia\\cargas_masivas\\informacion_de_pagos_bancos\\BCI\\"
    #ruta=os.path.join(os.getcwd(), "descargas\\")
   
   
    # print(ruta)

    return ruta

ruta_descarga=ruta_descargas()


def opciones_chrome():
    ua = UserAgent()
    user_agent = ua.random
    
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--no-sandbox')
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("log-level=3")      
    prefs ={
    # 'download.default_directory': ruta_descarga+fecha_recibida+'\\'+empresa_recibida,
    # 'download.default_directory': os.path.join(ruta_descarga, fecha_recibida, empresa_recibida),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False,
    "plugins.always_open_pdf_externally": True,
    # "credentials_enable_service": False,
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)

    return driver

