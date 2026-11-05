import diashabiles
from correo import envio_correo_generico_lista
from unired_sftp import mover_archivos_sftp
from time import sleep
import shutil
import os

CARPETA_LOCAL = './temp_sftp/'
PROCESO_NOMBRE = "SFTP UNIRED"
DESTINATARIOS_TO = 'karol.alvarado@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl;diego.morales@aguasnuevas.cl'
DESTINATARIOS_CC = 'jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl'

def main():
    # Ejecutar transferencia de archivos
    subidos_ok, fallidos = mover_archivos_sftp()

    # Filtrar solo archivos que existen para el correo
    subidos_ok_existentes = []
    for archivo in subidos_ok:
        ruta = os.path.abspath(os.path.join(CARPETA_LOCAL, archivo))
        if os.path.exists(ruta):
            subidos_ok_existentes.append(archivo)
        else:
            print(f"⚠️ Archivo no encontrado para adjuntar: {ruta}")

    # Enviar correo con resumen
    envio_correo_generico_lista(
    subidos_ok_existentes, 
    fallidos, 
    CARPETA_LOCAL=CARPETA_LOCAL,
    proceso_nombre=PROCESO_NOMBRE,        # <--- ARGUMENTO FALTANTE 1
    destinatarios_to=DESTINATARIOS_TO,    # <--- ARGUMENTO FALTANTE 2
    destinatarios_cc=DESTINATARIOS_CC     # <--- ARGUMENTO FALTANTE 3
    )

    # Limpiar carpeta temporal
    try:
        if os.path.exists(CARPETA_LOCAL):
            shutil.rmtree(CARPETA_LOCAL)
        print("🧹 Carpeta temporal eliminada.")
    except Exception as e:
        print(f"⚠️ Error al borrar la carpeta temporal: {e}")
        sleep(5)

if __name__ == "__main__":
    main()
