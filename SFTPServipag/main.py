"""Bot SFTP Servipag Caja y Portal: la configuración está en recaudador.json y la lógica en comun/sftp_recaudador.py."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BASE_DIR))  # para encontrar la carpeta comun/

from comun.sftp_recaudador import main_recaudador  # noqa: E402

if __name__ == "__main__":
    main_recaudador(BASE_DIR)
