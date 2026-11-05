import diashabiles
import index
import sftp
import correo
import mover_archivos
from time import sleep

#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()




def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        index.descarga()
        sftp.enviar_archivos()
       # correo.envio_correo()
        sleep(15)
       # mover_archivos.mover_archivos()
    
if __name__ == "__main__":
    main()