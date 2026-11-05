import os
import json
import paramiko
import stat
import time
from datetime import datetime
from paramiko.ssh_exception import SSHException

CARPETA_LOCAL = './temp_sftp/'
HISTORIAL = "historial.json"

MAX_REINTENTOS = 3
ESPERA_REINTENTO = 10  # segundos

CARPETAS_ORIGEN = [
    '/achanar',
    '/agde',
    '/altiplano',
    '/caja_araucania',
    '/magallanes',
    '/portal_araucania'
]

SFTP_ORIGEN = {
    'host': '200.54.71.230',
    'port': 22,
    'username': 'AGUASNUEVASSFTP',
    'password': os.getenv("SFTP_SERVIPAG_PASSWORD"),
    'ruta_remota': '/'
}

SFTP_DESTINO = {
    'host': '192.168.250.11',
    'port': 22,
    'username': 'rendicionsftpprod',
    'private_key_path': r"C:\Scraping\SFTPServipag\llaveprod",
    'ruta_remota': '/servipag/carga/'
}


# ---------- 🔌 Conexiones con reintento ----------
def conectar_sftp_origen(config):
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            print(f"🔌 Conectando a SFTP ORIGEN (intento {intento})")
            transport = paramiko.Transport((config['host'], config['port']))
            transport.connect(
                username=config['username'],
                password=config['password']
            )
            sftp = paramiko.SFTPClient.from_transport(transport)
            return sftp, transport

        except (SSHException, EOFError, OSError) as e:
            print(f"⚠️ Error conexión ORIGEN: {e}")
            if intento == MAX_REINTENTOS:
                raise
            time.sleep(ESPERA_REINTENTO)


def conectar_sftp_destino(config):
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            print(f"🔌 Conectando a SFTP DESTINO (intento {intento})")
            key = paramiko.Ed25519Key.from_private_key_file(
                config['private_key_path']
            )
            transport = paramiko.Transport((config['host'], config['port']))
            transport.connect(username=config['username'], pkey=key)
            sftp = paramiko.SFTPClient.from_transport(transport)
            return sftp, transport

        except (SSHException, EOFError, OSError) as e:
            print(f"⚠️ Error conexión DESTINO: {e}")
            if intento == MAX_REINTENTOS:
                raise
            time.sleep(ESPERA_REINTENTO)


# ---------- 📂 Listado recursivo con reintento ----------
def listar_archivos_recursivo(sftp, ruta):
    archivos = []
    hoy = datetime.now().date()

    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            for item in sftp.listdir_attr(ruta):
                ruta_completa = os.path.join(
                    ruta, item.filename
                ).replace('\\', '/')

                if stat.S_ISDIR(item.st_mode):
                    archivos += listar_archivos_recursivo(sftp, ruta_completa)
                else:
                    if item.filename.lower().endswith('.txt'):
                        fecha_mod = datetime.fromtimestamp(
                            item.st_mtime
                        ).date()
                        if fecha_mod == hoy:
                            archivos.append(ruta_completa)

            return archivos

        except (SSHException, EOFError, OSError) as e:
            print(f"⚠️ Error listando {ruta}: {e}")
            if intento == MAX_REINTENTOS:
                raise
            print("🔄 Reintentando listado...")
            time.sleep(ESPERA_REINTENTO)


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


# ---------- 🚀 Proceso principal ----------
def mover_archivos_sftp():
    subidos_ok = []
    fallidos = []

    os.makedirs(CARPETA_LOCAL, exist_ok=True)
    historial = cargar_historial()
    ya_subidos = archivos_ya_subidos(historial)

    # ORIGEN
    sftp_origen, trans_origen = conectar_sftp_origen(SFTP_ORIGEN)

    archivos = []
    for carpeta in CARPETAS_ORIGEN:
        print(f"🔍 Buscando archivos en: {carpeta}")
        archivos += listar_archivos_recursivo(sftp_origen, carpeta)

    print(f"✅ Archivos encontrados: {archivos}")

    for ruta_remota in archivos:
        nombre = os.path.basename(ruta_remota)

        if nombre in ya_subidos:
            print(f"⏩ Ya procesado antes: {nombre}")
            continue

        ruta_local = os.path.join(CARPETA_LOCAL, nombre)

        for intento in range(1, MAX_REINTENTOS + 1):
            try:
                sftp_origen.get(ruta_remota, ruta_local)
                print(f"⬇️ Descargado: {nombre}")
                break
            except (SSHException, EOFError, OSError) as e:
                print(f"⚠️ Error descargando {nombre}: {e}")
                if intento == MAX_REINTENTOS:
                    fallidos.append(nombre)
                time.sleep(ESPERA_REINTENTO)

    sftp_origen.close()
    trans_origen.close()

    # DESTINO
    sftp_destino, trans_destino = conectar_sftp_destino(SFTP_DESTINO)

    for archivo in os.listdir(CARPETA_LOCAL):
        if archivo in ya_subidos:
            continue

        ruta_local = os.path.join(CARPETA_LOCAL, archivo)
        ruta_remota = os.path.join(
            SFTP_DESTINO['ruta_remota'], archivo
        ).replace('\\', '/')

        for intento in range(1, MAX_REINTENTOS + 1):
            try:
                sftp_destino.put(ruta_local, ruta_remota)
                print(f"⬆️ Subido: {archivo}")
                subidos_ok.append(archivo)
                break
            except (SSHException, EOFError, OSError) as e:
                print(f"❌ Error subiendo {archivo}: {e}")
                if intento == MAX_REINTENTOS:
                    fallidos.append(archivo)
                time.sleep(ESPERA_REINTENTO)

    sftp_destino.close()
    trans_destino.close()

    if subidos_ok or fallidos:
        historial[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = {
            "subidos_ok": subidos_ok,
            "fallidos": fallidos
        }
        guardar_historial(historial)

    return subidos_ok, fallidos