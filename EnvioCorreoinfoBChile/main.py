import os
from datetime import datetime
from utils.correo import enviar_correo_con_carpeta

# Fecha actual
fecha_hoy = datetime.now().strftime("%d-%m-%Y")

# Carpeta del día
CARPETA_BASE = os.getenv("CARPETA_BASE", r"\\columbia\cargas_masivas\informacion_de_pagos_bancos\BCHILE")
carpeta_dia = os.path.join(CARPETA_BASE, fecha_hoy)

if not os.path.exists(carpeta_dia):
    print(f"⚠️ No existe la carpeta del día: {carpeta_dia}")
else:
    print(f"📁 Enviando archivos de la carpeta: {carpeta_dia}")
    enviar_correo_con_carpeta(carpeta_dia)
