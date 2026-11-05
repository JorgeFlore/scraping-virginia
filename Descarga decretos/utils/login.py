from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def iniciar_sesion(driver, empresa):
    usuario = os.getenv(f"USUARIO_{empresa}")
    contrasena = os.getenv(f"CONTRASENA_{empresa}")

    if not usuario or not contrasena:
        raise ValueError(f"⚠️ Credenciales no encontradas para {empresa} en .env")

    print(f"🔐 Iniciando sesión para empresa: {empresa}")

    driver.get("https://subsidios.ministeriodesarrollosocial.gob.cl/fps/")
    print(usuario,"    ", contrasena)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "usuario"))
        ).send_keys(usuario)

        driver.find_element(By.ID, "clave").send_keys(contrasena )

        # Esperar que un elemento que indica sesión iniciada aparezca
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn-sigin"))
        ).click()
        print(f"✅ Sesión iniciada correctamente para {empresa}")
    except Exception as e:
        print(f"❌ Error al iniciar sesión para {empresa}: {e}")
        raise


