# utils/logging_utils.py
import os
from datetime import datetime

# Variable global donde se guardará la ruta del log actual
LOG_PATH = None

def configurar_log(path_log):
    """
    Inicializa la ruta global del log.
    Debe ser llamada desde main.py al iniciar el scraping.
    """
    global LOG_PATH
    LOG_PATH = path_log
    # Crear el archivo si no existe
    if not os.path.exists(LOG_PATH):
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "w", encoding="utf-8") as log:
            log.write(f"=== LOG INICIADO {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ===\n\n")

def registrar_log(mensaje: str):
    """
    Registra un mensaje en el archivo de log centralizado y en consola.
    """
    if not LOG_PATH:
        raise RuntimeError("⚠️ El log no está configurado. Llama a configurar_log(path_log) desde main.py primero.")

    timestamp = datetime.now().strftime("%H:%M:%S")
    linea = f"{timestamp} - {mensaje}"
    print(linea)

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as log:
            log.write(linea + "\n")
    except Exception as e:
        print(f"⚠️ No se pudo escribir en el log: {e}")
