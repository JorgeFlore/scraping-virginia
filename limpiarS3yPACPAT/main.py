import diashabiles
from index import limpiar
from correo import envio_correo

#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()


def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        envio_correo()
        limpiar()
        

    
if __name__ == "__main__":
    main()