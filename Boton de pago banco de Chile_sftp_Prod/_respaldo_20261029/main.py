import diashabiles
import index
import sftp
import index
import mover_archivos
from time import sleep

#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()




def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        
        sftp.enviar_archivos()
        index.envio_correo()
        sleep(5)
        mover_archivos.mover_archivos()
        sleep(15)
      
    
if __name__ == "__main__":
    main()