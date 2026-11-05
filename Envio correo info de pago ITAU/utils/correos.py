import os
from datetime import datetime
import win32com.client as win32
from dotenv import load_dotenv

# Carga variables del .env de este proyecto
# (ajusta la ruta si tu .env está en otro lugar)
load_dotenv("utils/.env")

MAIL_TO = os.getenv("MAIL_TO", "")  # "a@b.cl;c@d.cl"
MAIL_CC = os.getenv("MAIL_CC", "")
MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX", "Información de Pagos ITAU")
MAIL_BANNER_PATH = os.getenv("MAIL_BANNER_PATH", "")  # opcional

def _listar_archivos(carpeta: str):
    if not carpeta or not os.path.isdir(carpeta):
        return []
    return [
        os.path.join(carpeta, f)
        for f in os.listdir(carpeta)
        if os.path.isfile(os.path.join(carpeta, f))
    ]

def _adjuntar(mail, ruta: str) -> bool:
    try:
        if ruta and os.path.isfile(ruta):
            mail.Attachments.Add(ruta)
            return True
    except Exception as e:
        print(f"⚠️ No se pudo adjuntar {ruta}: {e}")
    return False

def _html_tabla_archivos(archivos):
    filas = (
        "".join(
            f'<tr><td style="padding: 3px 6px; text-align:left;">{os.path.basename(a)}</td></tr>'
            for a in archivos
        )
        if archivos else '<tr><td style="padding: 3px 6px;"><i>Sin archivos adjuntos</i></td></tr>'
    )
    return f"""
    <table border="1" cellspacing="0" cellpadding="0"
           style="border-collapse:collapse; width:100%; max-width:480px; font-size:12px;">
        <thead style="background:#e6f2ff;">
            <tr><th style="padding:4px 6px; text-align:left;">Archivos adjuntos</th></tr>
        </thead>
        <tbody>{filas}</tbody>
    </table>
    """

def _incrustar_banner(mail):
    if MAIL_BANNER_PATH and os.path.isfile(MAIL_BANNER_PATH):
        try:
            adj = mail.Attachments.Add(MAIL_BANNER_PATH)
            adj.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                "banner_aguasnuevas",
            )
            return (
                '<div style="text-align:left; margin-bottom: 15px;">'
                '<img src="cid:banner_aguasnuevas" '
                'style="width:100%; max-width:600px; border-radius:6px;" />'
                '</div>'
            )
        except Exception as e:
            print(f"⚠️ No se pudo incrustar banner: {e}")
    return ""

def envio_correo(ruta_base: str, nombre_carpeta: str, empresa: str) -> bool:
    """
    Envía un correo por Outlook adjuntando TODOS los archivos en:
    ruta_base / nombre_carpeta / empresa

    Asunto: "{MAIL_SUBJECT_PREFIX} <nombre_carpeta> <empresa> - <fecha y hora>"
    Destinatarios y banner se leen desde utils/.env

    Retorna True si se envió, False si falló.
    """
    carpeta = os.path.join(ruta_base, nombre_carpeta, empresa)
    archivos = _listar_archivos(carpeta)
    print(f"📦 Carpeta a enviar: {carpeta}")
    print("   Archivos:", [os.path.basename(a) for a in archivos] or ["(ninguno)"])

    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = MAIL_TO
    if MAIL_CC:
        mail.CC = MAIL_CC

    fecha_str = datetime.now().strftime("%d-%m-%Y")
    mail.Subject = f"{MAIL_SUBJECT_PREFIX} {nombre_carpeta} {empresa} "

    # Adjuntar todos los archivos encontrados
    adj_ok = sum(_adjuntar(mail, a) for a in archivos)
    print(f"📎 Adjuntos agregados: {adj_ok}")

    banner_html = _incrustar_banner(mail)
    tabla_html = _html_tabla_archivos(archivos)

    mail.HTMLBody = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; max-width:700px;">
            {banner_html}
            <h2 style="color:#004A91; margin-top:10px;">Información de Pagos ITAU - {empresa}</h2>
            <p>Se adjuntan los archivos correspondientes a <b>{nombre_carpeta}</b>.</p>
            {tabla_html}
            <div style="margin-top:20px; font-size:12px; color:#666;">
                <p>Mensaje generado automáticamente.</p>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        mail.Send()
        print("✅ Correo enviado correctamente.")
        return True
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return False
