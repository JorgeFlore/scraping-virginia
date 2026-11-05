import paramiko
import os
from os import path, getcwd

# Datos de conexión al servidor FTP
directorio = path.join(getcwd(), "descargados")

def enviar_archivos():
    server = "192.168.250.11"
    port = 22
    username = "rendicionQA"
    private_key_path = r"C:\Scraping\BestadoCompraAqui_sftp\id_rsa.txt"
    archivo_remoto = "/bestado/carga2/"

    try:
        contenido = os.listdir(directorio)
        
        for item in contenido:
            print("Archivos: ", item)  # Línea de depuración
        
        private_key = paramiko.Ed25519Key(filename=private_key_path)
        transport = paramiko.Transport((server, port))
        transport.connect(username=username, pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        for archivo_local in contenido:
            destino = archivo_remoto + archivo_local
            ruta_local = path.join(directorio, archivo_local)
            print("Subiendo archivo:", ruta_local)  # Línea de depuración
            sftp.put(ruta_local, destino)

        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")


