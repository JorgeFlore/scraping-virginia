"""
Configuración central del bot Botón de Pago Banco de Chile (SFTP Producción).
Todas las rutas, credenciales y destinatarios se cambian aquí, no en el código.
"""
from pathlib import Path

# Carpeta donde vive este script (en producción: C:\Scraping\Boton de pago banco de Chile_sftp_Prod)
BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
DIR_ARCHIVOS = Path(r"C:\Rendicion\bchile")
DIR_ENVIADOS = DIR_ARCHIVOS / "enviados"
DIR_LOGS = BASE_DIR / "logs"
RUTA_BANNER = BASE_DIR / "BannerAguasNuevas.jpg"

# Archivos que NO se mueven a "enviados" (se mantienen en la carpeta de origen)
EXCLUIR_DE_MOVER = ("carga_rend",)

# Solo se adjuntan al correo los archivos subidos cuyo nombre contenga este texto
FILTRO_ADJUNTOS = "bchile"

# ---------------------------------------------------------------------------
# SFTP
# ---------------------------------------------------------------------------
SFTP_HOST = "192.168.250.11"
SFTP_PORT = 22
SFTP_USUARIO = "rendicionsftpprod"
SFTP_LLAVE = BASE_DIR / "llaveprod"          # llave Ed25519
SFTP_DIR_REMOTO = "/bchile/carga/"
SFTP_TIMEOUT = 30                            # segundos
SFTP_REINTENTOS = 3
SFTP_ESPERA_REINTENTO = 10                   # segundos entre reintentos

# Huella del servidor SFTP (formato "SHA256:xxxx").
# Mientras sea None no se valida; cada ejecución deja la huella real en el log.
# Copie ese valor aquí para protegerse de conectarse a un servidor suplantado.
SFTP_HUELLA_SERVIDOR = None

# ---------------------------------------------------------------------------
# API de feriados
# ---------------------------------------------------------------------------
FERIADOS_URL = "https://kansas.aguasnuevas.cl:8181/WebAPIIntegraciones/SOA/feriados?{anio}&{mes}&{dia}"
FERIADOS_VERIFICAR_SSL = False   # certificado interno; poner True si se instala un certificado válido
FERIADOS_TIMEOUT = 15
FERIADOS_REINTENTOS = 3

# ---------------------------------------------------------------------------
# Empresas esperadas (código en el nombre del archivo -> nombre)
# ---------------------------------------------------------------------------
EMPRESAS = {
    "ADA": "Aguas del Altiplano",
    "ARA": "Aguas Araucanía",
    "AMA": "Aguas Magallanes",
    "ATA": "Nueva Atacama",
    "AXA": "Aguas Decima",
}

# ---------------------------------------------------------------------------
# Correo (Outlook)
# ---------------------------------------------------------------------------
CORREO_PARA = [
    "karol.alvarado@aguasnuevas.cl",
    "griselda.aburto@aguasnuevas.cl",
    "diego.morales@aguasnuevas.cl",
]
CORREO_CC = [
    "manuel.rodriguez@aguasnuevas.cl",
    "fabian.cabrera@aguasnuevas.cl",
    "jorge.flores@aguasnuevas.cl",
    "eduardo.gajardo@aguasnuevas.cl",
    "luis.gonzalez@aguasnuevas.cl",
]
CORREO_ASUNTO = "[BOT]{estado} Alerta envío Archivo Botón de pago Banco de Chile (SFTP PRODUCCION) - {fecha}"
