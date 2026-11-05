import os
import win32com.client as win32
from datetime import datetime

# Define el banner path (se mantiene si necesitas un banner)
# Si este proceso NO usa banner, esta línea puede ser eliminada.
BANNER_PATH = r"C:\Scraping\FactoringPDF\BannerAguasNuevas.jpg" 

def envio_correo_outlook(lista_ok, lista_fail, CARPETA_LOCAL):
    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    # --- Asignar destinatarios ---
    mail.To = 'karol.alvarado@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl;diego.morales@aguasnuevas.cl'
    mail.CC = 'jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl'
    #mail.CC = 'jorge.flores@aguasnuevas.cl'

    # --- Asunto ---
    fecha = datetime.now().strftime("%Y-%m-%d")
    mail.Subject = f'Alerta SFTP_PROD PrestoRed - {fecha}'

    # --- Adjuntar archivos subidos exitosamente ---
    # Se mantiene la lógica try/except para adjuntos
    for archivo in lista_ok:
        ruta = os.path.join(CARPETA_LOCAL, archivo)
        try:
            if os.path.exists(ruta):
                mail.Attachments.Add(ruta)
            else:
                print(f"⚠️ No se encontró el archivo para adjuntar: {ruta}")
        except: pass
        
    # --- Tablas HTML con estilos compactos ---
    # Estilo de celda compacto (2px padding vertical) y alineación izquierda
    fila_compacta = '<tr><td style="padding: 2px 6px; text-align: left;">{}</td></tr>'
    
    filas_ok = "".join([fila_compacta.format(nombre) for nombre in lista_ok]) or '<tr><td style="padding: 2px 6px; text-align: left;"><i>Sin archivos</i></td></tr>'
    filas_fail = "".join([fila_compacta.format(nombre) for nombre in lista_fail]) or '<tr><td style="padding: 2px 6px; text-align: left;"><i>Sin errores</i></td></tr>'

    # --- Configuración del Banner (Si aplica) ---
    # Nota: Si el proceso PrestoRed no usa banner, puedes eliminar esta sección
    if os.path.exists(BANNER_PATH):
        adjunto_banner = mail.Attachments.Add(BANNER_PATH)
        adjunto_banner.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "banner_aguasnuevas"
        )
        banner_html = f"""
            <div style="text-align:left; margin-bottom: 15px;">
                <img src="cid:banner_aguasnuevas" style="width:100%; max-width:600px; border-radius:6px;" />
            </div>
        """
    else:
        banner_html = "" # Si no hay banner, deja el espacio vacío

    # --- Cuerpo del correo en HTML ---
    mail.HTMLBody = f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
        <div style="border:1px solid #ccc; border-radius:10px; padding:15px; max-width:700px;">
            {banner_html}
            
            <h2 style="color:#004A91; margin-top:10px;">📦 Alerta SFTP_PROD PrestoRed</h2>
            
            <p style="margin-top:20px;">Estimado usuario,</p>
            <p>Se ha ejecutado correctamente el bot de **PrestoRed**. A continuación se detallan los archivos procesados:</p>

            <h4 style="color:#0066cc;">✅ Archivos subidos correctamente:</h4>
            <table border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse; width:100%; max-width: 300px; font-size: 12px;">
                <thead style="background-color:#e6f2ff;">
                    <tr>
                        <th style="padding: 4px 6px; text-align: left;">Nombre del archivo</th>
                    </tr>
                </thead>
                <tbody>{filas_ok}</tbody>
            </table>

            <h4 style="color:#cc0000; margin-top:20px;">❌ Archivos con error:</h4>
            <table border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse; width:100%; max-width: 300px; font-size: 12px;">
                <thead style="background-color:#ffe6e6;">
                    <tr>
                        <th style="padding: 4px 6px; text-align: left;">Nombre del archivo</th>
                    </tr>
                </thead>
                <tbody>{filas_fail}</tbody>
            </table>

            <div class="footer">
                <p>Este mensaje ha sido enviado con información exclusiva para personal autorizado de Aguas Nuevas.</p>
                <p><b>Asistente Virtual - Aguas Nuevas</b></p>
            </div>
        </div>
    </body>
    </html>
    """

    # --- Enviar el correo ---
    mail.Send()
    print("📧 Correo enviado correctamente.")