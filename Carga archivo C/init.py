from time import sleep
from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def  Iniciar_sesión(driver,empresa):
       
    URL = "https://subsidios.ministeriodesarrollosocial.gob.cl/fps/"
    driver.get(URL)
     # Obtener credenciales para la empresa
    usuario = os.getenv(f"USUARIO_{empresa}")  # USUARIO_ADA, USUARIO_ATA, etc.
    contrasena = os.getenv(f"CONTRASENA_{empresa}")  # CONTRASENA_ADA, etc.
    try:
        campo_usuario = driver.find_element(By.ID, "usuario")  # Ajusta el ID correcto
        campo_contrasena = driver.find_element(By.ID, "clave")  # Ajusta el ID correcto
        campo_usuario.send_keys(usuario)
        campo_contrasena.send_keys(contrasena)
        campo_contrasena.send_keys(Keys.RETURN)
        sleep(3)
        driver.find_element(By.XPATH, '/html/body/div/button/span[1]').click()
        sleep(5)  # Esperar la respuesta del sistema
        print(f"✅ Ingreso exitoso en {empresa}")
        sleep(5)
    except Exception as e:
        print(f"❌ Error al ingresar en {empresa}: {e}")