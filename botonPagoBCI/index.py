import win32com.client
import os
from datetime import datetime, date # Importa date también para diashabiles
from time import sleep
import diashabiles
import logging
import logging
import os# Ensure these are imported if used
 # Importar el módulo logging

# --- Start of Logging Configuration ---
log_dir = 'C:/BotonBCI/logs/'
log_file = os.path.join(log_dir, 'descarga_outlook.log')

# Create the log directory if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True) # exist_ok=True prevents an error if the directory already exists
    print(f"Created log directory: {log_dir}") # For initial debugging, you can remove this later

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Suponemos que correo, mover_archivos, diashabiles, ftp son módulos propios
# y que 'diashabiles.previo()' devuelve un objeto datetime.date o datetime.datetime

def descarga():
    logging.info("--- Iniciando proceso de descarga de adjuntos de Outlook ---")
    
    output_dir = "C:/BotonBCI/descargados/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True) # Crea el directorio si no existe
        logging.info(f"Directorio de salida '{output_dir}' creado.")

    # Convertir diashabiles.previo() a objeto date para comparación
    ayer_dt = diashabiles.previo() 
    if isinstance(ayer_dt, datetime):
        ayer_date = ayer_dt.date()
    elif isinstance(ayer_dt, date):
        ayer_date = ayer_dt
    else:
        logging.error("La función diashabiles.previo() no retornó un objeto datetime o date válido.")
        return # Salir si no se puede determinar la fecha de ayer

    hoy_date = datetime.now().date() # Solo la fecha de hoy sin hora
    
    logging.info(f"Fecha de 'ayer' según diashabiles: {ayer_date}")
    logging.info(f"Fecha de 'hoy': {hoy_date}")

    try:
        # Intenta obtener la aplicación Outlook. Si no está abierta, puede tardar o fallar.
        # Es clave que Outlook pueda iniciarse en segundo plano si no está abierto.
        outlook_app = win32com.client.Dispatch("Outlook.Application")
        outlook_namespace = outlook_app.GetNamespace("MAPI")
        
        # Accede a la carpeta específica. Asegúrate de que esta ruta sea exacta.
        # Si 'asistentevirtualprd@grupoaguansuevas.cl' es una cuenta delegada,
        # asegúrate de que esté configurada como tal en el Outlook local.
        inbox_folder_path = "asistentevirtualprd@grupoaguansuevas.cl\\Bandeja de entrada\\Boton BCI"
        
        try:
            # Iterar a través de las carpetas para asegurarse de que se encuentra la correcta
            # Esto es más robusto que un string directo si la cuenta es delegada o el nombre exacto varía
            target_folder = None
            for folder in outlook_namespace.Folders:
                if folder.Name == "asistentevirtualprd@grupoaguansuevas.cl":
                    try:
                        target_folder = folder.Folders("Bandeja de entrada").Folders("Boton BCI")
                        break
                    except Exception as e:
                        logging.error(f"No se pudo encontrar la subcarpeta 'Bandeja de entrada' o 'Boton BCI': {e}")
                        return

            if not target_folder:
                logging.error(f"No se encontró la carpeta raíz del buzón: 'asistentevirtualprd@grupoaguansuevas.cl'.")
                return

        except Exception as e:
            logging.error(f"Error al acceder a las carpetas de Outlook: {e}")
            return

        messages = target_folder.Items
        # Ordenar los mensajes por fecha de recepción de forma descendente para procesar los más recientes primero
        messages.Sort("[ReceivedTime]", True) 
        
        processed_count = 0
        downloaded_count = 0

        # Limitar la cantidad de correos a analizar para evitar procesar miles en cada ejecución
        # O puedes usar un filtro para solo los de hoy/ayer desde Outlook directamente
        # Por ejemplo: messages = inbox.Items.Restrict("[ReceivedTime] >= '" + (datetime.now() - timedelta(days=2)).strftime('%m/%d/%Y %H:%M %p') + "'")
        
        # Iterar sobre un número limitado de mensajes recientes o hasta encontrar los relevantes
        for i, message in enumerate(messages):
            # Puedes poner un límite si no quieres procesar todos los correos en cada ejecución
            # if i >= 100: # Procesar solo los últimos 100 correos
            #     logging.info("Límite de correos procesados alcanzado (100).")
            #     break

            try:
                message_received_date = message.ReceivedTime.date() # Obtiene solo la fecha del correo
                
                # Comprobación de la fecha: ¿Es de hoy o de ayer?
                if message_received_date == hoy_date or message_received_date == ayer_date:
                    logging.info(f"Procesando correo (Asunto: '{message.Subject}', Recibido: {message_received_date})")
                    processed_count += 1

                    if message.Attachments.Count > 0:
                        logging.info(f"  Correo con {message.Attachments.Count} adjunto(s).")
                        for j in range(1, message.Attachments.Count + 1):
                            attachment_file = message.Attachments.Item(j)
                            file_path = os.path.join(output_dir, attachment_file.FileName)
                            
                            try:
                                attachment_file.SaveAsFile(file_path)
                                logging.info(f"  Adjunto '{attachment_file.FileName}' guardado en '{output_dir}'.")
                                downloaded_count += 1
                            except Exception as e_attach:
                                logging.error(f"  Error al guardar el adjunto '{attachment_file.FileName}': {e_attach}")
                    else:
                        logging.info("  No se encontraron adjuntos en este correo.")
                # Si los correos están ordenados por fecha, una vez que pasas los de ayer, puedes detenerte
                elif message_received_date < ayer_date:
                    logging.info(f"Correo anterior al rango de fechas ({message_received_date}), deteniendo búsqueda.")
                    break # Salir del bucle si ya pasamos los correos relevantes por fecha
            except Exception as e_msg:
                logging.error(f"Error al procesar el mensaje: {e_msg}. Detalles del mensaje: Asunto='{message.Subject}'")
                # Intenta continuar con el siguiente mensaje incluso si uno falla
                continue 

    except Exception as e:
        logging.error(f"Error general en la función descarga: {e}")
        # Considera qué hacer si Outlook no responde o no se puede iniciar
        # Puedes intentar cerrar la aplicación de Outlook si se abrió y causó un error
        try:
            outlook_app.Quit()
        except:
            pass # Ignora si ya estaba cerrado o no se pudo cerrar
    finally:
        logging.info(f"--- Proceso de descarga finalizado. Correos procesados: {processed_count}, Adjuntos descargados: {downloaded_count} ---")
        # Asegúrate de que la aplicación de Outlook se cierre para no dejar procesos colgando
        try:
            outlook_app.Quit()
            logging.info("Instancia de Outlook cerrada.")
        except:
            logging.warning("No se pudo cerrar la instancia de Outlook (quizás ya estaba cerrada o no se pudo obtener).")


# No olvides que necesitarás ejecutar descarga() en tu script principal
# para que se active cuando lo llame el Programador de Tareas.
# if __name__ == "__main__":
#     descarga()