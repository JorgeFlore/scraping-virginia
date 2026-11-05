import ftplib
import os
from glob import glob

# Datos de conexión al servidor FTP


def enviar_archivos():
    ftp_host = "192.168.250.4"  # Cambia esto por tu servidor FTP
    ftp_user = "rendicion"        # Cambia esto por tu usuario FTP
    ftp_pass = os.getenv("FTP_PASS")
    
    
    directorio = r'C:/B.Estado - Compra Aqui/descargados/'
    contenido = os.listdir(directorio)
    
    
    
    for archivo_local in contenido:
        #if os.path.isfile(os.path.join(directorio, archivo_local)) and archivo_local.endswith('.txt'):
    # Ruta del archivo local que deseas mover al servidor FTP
    #archivo_local = "test.txt"  # Cambia esto por el archivo local
        archivo_remoto = "/bestado/carga2/"+archivo_local  # Ruta en el servidor FTP
        # Conéctate al servidor FTP
        ftp = ftplib.FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)
        ruta_remota = os.path.dirname(archivo_remoto)  # Obtiene la ruta sin el nombre del archivo
        # Cambia de directorio en el servidor FTP, creando carpetas si es necesario
        for carpeta in ruta_remota.split("/"):
            try:
                ftp.cwd(carpeta)  # Intenta cambiar a la carpeta
            except ftplib.error_perm:
                ftp.mkd(carpeta)  # Si no existe, créala
                ftp.cwd(carpeta)  # Luego cambia a ella
        # Sube el archivo al servidor FTP
        with open(directorio+archivo_local, "rb") as archivo:
            ftp.storbinary(f"STOR {os.path.basename(archivo_remoto)}", archivo)
        print(f"Archivo '{archivo_local}' subido a '{archivo_remoto}' en el servidor FTP.")
        # Cierra la conexión FTP
        ftp.quit()