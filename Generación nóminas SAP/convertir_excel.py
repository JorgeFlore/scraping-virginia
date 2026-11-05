
import pandas as pd
import os
from bs4 import BeautifulSoup

ruta=r"C:\Users\manuel.rodriguez\Desktop\Scraping\Generación nóminas SAP"
contenido = os.listdir(ruta)

def obtener_csv():
    try:

        pruebas=ruta+r"\export.htm"
        print(pruebas)
        df = pd.read_html(ruta+r"\export.htm")[0]  # El [0] selecciona la primera tabla del archivo HTML
        df = df.drop(df.columns[1], axis=1)
        excel_file = r"C:\Users\manuel.rodriguez\Desktop\Scraping\Generación nóminas SAP\archivo_convertido.xlsx"
        df.to_excel(excel_file, index=False, engine='openpyxl', header=None)
    
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")