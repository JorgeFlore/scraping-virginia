import diashabiles
from index import descarga
from ftp import enviar_archivos
from correo import envio_correo
from mover_archivos import mover_archivos
from time import sleep
from ajustenombre import renombrar_archivos

#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()




def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        descarga()
        renombrar_archivos()
        sleep(10)
        enviar_archivos()
        envio_correo()
        sleep(15)
        mover_archivos()
    
if __name__ == "__main__":
    main()