import os
import shutil
from os import makedirs, path, getcwd

ruta_origen = r"C:\\Rendicion\\bestado\\descargados\\"
ruta_destino = r"C:\\Rendicion\bestado\\enviados\\"

def mover_archivos(): 
    
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    
    
    for archivo in os.listdir(ruta_origen):
        ruta_archivo_origen = os.path.join(ruta_origen, archivo)
        ruta_archivo_destino = os.path.join(ruta_destino, archivo)
        
        if os.path.isfile(ruta_archivo_origen):
            if ('carga_rend' not in ruta_archivo_origen):
                shutil.move(ruta_archivo_origen, ruta_archivo_destino)