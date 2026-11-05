"""
Bot Botón de Pago Banco de Chile - SFTP Producción.

Flujo:
  1. Verifica si hoy es día hábil (si la API de feriados no responde, se ejecuta igual
     en días de semana y se avisa en el correo).
  2. Sube al SFTP los archivos pendientes y verifica cada uno.
  3. Envía el correo con el estado real por empresa (o un correo de ERROR).
  4. Mueve a "enviados" solo los archivos que se subieron bien.

Códigos de salida: 0 = OK / no hábil, 1 = incompleto, 2 = error.
"""
import logging
import sys
from datetime import date, datetime, timedelta

import config
import diashabiles
import index
import mover_archivos
import sftp

log = logging.getLogger("bot_bchile")


def configurar_logging() -> None:
    config.DIR_LOGS.mkdir(parents=True, exist_ok=True)
    archivo = config.DIR_LOGS / f"bot_{datetime.now():%Y%m%d}.log"
    consola = logging.StreamHandler(sys.stdout)
    consola.setLevel(logging.WARNING)  # a log.txt solo llegan avisos y errores
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=[logging.FileHandler(archivo, encoding="utf-8"), consola],
    )
    logging.getLogger("paramiko").setLevel(logging.WARNING)


def fecha_de_proceso(hoy: date) -> date:
    try:
        return diashabiles.previo(hoy)
    except diashabiles.ErrorFeriados:
        return hoy - timedelta(days=1)


def main() -> int:
    configurar_logging()
    hoy = date.today()
    avisos = []
    pendientes = []
    fecha_proceso = hoy - timedelta(days=1)
    log.info("===== Inicio ejecución =====")

    try:
        # 1) Día hábil
        try:
            habil = diashabiles.es_habil(hoy)
        except diashabiles.ErrorFeriados as e:
            habil = hoy.weekday() <= 4
            log.warning("%s. Se asume día hábil=%s por ser día de semana.", e, habil)
            if habil:
                avisos.append("No se pudo consultar la API de feriados; se ejecutó igual por ser día de semana.")

        if not habil:
            log.info("No es día hábil. Fin.")
            return 0

        fecha_proceso = fecha_de_proceso(hoy)

        # 2) SFTP
        pendientes = sftp.archivos_pendientes(hoy)
        log.info("Archivos pendientes (%s): %s", len(pendientes), pendientes)
        resultados = sftp.enviar_archivos(pendientes)
        subidos = [r.nombre for r in resultados if r.ok]

        # 3) Correo (si falla, igual se mueven los archivos ya subidos para no reenviarlos)
        todo_ok = False
        try:
            todo_ok = index.envio_correo(resultados, fecha_proceso, avisos)
        except Exception:
            log.exception("No se pudo enviar el correo de resumen")

        # 4) Mover solo lo subido
        mover_archivos.mover_archivos(subidos)

        log.info("===== Fin ejecución: %s =====", "OK" if todo_ok else "INCOMPLETO")
        return 0 if todo_ok else 1

    except Exception as e:
        log.exception("Error en la ejecución")
        try:
            index.envio_correo_error(str(e), fecha_proceso, pendientes, avisos)
        except Exception:
            log.exception("Tampoco se pudo enviar el correo de error")
        return 2


if __name__ == "__main__":
    sys.exit(main())
