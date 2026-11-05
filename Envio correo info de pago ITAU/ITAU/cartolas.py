from utils import chrome
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
from utils import diashabiles
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import os
from shutil import rmtree
import utils.correos as correos


captura_fecha = datetime.datetime.now()
nombre_carpeta=captura_fecha.strftime('%d-%m-%Y')
empresa=''

a = date.today()
b = diashabiles.previo()

diferente_mes = a.month != b.month

dia_hoy = a.day
dia_previo = b.day

def descargar_informacion():

    ruta_descarga=chrome.ruta_descargas()
    
    empresas = ["76.215.634-2","76.215.637-7","76.215.628-8"]
    #empresas = ["76.215.634-2","76.850.128-9",]
    #
    #if os.path.isdir(ruta_descarga+nombre_carpeta):
    #    rmtree(ruta_descarga+nombre_carpeta)
    #
    #
    for i in empresas:  
        match i:
            case "76.215.634-2":
                empresa="ADA"
            case "76.215.637-7":
                empresa="ARA"
            case "76.215.628-8":
                empresa="AMA"


        correos.envio_correo(ruta_descarga,nombre_carpeta,empresa) # type: ignore
