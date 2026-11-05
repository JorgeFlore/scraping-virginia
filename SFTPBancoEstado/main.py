import diashabiles
from correo import envio_correo_outlook
from bancoestado_sftp import mover_archivos_sftp
from time import sleep
import shutil
import os
import logging
from datetime import datetime

# === CONFIGURACIÓN DE LOG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(LOG_DIR, f"bancoestado_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

# === VARIABLES ===
CARPETA_LOCAL = os.path.join(BASE_DIR, "temp_sftp")


def main():
    
    logging.info("Inicio de ejecución del script principal.")

   
    # --- Mover archivos ---
    subidos_ok, fallidos = mover_archivos_sftp()

    # --- Enviar correo ---
    try:
        envio_correo_outlook(subidos_ok, fallidos, CARPETA_LOCAL=CARPETA_LOCAL)
        logging.info("Correo enviado correctamente.")
    except Exception as e:
        logging.error(f"Error al enviar correo: {e}")

    # --- Limpiar carpeta temporal ---
    try:
        if os.path.exists(CARPETA_LOCAL):
            shutil.rmtree(CARPETA_LOCAL)
        logging.info("🧹 Carpeta temporal eliminada.")
    except Exception as e:
        logging.error(f"⚠️ Error al borrar la carpeta temporal: {e}")
        sleep(5)

    logging.info("Ejecución finalizada.\n")


if __name__ == "__main__":
    main()
