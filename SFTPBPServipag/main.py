import diashabiles
from correo import envio_correo_outlook
from bpservipag_sftp import mover_archivos_sftp
from time import sleep
import shutil
import os


#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()

CARPETA_LOCAL = './temp_sftp/'

def main():

    #if not run_today:
    #    print("no es dia habil")
    #    exit(0)
    #else:
        subidos_ok, fallidos = mover_archivos_sftp()
        envio_correo_outlook(subidos_ok, fallidos, CARPETA_LOCAL=CARPETA_LOCAL)
        
        try:
            if os.path.exists(CARPETA_LOCAL):
                shutil.rmtree(CARPETA_LOCAL)
            print("🧹 Carpeta temporal eliminada.")
        except Exception as e:
            print(f"⚠️ Error al borrar la carpeta temporal: {e}")
            sleep(5) 
    
if __name__ == "__main__":
    main()