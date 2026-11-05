"""
Mueve a "enviados" solo los archivos que se subieron correctamente al SFTP.
"""
import logging
import os
import shutil
from datetime import datetime

import config

log = logging.getLogger(__name__)


def mover_archivos(nombres: list) -> None:
    os.makedirs(config.DIR_ENVIADOS, exist_ok=True)

    for nombre in nombres:
        if any(excl in nombre for excl in config.EXCLUIR_DE_MOVER):
            log.info("No se mueve (excluido): %s", nombre)
            continue

        origen = os.path.join(config.DIR_ARCHIVOS, nombre)
        destino = os.path.join(config.DIR_ENVIADOS, nombre)
        if not os.path.isfile(origen):
            continue

        if os.path.exists(destino):
            # No se sobrescribe un archivo ya enviado: se agrega fecha-hora al nombre
            base, ext = os.path.splitext(nombre)
            destino = os.path.join(config.DIR_ENVIADOS, f"{base}_{datetime.now():%Y%m%d%H%M%S}{ext}")
            log.warning("Ya existía en enviados; se guarda como %s", os.path.basename(destino))

        shutil.move(origen, destino)
        log.info("Movido a enviados: %s", nombre)
