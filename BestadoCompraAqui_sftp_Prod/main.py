import diashabiles
import index
import correo
import mover_archivos
from subir_sftp import enviar_archivos
from time import sleep
from ajustenombre import renombrar_archivos

#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()




def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        index.descarga(),
        renombrar_archivos(),
        enviar_archivos(),
        correo.envio_correo(),
        sleep(15)
        mover_archivos.mover_archivos()
    
if __name__ == "__main__":
    main()