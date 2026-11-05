import paramiko

SFTP_DESTINO = {
    'host': '192.168.250.11',
    'port': 22,
    'username': 'rendicionQA',
    'private_key_path': "id_rsa.txt",
    'ruta_remota': '/servipag/carga/'
}

def test_conexion_sftp_con_llave(config):
    server = "192.168.250.11"      
    port = 22                 
    username = "rendicionQA"  
    private_key_path = "id_rsa.txt"  
  
    
    try:
   
        private_key = paramiko.Ed25519Key(filename=private_key_path)


        transport = paramiko.Transport((server, port))
        transport.connect(username=username, pkey=private_key)


        sftp = paramiko.SFTPClient.from_transport(transport)
        # Probar listando archivos
        archivos = sftp.listdir(config['ruta_remota'])
        print("✅ Conexión exitosa. Archivos en el destino:")
        for archivo in archivos:
            print(" -", archivo)

        # Cerrar conexión
        sftp.close()
        transport.close()

    except Exception as e:
        print("❌ Error al conectar al SFTP destino:", e)

# Ejecutar test
if __name__ == "__main__":
    test_conexion_sftp_con_llave(SFTP_DESTINO)
