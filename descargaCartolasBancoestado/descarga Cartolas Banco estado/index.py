import win32com.client
import os
from datetime import datetime
from time import sleep
import diashabiles
from openpyxl.styles import NamedStyle
import openpyxl
import os
import pandas as pd
from datetime import datetime
import diashabiles 



from datetime import datetime, timedelta

def descarga():
    try:
        # Iniciar Outlook y obtener el namespace
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        # Verificar si la cuenta y la carpeta existen
        cuenta_nombre = "jorge.flores@aguasnuevas.cl"
        carpeta_nombre = "Banco Estado"

        try:
            inbox = outlook.Folders.Item(cuenta_nombre).Folders.Item(carpeta_nombre)
            print("Carpeta encontrada:", carpeta_nombre)
        except Exception as e:
            print(f"Error al acceder a la carpeta '{carpeta_nombre}':", e)
            return

        # Obtener fecha actual
        hoy = datetime.today()
        
        # Si es lunes (0), tomar el sábado anterior como fecha de descarga
        if hoy.weekday() == 0:  # Lunes
            fecha_descarga = hoy - timedelta(days=2)  # Sábado
        else:
            fecha_descarga = hoy  # De martes a viernes, usar la fecha actual

        fecha_descarga_str = fecha_descarga.strftime("%Y-%m-%d")
        print("Fecha de descarga:", fecha_descarga_str)

        # Procesar correos en la bandeja
        messages = inbox.Items
        for message in messages:
            received_time = message.ReceivedTime.strftime("%Y-%m-%d")  # Obtener fecha de recepción

            if message.Attachments.Count > 0 and received_time == fecha_descarga_str:
                output_dir = "C:/Users/jorge.flores/Documents/RPA/Scarping/descarga Cartolas Banco estado/descargas/"
                os.makedirs(output_dir, exist_ok=True)  # Crear la carpeta si no existe

                for i in range(1, message.Attachments.Count + 1):
                    attachment_file = message.Attachments.Item(i)
                    file_path = os.path.join(output_dir, attachment_file.FileName)

                    try:
                        attachment_file.SaveAsFile(file_path)
                        print(f"Archivo guardado: {file_path}")
                    except Exception as e:
                        print(f"Error al guardar el archivo {attachment_file.FileName}:", e)

    except Exception as e:
        print("Error general en la función de descarga:", e)

              


def procesar_excel_y_renombrar():
    # Ruta del archivo Excel
    excel_path = r"C:\Users\jorge.flores\Downloads\excel\excel\Excel\P14 - D2 - Backup - Número Catola.xlsx"
    
    # Leer el archivo Excel
    df = pd.read_excel(excel_path)
    
    # Convertir columna "Fecha" a formato de fecha si no lo está
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors='coerce').dt.date
    
    # Obtener la fecha de hoy y la fecha anterior hábil
    fecha_hoy = datetime.today().date()
    fecha_ayer = diashabiles.previo().strftime("%d%m%Y")  # Formato DDMMYYYY
    
    # Filtrar filas donde la fecha en columna "Fecha" coincida con hoy
    df_filtrado = df[df["Fecha"] == fecha_hoy]
    
    if df_filtrado.empty:
        print("No hay registros en el Excel para la fecha de hoy.")
        return
    
    # Diccionario de prefijos para el nombre del archivo
    prefijos = {
        "ATA": "ACHANAR.DAT",
        "ADA": "AGUALTIP.DAT",
        "ARA": "AGUAS9A2.DAT",
        "AXA": "AGUASAXA.DAT",
        "AMA": "MAGAGUAS.DAT"
    }
    
    # Ruta donde están los archivos descargados
    #download_dir = r"C:\Virginia\P14 - D2 - Conciliación Bancaria\2025\BESTADO\TXT\prueba"
    download_dir = r"C:\Users\jorge.flores\Documents\RPA\Scarping\descarga Cartolas Banco estado\descargas"
    
    for index, row in df_filtrado.iterrows():
        codigo = str(int(row["Número Cartola"])).zfill(3)  # Convertir a entero para quitar .0 y rellenar con ceros
        prefijo = row["Sociedad"]  # Columna A

        if prefijo not in prefijos:
            print(f"Prefijo desconocido: {prefijo}, se omite el archivo.")
            continue

        nuevo_nombre = f"{codigo}_{fecha_ayer}_BESTADO_{prefijo}.txt"

        # Buscar el archivo original según el prefijo
        archivo_original = prefijos[prefijo]
        archivo_original_path = os.path.join(download_dir, archivo_original)
        nuevo_path = os.path.join(download_dir, nuevo_nombre)

        if os.path.exists(archivo_original_path):
            os.rename(archivo_original_path, nuevo_path)
            print(f"Archivo renombrado: {archivo_original} -> {nuevo_nombre}")
        else:
            print(f"Archivo no encontrado: {archivo_original}")


