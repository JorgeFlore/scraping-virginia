from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from extrae_datos import extraer_tabla_y_guardar_excel, CARPETA_LOCAL
from dotenv import load_dotenv
from init import Iniciar_sesión
from action import acciones, carga_archivo2
from correo import envio_correo_outlook
driver = webdriver.Chrome()

# Cargar variables de entorno
load_dotenv()


# Lista de empresas y credenciales asociadas (deben estar en el .env),
empresas = ["ADA","ATA","ARA","AXA","AMA"]

# URL de la página


for empresa in empresas:
   
    Iniciar_sesión(driver, empresa)
    sleep(3)
    acciones(driver)
    sleep(2)
    carga_archivo2(driver,empresa)
    archivo = extraer_tabla_y_guardar_excel(driver, empresa)
    sleep(2)
    if archivo:
        envio_correo_outlook(empresa)
    else:
        print("⛔ No se generó ningún archivo, correo no enviado.")
      
    print(f"🚪 Cerrando sesión en {empresa}\n")

print("🎉 Proceso completado.")
