import os
import time
from utils import edge
import glob

def monitor_directory(driver:edge):
    path = r"C:\Virginia\P10 - Factoring\XML"
    files_set = set(os.listdir(path))
    tiempo = 0
    contador = 0
    while tiempo <= 5:
        time.sleep(1)  # Espera 1 segundo antes de verificar nuevamente
        tiempo += 1
        print(tiempo)
        current_files = set(os.listdir(path))
        if tiempo == 5 and files_set == current_files:
            driver.refresh()
            tiempo = 0
            contador +=1
            if contador >= 10:
                return False
                
    
    new_files = current_files - files_set # Resta de las files que existian menos las files con el archivo descargado, deberia quedar 1 archivo 
    if new_files:
        for file in new_files:
            print(f"Nuevo archivo descargado: {file}")
            return True
        
def obtener_xml_mas_reciente():
    """
    Busca el archivo XML más reciente en la carpeta de descargas definida.
    Retorna la ruta completa (string) o None si no hay archivos.
    """
    carpeta_xml = r"C:\Virginia\P10 - Factoring\XML"
    
    # Buscamos todos los .xml
    patron = os.path.join(carpeta_xml, "*.xml")
    archivos_xml = glob.glob(patron)
    
    # Si la lista está vacía, retornamos None
    if not archivos_xml:
        return None

    # Buscamos el más nuevo por fecha de creación
    archivo_mas_reciente = max(archivos_xml, key=os.path.getctime)
    # print("Este es el archivo más reciente: " + archivo_mas_reciente)
    
    return archivo_mas_reciente


def ruta_descargas():
    return r"C:\Virginia\P10 - Factoring\XML\Errores"