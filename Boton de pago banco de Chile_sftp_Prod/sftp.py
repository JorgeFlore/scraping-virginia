"""
Envío de archivos al SFTP de producción.
"""
import base64
import hashlib
import logging
import os
import socket
import time
from dataclasses import dataclass
from datetime import date

import paramiko

import config

log = logging.getLogger(__name__)


class ErrorSFTP(Exception):
    """No se pudo establecer la conexión con el SFTP."""


@dataclass
class Resultado:
    nombre: str
    ruta: str
    ok: bool
    detalle: str = ""


def anios_validos(hoy: date = None) -> set:
    """Año actual; en enero también el anterior (archivos del 31 de diciembre)."""
    hoy = hoy or date.today()
    anios = {str(hoy.year)}
    if hoy.month == 1:
        anios.add(str(hoy.year - 1))
    return anios


def archivos_pendientes(hoy: date = None) -> list:
    """Archivos de la carpeta de origen cuyo nombre contiene un año válido."""
    anios = anios_validos(hoy)
    pendientes = []
    for nombre in sorted(os.listdir(config.DIR_ARCHIVOS)):
        ruta = os.path.join(config.DIR_ARCHIVOS, nombre)
        if os.path.isfile(ruta) and any(a in nombre for a in anios):
            pendientes.append(nombre)
    return pendientes


def huella(llave: paramiko.PKey) -> str:
    """Huella en el mismo formato que muestra OpenSSH (SHA256:...)."""
    digest = hashlib.sha256(llave.asbytes()).digest()
    return "SHA256:" + base64.b64encode(digest).decode().rstrip("=")


def _conectar():
    llave = paramiko.Ed25519Key(filename=str(config.SFTP_LLAVE))
    sock = socket.create_connection((config.SFTP_HOST, config.SFTP_PORT), timeout=config.SFTP_TIMEOUT)
    transport = paramiko.Transport(sock)
    try:
        transport.banner_timeout = config.SFTP_TIMEOUT
        transport.start_client(timeout=config.SFTP_TIMEOUT)

        huella_servidor = huella(transport.get_remote_server_key())
        log.info("Huella del servidor SFTP: %s", huella_servidor)
        if config.SFTP_HUELLA_SERVIDOR and huella_servidor != config.SFTP_HUELLA_SERVIDOR:
            raise ErrorSFTP(
                f"La huella del servidor ({huella_servidor}) no coincide con la configurada "
                f"({config.SFTP_HUELLA_SERVIDOR}). Conexión abortada."
            )

        transport.auth_publickey(config.SFTP_USUARIO, llave)
        return transport, paramiko.SFTPClient.from_transport(transport)
    except Exception:
        transport.close()
        raise


def conectar():
    ultimo_error = None
    for intento in range(1, config.SFTP_REINTENTOS + 1):
        try:
            return _conectar()
        except ErrorSFTP:
            raise  # huella incorrecta: no se reintenta
        except Exception as e:
            ultimo_error = e
            log.warning("Conexión SFTP intento %s/%s falló: %s", intento, config.SFTP_REINTENTOS, e)
            if intento < config.SFTP_REINTENTOS:
                time.sleep(config.SFTP_ESPERA_REINTENTO)
    raise ErrorSFTP(f"No se pudo conectar a {config.SFTP_HOST}:{config.SFTP_PORT}: {ultimo_error}")


def enviar_archivos(nombres: list) -> list:
    """
    Sube cada archivo y verifica que el tamaño remoto coincida con el local.
    Devuelve una lista de Resultado (uno por archivo). Lanza ErrorSFTP si no hay conexión.
    """
    resultados = []
    if not nombres:
        return resultados

    transport, cliente = conectar()
    try:
        for nombre in nombres:
            ruta_local = os.path.join(config.DIR_ARCHIVOS, nombre)
            destino = config.SFTP_DIR_REMOTO + nombre
            try:
                tamano_local = os.path.getsize(ruta_local)
                attrs = cliente.put(ruta_local, destino, confirm=True)
                if attrs.st_size != tamano_local:
                    raise IOError(f"tamaño remoto {attrs.st_size} != local {tamano_local}")
                log.info("Subido OK: %s (%s bytes)", nombre, tamano_local)
                resultados.append(Resultado(nombre, ruta_local, True, f"{tamano_local} bytes"))
            except Exception as e:
                log.error("Error subiendo %s: %s", nombre, e)
                resultados.append(Resultado(nombre, ruta_local, False, str(e)))
    finally:
        cliente.close()
        transport.close()
    return resultados
