import os
import shutil

ruta_origen = 'C:/B.Estado - Compra Aqui/descargados/'
ruta_destino = 'C:/B.Estado - Compra Aqui/enviados/'

def mover_archivos(): 
    # Asegúrate de que la ruta de destino existe
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    
    # Itera sobre los archivos en la carpeta de origen
    for archivo in os.listdir(ruta_origen):
        ruta_archivo_origen = os.path.join(ruta_origen, archivo)
        # Verifica que sea un archivo y no una carpeta
        if os.path.isfile(ruta_archivo_origen):
            ruta_archivo_destino = os.path.join(ruta_destino, archivo)
            shutil.move(ruta_archivo_origen, ruta_archivo_destino)