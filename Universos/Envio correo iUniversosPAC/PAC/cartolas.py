from utils import chrome
from os import * 
from time import sleep
from datetime import date
from utils import diashabiles
import datetime
import os
from shutil import rmtree
import utils.correos as correos

captura_fecha = datetime.datetime.now()
nombre_carpeta=captura_fecha.strftime('%d-%m-%Y')
empresa=''


a = date.today()
b = diashabiles.previo()

ruta_descarga=chrome.ruta_descargas()
ruta_archivos_procesados=ruta_descarga+"\\procesados\\"+nombre_carpeta+"\\"

empresas = ["96.703.230-1","76.215.634-2","76.850.128-9","76.215.637-7","76.215.628-8"]
#empresas = ["76.850.128-9"]
def descargar_informacion():

    
    
    for i in empresas:  
        match i:
            case "76.850.128-9":
                empresa="ATA"
                rut='76850128_9'
            case "76.215.634-2":
                empresa="ADA"
                rut='76215634_2'
            case "76.215.637-7":
                empresa="ARA"
                rut='76215637_7'
            case "76.215.628-8":
                empresa="AMA"
                rut='76215628_8'
            case "96.703.230-1":
                empresa="AXA"
                rut='96703230_1'


        correos.envio_correo(ruta_archivos_procesados,empresa,rut)
