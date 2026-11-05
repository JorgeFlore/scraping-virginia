import win32com.client
import os
from datetime import datetime
from time import sleep
import correo
import mover_archivos
import diashabiles
from os import makedirs, path, getcwd

ruta_archivos = path.join(getcwd(), "descargados")

def descarga():
    ayer = diashabiles.previo()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders("asistentevirtualprd@grupoaguansuevas.cl").Folders("Bandeja de entrada").Folders("Boton BCI")
    fecha_actual = datetime.now()
    fecha_actual = str(fecha_actual.strftime("%Y-%m-%d"))
    ayer = str(ayer.strftime("%Y-%m-%d"))
    print("Ayer: ",ayer)
    # Cambia "Buzón de correo" por el nombre de tu buzón si es diferente

    # Selecciona la cantidad de correos a analizar
    messages = inbox.Items
    for message in messages:
        received_time = message.ReceivedTime
        received_time = message.ReceivedTime  # Obtiene la fecha y hora de recepción
        received_time = received_time.strftime("%Y-%m-%d")  # Formatea la fecha
        if message.Attachments.Count > 0:
            attachment = message.Attachments
            if fecha_actual==str(received_time):
                for i in range(1, attachment.Count + 1):
                    attachment_file = attachment.Item(i)
                    output_dir = ruta_archivos  
                    attachment_file.SaveAsFile(os.path.join(output_dir, attachment_file.FileName))
              
descarga()       
         
