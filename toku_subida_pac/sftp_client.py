import os
import logging
import paramiko

from typing import Tuple
from paramiko import SFTPClient, Transport

from config import (
    LOCAL_FOLDER,
    SFTP_DESTINO
)


def conectar_sftp_destino() -> Tuple[SFTPClient, Transport]:
    """
    Conecta al SFTP utilizando llave privada Ed25519.
    """

    key = paramiko.Ed25519Key.from_private_key_file(
        SFTP_DESTINO["private_key_path"]
    )

    transport = Transport(
        (
            SFTP_DESTINO["host"],
            SFTP_DESTINO["port"]
        )
    )

    transport.connect(
        username=SFTP_DESTINO["username"],
        pkey=key
    )

    sftp = SFTPClient.from_transport(
        transport
    )

    if sftp is None:
        raise Exception(
            "No fue posible crear el cliente SFTP"
        )

    return sftp, transport


def upload_files():
    """
    Sube todos los archivos encontrados en LOCAL_FOLDER
    y verifica que los tamaños coincidan.
    """

    archivos_ok = []
    archivos_error = []

    try:

        logging.info(
            "Conectando al servidor SFTP..."
        )

        sftp, transport = conectar_sftp_destino()

        try:

            logging.info(
                "Conexión SFTP establecida correctamente."
            )

            archivos = [
                archivo
                for archivo in os.listdir(LOCAL_FOLDER)
                if os.path.isfile(
                    os.path.join(
                        LOCAL_FOLDER,
                        archivo
                    )
                )
                and archivo.startswith("BCHILEC_")
            ]

            if not archivos:

                logging.info(
                    "No existen archivos para procesar."
                )

                return archivos_ok, archivos_error

            for archivo in archivos:

                ruta_local = os.path.join(
                    LOCAL_FOLDER,
                    archivo
                )

                ruta_remota = (
                    SFTP_DESTINO["ruta_remota"]
                    + archivo
                )

                try:

                    logging.info(
                        f"Subiendo archivo: {archivo}"
                    )

                    sftp.put(
                        ruta_local,
                        ruta_remota
                    )

                    tamaño_local = os.path.getsize(
                        ruta_local
                    )

                    atributos_remotos = sftp.stat(
                        ruta_remota
                    )

                    tamaño_remoto = (
                        atributos_remotos.st_size
                    )

                    if tamaño_local == tamaño_remoto:

                        archivos_ok.append(
                            archivo
                        )

                        logging.info(
                            f"Archivo validado correctamente: {archivo}"
                        )

                    else:

                        mensaje = (
                            f"{archivo} - Tamaño distinto "
                            f"(Local={tamaño_local}, "
                            f"Remoto={tamaño_remoto})"
                        )

                        archivos_error.append(
                            mensaje
                        )

                        logging.error(
                            mensaje
                        )

                except Exception as e:

                    mensaje = (
                        f"{archivo} - Error: {str(e)}"
                    )

                    archivos_error.append(
                        mensaje
                    )

                    logging.exception(
                        mensaje
                    )

        finally:

            try:
                sftp.close()
            except Exception:
                pass

            try:
                transport.close()
            except Exception:
                pass

            logging.info(
                "Conexión SFTP cerrada."
            )

    except Exception as e:

        mensaje = (
            f"Error de conexión SFTP: {str(e)}"
        )

        archivos_error.append(
            mensaje
        )

        logging.exception(
            mensaje
        )

    return archivos_ok, archivos_error