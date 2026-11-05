import os
import time
from time import sleep
from dotenv import load_dotenv
from pathlib import Path
from utils.opciones_edge import opciones_edge
from utils.login import iniciar_sesion
from utils.rutas import obtener_ruta_descarga
from descarga_concesiones import concesiones
from descarga_exticiones import extinciones
from utils.correo import enviar_correo_fin_empresa

# Carga variables de entorno
dotenv_path = Path('utils/.env')
load_dotenv(dotenv_path)

# Destinatarios fijos
destinatarios = [ 
   "manuel.apeleo@aguasnuevas.cl",
    "daniel.gutierrez@aguasnuevas.cl"
    
    
]
cc_destinatarios = [
    "jorge.flores@aguasnuevas.cl",
    "manuel.rodriguez@aguasnuevas.cl"     
]

# Inicio medición tiempo total
inicio = time.time()

empresas = ["ADA","ATA","ARA","AXA","AMA"] 
#empresas = ["AXA"]
tipos_documento = ["Extinciones", "Concesiones"]   

for empresa in empresas:
    rutas_descarga = {}
    cantidad_archivos = {}

    for tipo in tipos_documento:
        print(f"🔄 Procesando empresa: {empresa} - tipo: {tipo}")

        ruta_descarga = obtener_ruta_descarga(empresa, tipo)
        rutas_descarga[tipo] = ruta_descarga

        driver = opciones_edge(ruta_descarga)

        try:
            iniciar_sesion(driver, empresa)
            sleep(2)

            if tipo == "Extinciones":
                extinciones(driver, ruta_descarga)
            else:
                concesiones(driver, ruta_descarga)

            sleep(2)

            archivos = [f for f in os.listdir(ruta_descarga) if os.path.isfile(os.path.join(ruta_descarga, f))]
            cantidad_archivos[tipo] = len(archivos)

        except Exception as e:
            print(f"❌ Error en {empresa} - {tipo}: {e}")

        finally:
            driver.quit()
            print(f"✅ Finalizado proceso para {empresa} - {tipo}\n")

    enviar_correo_fin_empresa(
        empresa,
        destinatarios,
        rutas_descarga,
        cantidad_archivos,
        cc=cc_destinatarios
    )

fin = time.time()
duracion = fin - inicio
minutos = int(duracion // 60)
segundos = int(duracion % 60)
print(f"⏱ Tiempo total de ejecución: {minutos} minutos y {segundos} segundos")
print("🎉 Proceso completado.")
