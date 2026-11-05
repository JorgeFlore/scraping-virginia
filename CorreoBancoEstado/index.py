import win32com.client
import os
from datetime import datetime, timedelta
from time import sleep
import correo
import mover_archivos
import diashabiles
from glob import glob
import pandas as pd

def descarga():
    ayer = diashabiles.previo()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders("asistentevirtualprd@grupoaguansuevas.cl").Folders("Bandeja de entrada").Folders("Banco Estado")
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    ayer = ayer.strftime("%Y-%m-%d")
    print("Ayer: ", ayer)

    messages = inbox.Items
    for message in messages:
        received_time = message.ReceivedTime.strftime("%Y-%m-%d")
        if message.Attachments.Count > 0 and fecha_actual == received_time:
            for i in range(1, message.Attachments.Count + 1):
                attachment = message.Attachments.Item(i)
                output_dir = r"C:\Scraping\CorreoBancoEstado\descargados"
                attachment.SaveAsFile(os.path.join(output_dir, attachment.FileName))


def renombrar_archivos():
    directorio = r"C:\Scraping\CorreoBancoEstado\descargados"
    mapeo = {
        "ACHANAR.DAT": "122_26062025_BESTADO_ATA.txt",
        "AGUALTIP.DAT": "122_26062025_BESTADO_ADA.txt",
        "AGUASAXA.DAT": "122_26062025_BESTADO_AXA.txt",
        "MAGAGUAS.DAT": "122_26062025_BESTADO_AMA.txt",
    }

    for archivo in glob(os.path.join(directorio, "*.DAT")):
        nombre = os.path.basename(archivo)
        if nombre in mapeo:
            nuevo_nombre = mapeo[nombre]
            ruta_nueva = os.path.join(directorio, nuevo_nombre)
            os.rename(archivo, ruta_nueva)
            print(f"{nombre} → {nuevo_nombre}")
        else:
            print(f"{nombre} no está en el mapeo. Se omite.")

    archivo_unificado = os.path.join(directorio, "122_26062025_BESTADO_ARA.txt")
    archivos_a_unir = ["AGUAS9A.DAT", "AGUAS9A2.DAT"]

    with open(archivo_unificado, "wb") as salida:
        for nombre in archivos_a_unir:
            ruta = os.path.join(directorio, nombre)
            if os.path.exists(ruta):
                with open(ruta, "rb") as f:
                    salida.write(f.read())
                os.remove(ruta)
                print(f"{nombre} agregado a {os.path.basename(archivo_unificado)}")
            else:
                print(f"{nombre} no encontrado")

    renombrar_final_por_cartola()


def renombrar_final_por_cartola():
    directorio = r"C:\Scraping\CorreoBancoEstado\descargados"
    ruta_excel = r"C:\Virginia\P14 - D2 - Conciliación Bancaria\P14 - D2 - Backup - Número Cartola.xlsx"

    fecha_ayer = (datetime.today() - timedelta(days=1)).strftime("%d-%m-%Y")
    print(f"Renombrando según Excel, fecha buscada: {fecha_ayer}")

    try:
        df = pd.read_excel(ruta_excel, dtype={'Número Cartola': str})
        df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d-%m-%Y", errors='coerce')
        fecha_dt = pd.to_datetime(fecha_ayer, format="%d-%m-%Y")
        df = df[df['Fecha'] == fecha_dt]

        if df.empty:
            print("No se encontraron filas en el Excel para la fecha:", fecha_ayer)
            return

        for _, fila in df.iterrows():
            sociedad = fila['Sociedad']
            numero_cartola = fila['Número Cartola']
            nombre_actual = f"122_{fecha_ayer.replace('-', '')}_BESTADO_{sociedad}.txt"
            nombre_nuevo = f"{numero_cartola}.txt"

            ruta_actual = os.path.join(directorio, nombre_actual)
            ruta_nueva = os.path.join(directorio, nombre_nuevo)

            if os.path.exists(ruta_actual):
                os.rename(ruta_actual, ruta_nueva)
                print(f"{nombre_actual} → {nombre_nuevo}")
            else:
                print(f"Archivo no encontrado para renombrar: {nombre_actual}")

    except Exception as e:
        print(f"Error al procesar Excel: {e}")
