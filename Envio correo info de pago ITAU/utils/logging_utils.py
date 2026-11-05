import os
import logging
from datetime import datetime

def configurar_logger():
    """Configura un logger central con carpeta separada por fecha."""
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    hora_actual = datetime.now().strftime("%H-%M-%S")

    base_path = os.path.join(os.getcwd(), "logs", fecha_hoy)
    os.makedirs(base_path, exist_ok=True)

    log_filename = os.path.join(base_path, f"scraping_log_{fecha_hoy}_{hora_actual}.txt")

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    return logging.getLogger(__name__)

# Instancia global del logger
logger = configurar_logger()

def registrar_log(mensaje: str, nivel: str = "info"):
    """Registra un mensaje en el log y en consola."""
    if nivel.lower() == "error":
        logger.error(mensaje)
    elif nivel.lower() == "warning":
        logger.warning(mensaje)
    else:
        logger.info(mensaje)
