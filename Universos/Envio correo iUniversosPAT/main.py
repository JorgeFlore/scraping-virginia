import utils.diashabiles as dias_habiles
import PAT.cartolas as cartolas

#driver = webdriver.Firefox()
run_today = dias_habiles.es_habil()




def main():

    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        cartolas.descargar_informacion()

    
if __name__ == "__main__":
    main()