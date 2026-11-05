import os
import win32com.client as win32
from dotenv import load_dotenv

load_dotenv()

def enviar_correo(
    empresa,
    archivo_path,
    fecha_desde,
    fecha_hasta,
    rut_dv,
    fecha_ejecucion,
    hora_inicio,
    hora_fin,
    hay_cesiones=True
):
    """
    Envía correo HTML con información del proceso Factoring SII (PDF),
    incluyendo imagen corporativa local en el encabezado.
    """

    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.BodyFormat = 2  # HTML format

        # --- Asunto ---
        asunto = f"[{empresa}] Notificación de Proceso Factoring SII PDF"
        if not hay_cesiones:
            asunto += " (Sin Cesiones)"
        mail.Subject = asunto

        # --- Banner corporativo ---
        banner_path = r"C:\Scraping\FactoringPDF\BannerAguasNuevas.jpg"
        banner_cid = "banneraguasnuevas"
        if os.path.exists(banner_path):
            attachment = mail.Attachments.Add(banner_path)
            attachment.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", banner_cid
            )

        # --- Cuerpo HTML ---
        body_base = f"""
        <html><head><meta charset="UTF-8">
        <style>
        body {{ font-family: Calibri; font-size:14px; color:#333; }}
        .container {{ border:1px solid #ddd; border-radius:8px; padding:16px; background:#fafafa; }}
        h2 {{ color:#004a8f; }}
        .section-title {{ color:#004a8f; font-weight:bold; margin-top:10px; }}
        .highlight {{ font-weight:bold; }}
        .footer {{ margin-top:20px; font-size:12px; color:#666; }}
        </style></head><body>
        <div class="container">
        <img src="cid:{banner_cid}" width="600" style="border-radius:8px;">
        <h2>🔔 Notificación de Proceso Factoring SII (PDF)</h2>
        """

        if hay_cesiones:
            body = body_base + f"""
            <p>Se ha ejecutado exitosamente el proceso Factoring SII (PDF).</p>
            <p class="section-title">Información del proceso:</p>
            <p>· <span class="highlight">Fecha ejecución:</span> {fecha_ejecucion}</p>
            <p>· <span class="highlight">Hora inicio/término:</span> {hora_inicio} / {hora_fin}</p>
            <p class="section-title">Operación:</p>
            <p>· <span class="highlight">Rut empresa:</span> {rut_dv}</p>
            <p>· <span class="highlight">Sociedad:</span> {empresa}</p>
            <p>· <span class="highlight">Rango de fechas:</span> {fecha_desde} / {fecha_hasta}</p>
            <p>· <span class="highlight">Archivo generado:</span> {os.path.basename(archivo_path)}</p>
            """
        else:
            body = body_base + f"""
            <p>El proceso se ejecutó, pero no se encontraron cesiones.</p>
            <p class="section-title">Información del proceso:</p>
            <p>· <span class="highlight">Fecha ejecución:</span> {fecha_ejecucion}</p>
            <p>· <span class="highlight">Hora inicio/término:</span> {hora_inicio} / {hora_fin}</p>
            <p class="section-title">Resultado:</p>
            <p>· No existen registros de cesiones para <b>{empresa}</b>.</p>
            """

        body += f"""
        <div class="footer">
            <p>Este mensaje es exclusivo para personal autorizado de Aguas Nuevas.</p>
            <p><b>Asistente Virtual - Aguas Nuevas</b></p>
        </div></div></body></html>
        """

        mail.HTMLBody = body
        
        # --- Adjuntar archivo (PDF o captura) ---
        if archivo_path and os.path.exists(archivo_path):
            mail.Attachments.Add(archivo_path)


        # --- Destinatarios dinámicos ---
        destinatarios = os.getenv(f"DESTINATARIOS_{empresa}")
        destinatarios_cc = os.getenv("DESTINATARIOS_CC")

        if not destinatarios:
            raise ValueError(f"No se definieron destinatarios para la empresa {empresa} en el .env")

        mail.To = "; ".join([d.strip() for d in destinatarios.split(",") if d.strip()])
        if destinatarios_cc:
            mail.CC = "; ".join([d.strip() for d in destinatarios_cc.split(",") if d.strip()])

        # --- Envío ---
        mail.Send()
        print(f"📧 Correo enviado correctamente para {empresa}")

    except Exception as e:
        print(f"❌ Error al enviar correo para {empresa}: {e}")
