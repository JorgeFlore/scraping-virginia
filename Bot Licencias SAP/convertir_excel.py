
import pandas as pd
import os

ruta=r"C:\Scraping\Bot Licencias SAP\archivos"
contenido = os.listdir(ruta)

def obtener_csv():
    try:

        pruebas=ruta+r"\usuarios.htm"
        print(pruebas)
        df = pd.read_html(ruta+r"\usuarios.htm")[0]  # El [0] selecciona la primera tabla del archivo HTML

   
        df.to_csv(ruta+r"\usuarios.csv", index=False,header=False,sep=';',encoding="utf-8")
    
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")