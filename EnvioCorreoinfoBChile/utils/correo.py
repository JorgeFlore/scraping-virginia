import os
import win32com.client as win32
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("utils/.env")

MAIL_TO = os.getenv("MAIL_TO", "")
MAIL_CC = os.getenv("MAIL_CC", "")
MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX", "Informacion de Pago Banco Chile  AXA")
BANNER_PATH = os.getenv("MAIL_BANNER_PATH", "")
CARPETA_BASE = os.getenv("CARPETA_BASE", "")
CARPETA_LOGS = os.getenv("CARPETA_LOGS", "")


def enviar_correo_con_carpeta(carpeta_envio):
    """Envía un correo con todos los archivos en la carpeta del día."""
    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    fecha = datetime.now().strftime("%d-%m-%Y")

    mail.To = MAIL_TO
    mail.CC = MAIL_CC
    mail.Subject = f"{MAIL_SUBJECT_PREFIX} - {fecha}"

    # Adjuntar todos los archivos de la carpeta
    archivos = [
        os.path.join(carpeta_envio, f)
        for f in os.listdir(carpeta_envio)
        if os.path.isfile(os.path.join(carpeta_envio, f))
    ]
    for ruta in archivos:
        mail.Attachments.Add(ruta)

    # Banner opcional
    if BANNER_PATH and os.path.exists(BANNER_PATH):
        adj = mail.Attachments.Add(BANNER_PATH)
        adj.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
            "banner_aguasnuevas",
        )
        banner_html = (
            '<div style="text-align:left; margin-bottom: 15px;">'
            '<img src="cid:banner_aguasnuevas" '
            'style="width:100%; max-width:600px; border-radius:6px;" />'
            "</div>"
        )
    else:
        banner_html = ""

    filas = "".join(
        f'<tr><td style="padding: 3px 6px;">{os.path.basename(f)}</td></tr>'
        for f in archivos
    ) or "<tr><td><i>Sin archivos adjuntos</i></td></tr>"

    mail.HTMLBody = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 13px;">
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px;">
            {banner_html}
            <h2 style="color:#004A91;">📦 Informacion de Pago Banco de Chile AXA</h2>
            <p>Se adjuntan los archivos Descargados automáticamente el día <b>{fecha}</b>:</p>
            <table border="1" cellspacing="0" cellpadding="0"
                   style="border-collapse:collapse; width:100%; max-width:400px; font-size:12px;">
                <thead style="background-color:#e6f2ff;">
                    <tr><th style="padding: 4px 6px; text-align: left;">Archivos adjuntos</th></tr>
                </thead>
                <tbody>{filas}</tbody>
            </table>
            <p style="margin-top:20px; font-size:12px; color:#666;">Mensaje enviado automáticamente.</p>
        </div>
    </body>
    </html>
    """

    mail.Send()
    print(f"📧 Correo enviado correctamente con {len(archivos)} adjuntos.")


