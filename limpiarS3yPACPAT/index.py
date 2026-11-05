import boto3
import shutil
import os

def limpiar():
    
    carpeta_origen = r"\\columbia\cargas_masivas\recaudacion_pac_pat"  
    carpeta_destino = r"\\columbia\cargas_masivas\recaudacion_pac_pat\2026" 

    
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)  


    for archivo in os.listdir(carpeta_origen):
        ruta_origen = os.path.join(carpeta_origen, archivo)
        ruta_destino = os.path.join(carpeta_destino, archivo)


        if os.path.isfile(ruta_origen):

            shutil.move(ruta_origen, ruta_destino)
            print(f"Archivo movido: {ruta_origen} -> {ruta_destino}")

    print("Todos los archivos han sido movidos.")
