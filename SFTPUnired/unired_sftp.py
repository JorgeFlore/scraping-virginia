import os
import json
import paramiko
import stat
from datetime import datetime

CARPETA_LOCAL = './temp_sftp/'
HISTORIAL = "historial.json"

SFTP_ORIGEN = {
    'host': 'srvsftp.unired.cl',
    'port': 22,
    'username': 'aguasnuevas',
    'password': os.getenv("SFTP_UNIRED_PASSWORD"),
    'ruta_remota': '/home/Rendiciones/'
}

SFTP_DESTINO = {
    'host': '192.168.250.11',
    'port': 22,
    'username': 'rendicionsftpprod',
    'private_key_path': r"C:\Scraping\SFTPUnired\llaveprod",
    'ruta_remota': '/unired/pendientes/'
}

# ---------- 🔗 Conexión SFTP ----------
def conectar_sftp_origen(config):
    transport = paramiko.Transport((config['host'], config['port']))
    transport.connect(username=config['username'], password=config['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp, transport

def conectar_sftp_destino(config):
    key = paramiko.Ed25519Key.from_private_key_file(config['private_key_path'])
    transport = paramiko.Transport((config['host'], config['port']))
    transport.connect(username=config['username'], pkey=key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp, transport

# ---------- 📂 Listado recursivo ----------
def listar_archivos_recursivo(sftp, ruta):
    archivos = []
    hoy = datetime.now().date()
    print(hoy)
    for item in sftp.listdir_attr(ruta):
        ruta_completa = os.path.join(ruta, item.filename).replace('\\', '/')
        if stat.S_ISDIR(item.st_mode):
            archivos += listar_archivos_recursivo(sftp, ruta_completa)
        else:
            if item.filename.lower().endswith('.txt'):
                fecha_mod = datetime.fromtimestamp(item.st_mtime).date()
                if fecha_mod == hoy:
                    archivos.append(ruta_completa)
    return archivos

# ---------- 📒 Historial JSON ----------
def cargar_historial():
    if os.path.exists(HISTORIAL):
        with open(HISTORIAL, "r") as f:
            return json.load(f)
    return {}

def guardar_historial(historial):
    historial_ordenado = dict(sorted(historial.items()))
    with open(HISTORIAL, "w") as f:
        json.dump(historial_ordenado, f, indent=2)

def archivos_ya_subidos(historial):
    subidos = set()
    for ejecucion in historial.values():
        subidos.update(ejecucion.get("subidos_ok", []))
    return subidos

# ---------- 🚀 Proceso principal ----------
def mover_archivos_sftp():
    subidos_ok = []
    fallidos = []

    os.makedirs(CARPETA_LOCAL, exist_ok=True)
    historial = cargar_historial()
    ya_subidos = archivos_ya_subidos(historial)

    print("📥 Conectando a SFTP ORIGEN...")
    sftp_origen, trans_origen = conectar_sftp_origen(SFTP_ORIGEN)

    print(f"🔍 Buscando archivos en: {SFTP_ORIGEN['ruta_remota']}")
    archivos = listar_archivos_recursivo(sftp_origen, SFTP_ORIGEN['ruta_remota'])
    print(f"✅ Archivos encontrados: {archivos}")

    for ruta_remota in archivos:
        nombre_archivo = os.path.basename(ruta_remota)
        if nombre_archivo in ya_subidos:
            print(f"⏩ Ya se movió antes: {nombre_archivo}, lo salto.")
            continue
        ruta_local = os.path.join(CARPETA_LOCAL, nombre_archivo)
        try:
            sftp_origen.get(ruta_remota, ruta_local)
            print(f"⬇️  Descargado: {nombre_archivo}")
        except Exception as e:
            print(f"⚠️ Error al descargar {nombre_archivo}: {e}")

    sftp_origen.close()
    trans_origen.close()

    print("\n📤 Conectando a SFTP DESTINO...")
    sftp_destino, trans_destino = conectar_sftp_destino(SFTP_DESTINO)

    for archivo in os.listdir(CARPETA_LOCAL):
        if archivo in ya_subidos:
            print(f"⏩ Ya estaba en historial: {archivo}, lo salto.")
            continue
        ruta_local = os.path.join(CARPETA_LOCAL, archivo)
        ruta_remota = os.path.join(SFTP_DESTINO['ruta_remota'], archivo).replace('\\', '/')
        try:
            sftp_destino.put(ruta_local, ruta_remota)
            print(f"⬆️  Subido: {archivo}")
            subidos_ok.append(archivo)
        except Exception as e:
            print(f"❌ Error al subir {archivo}: {e}")
            fallidos.append(archivo)

    sftp_destino.close()
    trans_destino.close()

    if subidos_ok or fallidos:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historial[timestamp] = {
            "subidos_ok": subidos_ok,
            "fallidos": fallidos
        }
        guardar_historial(historial)

    return subidos_ok, fallidos
