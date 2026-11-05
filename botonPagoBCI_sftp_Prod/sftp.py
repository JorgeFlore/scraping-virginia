import paramiko
import os
from os import path, getcwd


# Datos de conexión al servidor FTP
directorio = path.join(getcwd(), "descargados")


def enviar_archivos():
    
    server = "192.168.250.11"      
    port = 22                 
    username = "rendicionsftpprod"  
    private_key_path = "llaveprod"  
    #archivo_local = "archivo_local.txt"  
    archivo_remoto = "/bbci/carga/" 
    
    try:
   
        contenido = os.listdir(directorio)
        private_key = paramiko.Ed25519Key(filename=private_key_path)


        transport = paramiko.Transport((server, port))
        transport.connect(username=username, pkey=private_key)


        sftp = paramiko.SFTPClient.from_transport(transport)

        for archivo_local in contenido:
            
            destino=archivo_remoto+archivo_local
            sftp.put(path.join(getcwd(), "descargados\\"+archivo_local), destino)
            
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")