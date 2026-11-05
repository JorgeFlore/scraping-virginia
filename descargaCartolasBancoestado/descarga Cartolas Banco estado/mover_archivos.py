import os
import shutil



def mover_archivos(): 
    ruta_origen = 'C:\\Users\\jorge.flores\\Documents\\RPA\\Scarping\\descarga Cartolas Banco estado\\descargas\\'
    ruta_destino = 'C:\\Users\\jorge.flores\\Documents\\RPA\\Scarping\\descarga Cartolas Banco estado\\enviados/'
    # Asegúrate de que la ruta de destino existe
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    
    # Itera sobre los archivos en la carpeta de origen
    for archivo in os.listdir(ruta_origen):
        ruta_archivo_origen = os.path.join(ruta_origen, archivo)
        ruta_archivo_destino = os.path.join(ruta_destino, archivo)
        # Verifica que sea un archivo y no una carpeta
        if os.path.isfile(ruta_archivo_origen):
            shutil.move(ruta_archivo_origen, ruta_archivo_destino)