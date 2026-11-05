import diashabiles
import index
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
        sleep(5)
        index.procesar_excel_y_renombrar()
       # mover_archivos.mover_archivos()
    
if __name__ == "__main__":
    main()