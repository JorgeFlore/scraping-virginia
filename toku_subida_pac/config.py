# ==================================
# CARPETAS
# ==================================

LOCAL_FOLDER = r"\\columbia\\cargas_masivas\\recaudacion_pac_pat"

# ==================================
# SFTP DESTINO
# ==================================

SFTP_DESTINO = {
    "host": "192.168.250.11",
    "port": 22,
    "username": "rendicionsftpprod",
    "private_key_path": r"C:\\Scraping\\toku_subida_pac\llaveprod",
    "ruta_remota": "/toku/carga/"
}

# ==================================
# CORREO
# ==================================

EMAIL_TO = (
  "jorge.flores@aguasnuevas.cl"
)

EMAIL_CC = (
    "manuel.rodriguez@aguasnuevas.cl"

)

# ==================================
# LOGS
# ==================================

LOG_FILE = "logs/proceso.log"