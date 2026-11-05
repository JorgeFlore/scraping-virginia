import os
import json
import paramiko
import stat
import logging
from datetime import datetime, timedelta

# ---------- ⚙️ Configuración ----------
CARPETA_LOCAL = './temp_sftp/'
HISTORIAL = "historial.json"
LOG_FILE = 'sftp_transfer.log'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(message)s'))
logging.getLogger('').addHandler(console)

CARPETAS_ORIGEN = [
    '/BPAguasAltiplano',
    '/BPNuevaAtacama',
    '/BPAguasAraucania',
    '/BPAguasDecima',
    '/BPAguasMagallanes'
    
]

SFTP_ORIGEN = {
    'host': '200.54.71.230',
    'port': 22,
    'username': 'AGUASNUEVASSFTP',
    'password': os.getenv("SFTP_BPSERVIPAG_PASSWORD"),
    'ruta_remota': '/'
}

SFTP_DESTINO = {
    'host': '192.168.250.11', 
    'port': 22,
    'username': 'rendicionsftpprod',#PROD 'rendicionsftpprod', #QA  rendicionQA
    'private_key_path': r"C:\Scraping\SFTPBPServipag\llaveprod",#PROD  r"C:\Scraping\SFTPServipag\llaveprod",   QA r"C:\Users\win10\Documents\llaveSFTPQA\id_rsa.txt"
    'ruta_remota': '/servipag/cargasbp/'
}

# ---------- 🔑 Conexiones ----------
def conectar_sftp_origen(config):
    try:
        transport = paramiko.Transport((config['host'], config['port']))
        transport.connect(username=config['username'], password=config['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)
        logging.info("✅ Conexión exitosa a SFTP ORIGEN.")
        return sftp, transport
    except Exception as e:
        logging.error(f"❌ Error al conectar a SFTP ORIGEN: {e}")
        return None, None

def conectar_sftp_destino(config):
    try:
        key = paramiko.Ed25519Key.from_private_key_file(config['private_key_path'])
        transport = paramiko.Transport((config['host'], config['port']))
        transport.connect(username=config['username'], pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        logging.info("✅ Conexión exitosa a SFTP DESTINO.")
        return sftp, transport
    except Exception as e:
        logging.error(f"❌ Error al conectar a SFTP DESTINO: {e}")
        return None, None

# ---------- 📒 Historial ----------
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

# ---------- 📂 Listar archivos ----------
def listar_archivos_recursivo(sftp, ruta):
    archivos = []
    ahora = datetime.now()
    limite = ahora - timedelta(hours=24)

    try:
        for item in sftp.listdir_attr(ruta):
            ruta_completa = os.path.join(ruta, item.filename).replace('\\', '/')
            if stat.S_ISDIR(item.st_mode):
                archivos += listar_archivos_recursivo(sftp, ruta_completa)
            else:
                if item.filename.lower().endswith('.txt'):
                    fecha_modificacion = datetime.fromtimestamp(item.st_mtime)
                    if fecha_modificacion > limite:
                        archivos.append(ruta_completa)
    except Exception as e:
        logging.error(f"❌ Error al listar {ruta}: {e}")

    return archivos

# ---------- 🚀 Proceso principal ----------
def mover_archivos_sftp():
    subidos_ok = []
    fallidos = []

    os.makedirs(CARPETA_LOCAL, exist_ok=True)
    historial = cargar_historial()
    ya_subidos = archivos_ya_subidos(historial)

    logging.info("📥 Conectando a SFTP ORIGEN...")
    sftp_origen, trans_origen = conectar_sftp_origen(SFTP_ORIGEN)
    if not sftp_origen:
        return subidos_ok, fallidos

    archivos = []
    for carpeta in CARPETAS_ORIGEN:
        logging.info(f"🔍 Buscando archivos en: {carpeta}")
        archivos += listar_archivos_recursivo(sftp_origen, carpeta)

    logging.info(f"✅ Archivos encontrados: {archivos}")

    for ruta_remota in archivos:
        nombre_archivo = os.path.basename(ruta_remota)

        if nombre_archivo in ya_subidos:
            logging.info(f"⏩ Ya se movió antes: {nombre_archivo}, lo salto.")
            continue

        ruta_local = os.path.join(CARPETA_LOCAL, nombre_archivo)
        try:
            sftp_origen.get(ruta_remota, ruta_local)
            logging.info(f"⬇️  Descargado: {nombre_archivo}")
        except Exception as e:
            logging.error(f"⚠️  Error al descargar {nombre_archivo}: {e}")
            fallidos.append(nombre_archivo)

    sftp_origen.close()
    trans_origen.close()

    logging.info("📤 Conectando a SFTP DESTINO...")
    sftp_destino, trans_destino = conectar_sftp_destino(SFTP_DESTINO)
    if not sftp_destino:
        return subidos_ok, fallidos

    for archivo in os.listdir(CARPETA_LOCAL):
        if archivo in ya_subidos:
            logging.info(f"⏩ Ya estaba en historial: {archivo}, lo salto.")
            continue

        ruta_local = os.path.join(CARPETA_LOCAL, archivo)
        ruta_remota = os.path.join(SFTP_DESTINO['ruta_remota'], archivo).replace('\\', '/')

        try:
            sftp_destino.put(ruta_local, ruta_remota)
            logging.info(f"⬆️  Subido: {archivo}")
            subidos_ok.append(archivo)
        except Exception as e:
            logging.error(f"❌ Error al subir {archivo}: {e}")
            fallidos.append(archivo)

    sftp_destino.close()
    trans_destino.close()

    # Guardar historial de la ejecución
    if subidos_ok or fallidos:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historial[timestamp] = {
            "subidos_ok": subidos_ok,
            "fallidos": fallidos
        }
        guardar_historial(historial)

    return subidos_ok, fallidos

# ---------- ▶️ Ejecución directa ----------
if __name__ == '__main__':
    ok, fail = mover_archivos_sftp()
    logging.info(f"\n🎉 Transferencias exitosas: {ok}")
    logging.info(f"❗ Transferencias fallidas: {fail}")
