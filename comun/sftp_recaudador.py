"""
Motor único para los bots SFTP de recaudadores.

Cada carpeta (SFTPServipag, SFTPUnired, SFTPSantander, ...) tiene solo:
  - recaudador.json  -> qué servidor, qué carpetas, a dónde subir y a quién avisar
  - main.py          -> 4 líneas que llaman a main_recaudador()
  - historial.json   -> el mismo historial de siempre (mismo formato, se reutiliza)

Flujo (igual que los bots originales):
  1. Conecta al SFTP del recaudador (usuario + clave desde variable de entorno).
  2. Busca archivos (.txt) del día en las carpetas configuradas (recursivo).
  3. Descarga los que no están en historial.json a <carpeta>/temp_sftp.
  4. Los sube al SFTP interno con la llave privada.
  5. Registra la ejecución en historial.json, envía el correo y borra temp_sftp.

Mejoras respecto a las versiones anteriores:
  - Reintentos en conexión, listado, descarga y subida (antes solo Servipag los tenía).
  - Si una carpeta del origen falla, sigue con las demás y lo informa en el correo.
  - Si falla la conexión o falta una clave, igual se envía el correo con el error.
  - Log diario en <carpeta>/logs/ (en vez de un sftp_transfer.log que crecía sin límite).
"""
import json
import logging
import os
import shutil
import stat
import time
from datetime import datetime, timedelta

import paramiko

log = logging.getLogger("sftp_recaudador")


