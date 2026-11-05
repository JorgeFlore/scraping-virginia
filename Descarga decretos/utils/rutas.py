import os
from datetime import datetime

BASE_DIR = r"\\columbia\local\RPA\P09 - Subsidio"

def obtener_ruta_descarga(empresa: str, tipo_documento: str) -> str:
    # Obtener carpeta del mes y año actual
    carpeta_mes = datetime.now().strftime("%Y-%m")
    
    # Construir la ruta completa: BASE_DIR / mes-año / empresa / tipo_documento
    ruta = os.path.join(BASE_DIR, carpeta_mes, empresa, tipo_documento)

    # Crear la carpeta si no existe
    os.makedirs(ruta, exist_ok=True)

    print(f"📁 Ruta de descarga generada: {ruta}")
    return ruta
