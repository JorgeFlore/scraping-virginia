"""
Correo de resumen (Outlook) para los bots SFTP de recaudadores.

Una sola plantilla para todos; lo que cambia por bot (destinatarios, asunto,
título y mensaje) está en la sección "correo" de cada recaudador.json.
"""
import html
import os
from datetime import datetime

BANNER_POR_DEFECTO = r"C:\Scraping\FactoringPDF\BannerAguasNuevas.jpg"
_FILA = '<tr><td style="padding: 2px 6px; text-align: left;">{}</td></tr>'


def _filas(nombres, vacio):
    if not nombres:
        return _FILA.format(f"<i>{vacio}</i>")
    return "".join(_FILA.format(html.escape(n)) for n in sorted(nombres))


def _tabla(titulo, color, fondo, filas):
    return f"""
            <h4 style="color:{color}; margin-top:20px;">{titulo}</h4>
            <table border="1" cellspacing="0" cellpadding="0"
                   style="border-collapse:collapse; width:100%; max-width: 300px; font-size: 12px;">
                <thead style="background-color:{fondo};">
                    <tr><th style="padding: 4px 6px; text-align: left;">Nombre del archivo</th></tr>
                </thead>
                <tbody>{filas}</tbody>
            </table>"""


def construir_html(cfg, lista_ok, lista_fail, banner_html=""):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; max-width:700px;">
            {banner_html}
            <h2 style="color:#004A91; margin-top:10px;">{cfg['titulo']}</h2>
            <p style="margin-top:20px;">Estimado usuario,</p>
            <p>{cfg['mensaje']}</p>
            {_tabla("✅ Archivos subidos correctamente:", "#0066cc", "#e6f2ff", _filas(lista_ok, "Sin archivos"))}
            {_tabla("❌ Archivos con error:", "#cc0000", "#ffe6e6", _filas(lista_fail, "Sin errores"))}
            <div class="footer">
                <p>Este mensaje ha sido enviado con información exclusiva para personal autorizado de Aguas Nuevas.</p>
                <p><b>Asistente Virtual - Aguas Nuevas</b></p>
            </div>
        </div>
    </body>
    </html>
    """


def asunto(cfg, ahora=None):
    ahora = ahora or datetime.now()
    return cfg["asunto"].format(fecha=ahora.strftime(cfg.get("formato_fecha", "%Y-%m-%d")))


def enviar_resumen(cfg, lista_ok, lista_fail, carpeta_local):
    import win32com.client as win32  # solo existe en Windows

    mail = win32.Dispatch("Outlook.Application").CreateItem(0)
    mail.To = cfg["to"]
    mail.CC = cfg.get("cc", "")
    mail.Subject = asunto(cfg)

    for nombre in lista_ok:
        ruta = os.path.join(carpeta_local, nombre)
        if os.path.exists(ruta):
            mail.Attachments.Add(os.path.abspath(ruta))

    banner_html = ""
    banner = cfg.get("banner", BANNER_POR_DEFECTO)
    if banner and os.path.exists(banner):
        adjunto = mail.Attachments.Add(banner)
        adjunto.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                             "banner_aguasnuevas")
        banner_html = ('<div style="text-align:left; margin-bottom: 15px;">'
                       '<img src="cid:banner_aguasnuevas" style="width:100%; max-width:600px; border-radius:6px;" />'
                       '</div>')

    mail.HTMLBody = construir_html(cfg, lista_ok, lista_fail, banner_html)
    mail.Send()
