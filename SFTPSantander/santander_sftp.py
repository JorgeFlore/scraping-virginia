import os
import json
import paramiko
import stat
import logging
from datetime import datetime

# === CONFIGURACIÓN BASE ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CARPETA_LOCAL = os.path.join(BASE_DIR, "temp_sftp")
os.makedirs(CARPETA_LOCAL, exist_ok=True)

# Carpeta de logs
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Archivo log diario
log_filename = os.path.join(LOG_DIR, f"prestored_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Mostrar también en consola
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# === ARCHIVO HISTORIAL JSON ===
HISTORIAL = os.path.join(BASE_DIR, "historial.json")

CARPETAS_ORIGEN = [
    '/SANTANDER/ALTIPLANO',
    '/SANTANDER/ARAUCANIA',
    '/SANTANDER/MAGALLANES'
]

SFTP_ORIGEN = {
    'host':  'ftp.eftgroup.net',
    'port': 22,
    'username': 'holding_aguas_nuevas',
    'password': os.getenv("SFTP_SANTANDER_PASSWORD"),
    'ruta_remota': '/'
}

SFTP_DESTINO = {
    'host': '192.168.250.11',
    'port': 22,
    'username': 'rendicionsftpprod',
    'private_key_path': r"C:\Scraping\SFTPPrestoRED\llaveprod",
    'ruta_remota': '/bsantander/pendientes/'
}


# ---------- 🔑 Conexiones ----------
def conectar_sftp_origen(config):
    logging.info(f"Conectando a SFTP ORIGEN {config['host']}...")
    transport = paramiko.Transport((config['host'], config['port']))
    transport.connect(username=config['username'], password=config['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    logging.info("Conexión a ORIGEN establecida correctamente.")
    return sftp, transport


def conectar_sftp_destino(config):
    logging.info(f"Conectando a SFTP DESTINO {config['host']}...")
    key = paramiko.Ed25519Key.from_private_key_file(config['private_key_path'])
    transport = paramiko.Transport((config['host'], config['port']))
    transport.connect(username=config['username'], pkey=key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    logging.info("Conexión a DESTINO establecida correctamente.")
    return sftp, transport


# ---------- 📂 Utilidades ----------
def listar_archivos_recursivo(sftp, ruta):
    archivos = []
    hoy = datetime.now().date()

    for item in sftp.listdir_attr(ruta):
        ruta_completa = os.path.join(ruta, item.filename).replace('\\', '/')

        if stat.S_ISDIR(item.st_mode):
            archivos += listar_archivos_recursivo(sftp, ruta_completa)
        else:
            if item.filename.lower().endswith('.txt'):
                fecha_modificacion = datetime.fromtimestamp(item.st_mtime).date()
                if fecha_modificacion == hoy:
                    archivos.append(ruta_completa)

    return archivos


# ---------- 📒 Manejo de historial ----------
def cargar_historial():
    if os.path.exists(HISTORIAL):
        try:
            with open(HISTORIAL, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error al leer historial: {e}")
    return {}


def guardar_historial(historial):
    try:
        historial_ordenado = dict(sorted(historial.items()))
        with open(HISTORIAL, "w", encoding="utf-8") as f:
            json.dump(historial_ordenado, f, indent=2, ensure_ascii=False)
        logging.info("Historial actualizado correctamente.")
    except Exception as e:
        logging.error(f"Error al guardar historial: {e}")


def archivos_ya_subidos(historial):
    subidos = set()
    for ejecucion in historial.values():
        subidos.update(ejecucion.get("subidos_ok", []))
    return subidos


# ---------- 🚀 Proceso principal ----------
def mover_archivos_sftp():
    subidos_ok = []
    fallidos = []

    historial = cargar_historial()
    ya_subidos = archivos_ya_subidos(historial)

    try:
        sftp_origen, trans_origen = conectar_sftp_origen(SFTP_ORIGEN)

        archivos = []
        for carpeta in CARPETAS_ORIGEN:
            logging.info(f"Buscando archivos en {carpeta}...")
            archivos += listar_archivos_recursivo(sftp_origen, carpeta)

        logging.info(f"Archivos encontrados: {archivos}")

        for ruta_remota in archivos:
            nombre_archivo = os.path.basename(ruta_remota)

            if nombre_archivo in ya_subidos:
                logging.info(f"Ya se movió antes: {nombre_archivo}, se salta.")
                continue

            ruta_local = os.path.join(CARPETA_LOCAL, nombre_archivo)
            try:
                sftp_origen.get(ruta_remota, ruta_local)
                logging.info(f"Descargado: {nombre_archivo}")
            except Exception as e:
                logging.error(f"Error al descargar {nombre_archivo}: {e}")
                fallidos.append(nombre_archivo)

        sftp_origen.close()
        trans_origen.close()
        logging.info("Conexión con ORIGEN cerrada.")

    except Exception as e:
        logging.error(f"Error crítico con SFTP ORIGEN: {e}")
        return [], []

    try:
        sftp_destino, trans_destino = conectar_sftp_destino(SFTP_DESTINO)

        for archivo in os.listdir(CARPETA_LOCAL):
            if archivo in ya_subidos:
                logging.info(f"Ya estaba en historial: {archivo}, se salta.")
                continue

            ruta_local = os.path.join(CARPETA_LOCAL, archivo)
            ruta_remota = os.path.join(SFTP_DESTINO['ruta_remota'], archivo).replace('\\', '/')

            try:
                sftp_destino.put(ruta_local, ruta_remota)
                logging.info(f"Subido: {archivo}")
                subidos_ok.append(archivo)
            except Exception as e:
                logging.error(f"Error al subir {archivo}: {e}")
                fallidos.append(archivo)

        sftp_destino.close()
        trans_destino.close()
        logging.info("Conexión con DESTINO cerrada.")

    except Exception as e:
        logging.error(f"Error crítico con SFTP DESTINO: {e}")
        return subidos_ok, fallidos

    # Guardar historial
    if subidos_ok or fallidos:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        historial[timestamp] = {
            "subidos_ok": subidos_ok,
            "fallidos": fallidos
        }
        guardar_historial(historial)

    logging.info("Proceso mover_archivos_sftp finalizado.")
    return subidos_ok, fallidos
