import os
from datetime import datetime
import utils.diashabiles as dias_habiles
import ITAU.cartolas as cartolas
from utils.logging_utils import registrar_log

def main():
    """Ejecuta la descarga de información solo en días hábiles."""
    fecha_hoy = datetime.now().strftime("%d-%m-%Y")
    registrar_log(f"🕐 Inicio del proceso BCI - {fecha_hoy}")

    try:
        # Verificar si es día hábil
        if not dias_habiles.es_habil():
            registrar_log("🚫 No es día hábil. Proceso detenido.")
            print("No es día hábil. El proceso no se ejecutará.")
            return

        # Si es día hábil, ejecutar scraping
        registrar_log("✅ Día hábil detectado. Iniciando descarga de información...")
        cartolas.descargar_informacion()
        registrar_log("🏁 Descarga completada correctamente.")

    except Exception as e:
        registrar_log(f"💥 Error crítico en main.py: {e}")
        print(f"Error durante la ejecución: {e}")

    finally:
        registrar_log("🧹 Proceso finalizado.\n")

if __name__ == "__main__":
    main()