# ---------------------------------------------------------------- configuración
def cargar_config(base_dir):
    with open(os.path.join(base_dir, "recaudador.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    cfg.setdefault("reintentos", 3)
    cfg.setdefault("espera_reintento", 10)
    cfg.setdefault("filtro", {})
    cfg["filtro"].setdefault("extension", ".txt")
    cfg["filtro"].setdefault("modo", "hoy")  # "hoy" | "ultimas_24h"
    cfg["origen"].setdefault("port", 22)
    cfg["destino"].setdefault("port", 22)
    return cfg


def configurar_log(base_dir, slug):
    carpeta = os.path.join(base_dir, "logs")
    os.makedirs(carpeta, exist_ok=True)
    archivo = os.path.join(carpeta, f"{slug}_{datetime.now():%Y-%m-%d}.log")
    formato = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    raiz = logging.getLogger()
    raiz.setLevel(logging.INFO)
    for h in (logging.FileHandler(archivo, encoding="utf-8"), logging.StreamHandler()):
        h.setFormatter(formato)
        raiz.addHandler(h)


# ---------------------------------------------------------------- reintentos
def con_reintentos(accion, descripcion, reintentos, espera):
    for intento in range(1, reintentos + 1):
        try:
            return accion()
        except Exception as e:  # noqa: BLE001 - se registra y se reintenta
            log.warning("%s falló (intento %s/%s): %s", descripcion, intento, reintentos, e)
            if intento == reintentos:
                raise
            time.sleep(espera)


# ---------------------------------------------------------------- conexiones
def conectar_origen(cfg):
    o = cfg["origen"]
    clave = os.getenv(o["password_env"])
    if not clave:
        raise RuntimeError(f"Falta la variable de entorno {o['password_env']} (clave del SFTP origen)")

    def _conectar():
        transport = paramiko.Transport((o["host"], o["port"]))
        transport.connect(username=o["username"], password=clave)
        return paramiko.SFTPClient.from_transport(transport), transport

    log.info("Conectando a SFTP ORIGEN %s...", o["host"])
    return con_reintentos(_conectar, "Conexión ORIGEN", cfg["reintentos"], cfg["espera_reintento"])


def conectar_destino(cfg):
    d = cfg["destino"]

    def _conectar():
        key = paramiko.Ed25519Key.from_private_key_file(d["llave"])
        transport = paramiko.Transport((d["host"], d["port"]))
        transport.connect(username=d["username"], pkey=key)
        return paramiko.SFTPClient.from_transport(transport), transport

    log.info("Conectando a SFTP DESTINO %s...", d["host"])
    return con_reintentos(_conectar, "Conexión DESTINO", cfg["reintentos"], cfg["espera_reintento"])


def cerrar(sftp, transport):
    for obj in (sftp, transport):
        try:
            obj.close()
        except Exception:  # noqa: BLE001
            pass


# ---------------------------------------------------------------- búsqueda
def es_del_periodo(mtime, modo, ahora=None):
    ahora = ahora or datetime.now()
    fecha = datetime.fromtimestamp(mtime)
    if modo == "ultimas_24h":
        return fecha > ahora - timedelta(hours=24)
    return fecha.date() == ahora.date()


def listar_recursivo(sftp, ruta, filtro):
    archivos = []
    for item in sftp.listdir_attr(ruta):
        completa = os.path.join(ruta, item.filename).replace("\\", "/")
        if stat.S_ISDIR(item.st_mode):
            archivos += listar_recursivo(sftp, completa, filtro)
        elif item.filename.lower().endswith(filtro["extension"]) and es_del_periodo(item.st_mtime, filtro["modo"]):
            archivos.append(completa)
    return archivos


# ---------------------------------------------------------------- historial
def cargar_historial(ruta):
    if os.path.exists(ruta):
        try:
            with open(ruta, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:  # noqa: BLE001
            log.error("No se pudo leer el historial (%s). Se detiene para no re-subir archivos.", e)
            raise
    return {}


def guardar_historial(ruta, historial):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(historial.items())), f, indent=2, ensure_ascii=False)


def ya_subidos(historial):
    nombres = set()
    for ejecucion in historial.values():
        nombres.update(ejecucion.get("subidos_ok", []))
    return nombres


# ---------------------------------------------------------------- proceso
def mover_archivos(cfg, base_dir):
    """Devuelve (subidos_ok, fallidos). Nunca lanza excepción: los errores van a 'fallidos'."""
    temp = os.path.join(base_dir, "temp_sftp")
    ruta_historial = os.path.join(base_dir, "historial.json")
    os.makedirs(temp, exist_ok=True)
    r, espera = cfg["reintentos"], cfg["espera_reintento"]

    subidos_ok, fallidos, descargados = [], [], []
    try:
        historial = cargar_historial(ruta_historial)
    except Exception as e:  # noqa: BLE001
        return [], [f"ERROR historial.json ilegible, no se movió nada: {e}"]
    previos = ya_subidos(historial)

    # ---- ORIGEN: buscar y descargar
    try:
        sftp, transport = conectar_origen(cfg)
    except Exception as e:  # noqa: BLE001
        log.error("Error crítico con SFTP ORIGEN: %s", e)
        return [], [f"ERROR conexión origen: {e}"]

    try:
        encontrados = []
        for carpeta in cfg["origen"]["carpetas"]:
            log.info("Buscando archivos en %s", carpeta)
            try:
                encontrados += con_reintentos(lambda c=carpeta: listar_recursivo(sftp, c, cfg["filtro"]),
                                              f"Listado {carpeta}", r, espera)
            except Exception as e:  # noqa: BLE001
                log.error("No se pudo leer la carpeta %s: %s", carpeta, e)
                fallidos.append(f"ERROR carpeta {carpeta}: {e}")
        log.info("Archivos encontrados: %s", encontrados)

        for remota in encontrados:
            nombre = os.path.basename(remota)
            if nombre in previos:
                log.info("Ya se movió antes: %s, se salta.", nombre)
                continue
            if nombre in descargados:
                continue
            local = os.path.join(temp, nombre)
            try:
                con_reintentos(lambda a=remota, b=local: sftp.get(a, b), f"Descarga {nombre}", r, espera)
                descargados.append(nombre)
                log.info("Descargado: %s", nombre)
            except Exception as e:  # noqa: BLE001
                log.error("Error al descargar %s: %s", nombre, e)
                fallidos.append(nombre)
    finally:
        cerrar(sftp, transport)

    # ---- DESTINO: subir
    if descargados:
        try:
            sftp, transport = conectar_destino(cfg)
        except Exception as e:  # noqa: BLE001
            log.error("Error crítico con SFTP DESTINO: %s", e)
            fallidos += descargados
            fallidos.append(f"ERROR conexión destino: {e}")
        else:
            try:
                for nombre in descargados:
                    remota = os.path.join(cfg["destino"]["ruta_remota"], nombre).replace("\\", "/")
                    try:
                        con_reintentos(lambda a=os.path.join(temp, nombre), b=remota: sftp.put(a, b),
                                       f"Subida {nombre}", r, espera)
                        subidos_ok.append(nombre)
                        log.info("Subido: %s", nombre)
                    except Exception as e:  # noqa: BLE001
                        log.error("Error al subir %s: %s", nombre, e)
                        fallidos.append(nombre)
            finally:
                cerrar(sftp, transport)

    # ---- Historial (mismo formato que antes)
    if subidos_ok or fallidos:
        historial[datetime.now().strftime("%Y-%m-%d %H:%M:%S")] = {"subidos_ok": subidos_ok, "fallidos": fallidos}
        guardar_historial(ruta_historial, historial)

    log.info("Proceso finalizado. OK=%s  Fallidos=%s", len(subidos_ok), len(fallidos))
    return subidos_ok, fallidos


def main_recaudador(base_dir):
    """Punto de entrada que usa cada main.py."""
    from comun.correo_sftp import enviar_resumen

    cfg = cargar_config(base_dir)
    configurar_log(base_dir, cfg.get("slug", os.path.basename(base_dir).lower()))
    log.info("Inicio: %s", cfg["nombre"])

    subidos_ok, fallidos = mover_archivos(cfg, base_dir)
    temp = os.path.join(base_dir, "temp_sftp")

    try:
        enviar_resumen(cfg["correo"], subidos_ok, fallidos, temp)
        log.info("Correo enviado.")
    except Exception as e:  # noqa: BLE001
        log.error("Error al enviar correo: %s", e)

    try:
        if os.path.exists(temp):
            shutil.rmtree(temp)
        log.info("Carpeta temporal eliminada.")
    except Exception as e:  # noqa: BLE001
        log.error("Error al borrar la carpeta temporal: %s", e)

    log.info("Ejecución finalizada.")
    return subidos_ok, fallidos
