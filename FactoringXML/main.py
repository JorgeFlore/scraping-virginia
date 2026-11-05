import diashabiles
import FactoringXml

import sys
print(f"Ejecutando script: {sys.argv[0]}")

#driver = webdriver.Firefox()
run_today = diashabiles.es_habil()

def main():
   
    if not run_today:
        print("no es dia habil")
        exit(0)
    else:
        FactoringXml.descargar_xml()

    
if __name__ == "__main__":
    main()