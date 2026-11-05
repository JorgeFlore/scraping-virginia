import diashabiles
from index import limpiar_bancoestado, limpiar_bancoChile
from correo import envio_correo
from mover_archivos import mover_archivos


#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()


def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        envio_correo()
        limpiar_bancoestado()
        limpiar_bancoChile()
        mover_archivos()
        

    
if __name__ == "__main__":
    main()