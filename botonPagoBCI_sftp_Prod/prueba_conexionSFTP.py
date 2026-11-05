import paramiko

host = "192.168.250.11"  
port = 22
username = "bbciprod"
private_key_path = "llavebbciprod" 

try:
    private_key = paramiko.Ed25519Key(filename=private_key_path)
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, pkey=private_key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    print("Conexión exitosa")
    transport.close()
except Exception as e:
    print(f"Error de conexión: {e}")