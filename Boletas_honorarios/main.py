from boletas_de_honorarios import boletas3
from utils import diashabiles
import logging
#driver = webdriver.Firefox()
#run_today = diashabiles.es_habil()


def main():

    logging.basicConfig(
        filename = "C:\\Scraping\\Boletas_honorarios\\Log.log",
        level=logging.INFO,
        encoding="utf-8",
        datefmt="%d-%m-%Y %H:%M:%S",
        format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s",
        filemode="w"
    )


    # boletas.descargar_boletas_de_honorarios()
    boletas3.descargar_boletas_de_honorarios()
    
if __name__ == "__main__":
    main()