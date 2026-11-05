import os
import win32com.client as win32
from datetime import datetime

# Se mantiene la ruta del banner como una constante global
BANNER_PATH = r"C:\Scraping\FactoringPDF\BannerAguasNuevas.jpg"

def envio_correo_generico_lista(
    lista_ok,
    CARPETA_LOCAL,
    proceso_nombre,
    destinatarios_to,
    destinatarios_cc,
    mensaje_descripcion="Se ha ejecutado exitosamente el proceso de transferencia SFTP."
):

    """
    Envía un correo con la plantilla de listas compactas para cualquier proceso.
    """
    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    # --- Destinatarios ---
    mail.To = destinatarios_to
    mail.CC = destinatarios_cc

    # --- Asunto ---
    fecha = datetime.now().strftime("%d-%m-%Y")
    mail.Subject = f"[{proceso_nombre}] Notificación de Proceso - {fecha}"

    # --- Adjuntar archivos subidos exitosamente (Si aplica) ---
    banner_cid = "banner_aguasnuevas"
    
    for archivo in lista_ok:
        ruta = os.path.abspath(os.path.join(CARPETA_LOCAL, archivo))
        if os.path.exists(ruta):
            mail.Attachments.Add(ruta)
        else:
            print(f"⚠️ No se encontró el archivo para adjuntar: {ruta}")

    # --- Tablas HTML ---
    fila_compacta = '<tr><td style="padding: 2px 6px; text-align: left;">{}</td></tr>'
    
    filas_ok = "".join([fila_compacta.format(nombre) for nombre in lista_ok]) or '<tr><td style="padding: 2px 6px; text-align: left;"><i>Sin archivos</i></td></tr>'
    filas_fail = "".join([fila_compacta.format(nombre) for nombre in lista_fail]) or '<tr><td style="padding: 2px 6px; text-align: left;"><i>Sin errores</i></td></tr>'

    # --- Imagen embebida ---
    banner_html = ""
    if os.path.exists(BANNER_PATH):
        adjunto_banner = mail.Attachments.Add(BANNER_PATH)
        adjunto_banner.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", banner_cid
        )
        banner_html = f"""
            <div style="text-align:left;">
                <img src="cid:{banner_cid}" style="width:100%; max-width:600px; border-radius:6px;" />
            </div>
        """

    # --- Cuerpo del correo ---
    mail.HTMLBody = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; max-width:700px;">
            {banner_html}

            <h2 style="color:#004A91; margin-top:20px;">📦 Notificación de Proceso {proceso_nombre}</h2>
            <p>{mensaje_descripcion} A continuación se detallan los resultados:</p>

            <h3 style="color:#0066cc;">✅ Archivos subidos correctamente:</h3>
            <table border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse; width:100%; max-width: 350px;">
                <thead style="background-color:#e6f2ff; font-size:13px;">
                    <tr>
                        <th style="padding: 4px 6px; text-align: left;">Nombre del archivo</th>
                    </tr>
                </thead>
                <tbody>{filas_ok}</tbody>
            </table>

            <h3 style="color:#cc0000; margin-top:20px;">❌ Archivos con error:</h3>
            <table border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse; width:100%; max-width: 350px;">
                <thead style="background-color:#ffe6e6; font-size:13px;">
                    <tr>
                        <th style="padding: 4px 6px; text-align: left;">Nombre del archivo</th>
                    </tr>
                </thead>
                <tbody>{filas_fail}</tbody>
            </table>

            <p style="margin-top:20px; font-size:12px; color:#555;">
                Este mensaje ha sido enviado con información exclusiva para personal autorizado de Aguas Nuevas.<br>
                <b>Asistente Virtual - Aguas Nuevas</b>
            </p>
        </div>
    </body>
    </html>
    """

    # --- Enviar el correo ---
    mail.Send()
    print(f"📧 Correo de notificación ({proceso_nombre}) enviado correctamente.")