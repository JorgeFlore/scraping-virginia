import os
import win32com.client as win32
from datetime import datetime
from utils import credenciales
from nuevoArchivo import obtener_xml_mas_reciente

# Obtenemos la lista de correos de tu archivo de credenciales
correos = credenciales.listar_correos()

def correo(mensaje, empresa, ruta_imagen=None, buscar_xml=True):
    """
    Función principal que orquesta el envío.
    Busca el XML automáticamente y llama a la función de envío por Outlook.
    """
    # 1. Buscamos el XML más reciente
    # ruta_xml = obtener_xml_mas_reciente()
    ruta_xml = None

    if buscar_xml:
        ruta_xml = obtener_xml_mas_reciente()
    
    # 2. Iteramos por tus destinatarios (según tu lógica original)
    for i in correos:
        email = i[0]
        print(f"Preparando envío a: {email}")
        
        # Llamamos a la función adaptada de Outlook
        notificar(email, empresa, mensaje, ruta_xml, ruta_imagen)

def notificar(email, empresa, mensaje, ruta_xml=None, ruta_imagen=None):
    """
    Envía correo usando la aplicación local de Outlook (win32com).
    Adaptado del código del supervisor para usar datos del proyecto XML.
    """
    try:
        # Iniciamos la instancia de Outlook
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0) # 0 = olMailItem
        mail.BodyFormat = 2          # 2 = olFormatHTML

        # --- Variables de Tiempo ---
        ahora = datetime.now()
        fecha = ahora.strftime("%d-%m-%Y")
        hora = ahora.strftime("%H:%M:%S")

        # mail.SentOnBehalfOfName = "RPA@aguasnuevas.cl"

        # --- Asunto ---
        asunto = f"[{empresa}] Notificación de Proceso Factoring SII XML"
        mail.Subject = asunto

        # --- Banner corporativo ---
        banner_path = r"C:\Scraping\FactoringXML2.0\BannerAguasNuevas.jpg"
        banner_cid = "banneraguasnuevas"
        if os.path.exists(banner_path):
            attachment = mail.Attachments.Add(banner_path)
            attachment.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", banner_cid
            )

        # --- Captura de pantalla ---
        image_cid = "captura"
        captura_error = ""

        if ruta_imagen and os.path.exists(ruta_imagen):
            try:
                attachment = mail.Attachments.Add(ruta_imagen)
                attachment.PropertyAccessor.SetProperty(
                    "http://schemas.microsoft.com/mapi/proptag/0x3712001F", image_cid
                )
                
                captura_error = f"""
                <br>
                <p style="color:#cc0000; font-weight:bold;">Evidencia del error:</p>
                <img src="cid:{image_cid}" style="max-width:100%; border:1px solid #ccc;">
                <br>
                """
            except Exception as e:
                print(f"No se pudo adjuntar la captura: {e}")

        # --- Nombre del archivo para mostrar en el HTML ---
        nombre_archivo = os.path.basename(ruta_xml) if ruta_xml else "No generado"

        # --- Cuerpo HTML (Estilo Supervisor) ---
        body = f"""
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
            <img src="cid:{banner_cid}" width="600" style="border-radius:8px;"><br><br>
            
            <h2>🔔 Notificación de Proceso Factoring SII (XML)</h2>
            
            <p>Se ha ejecutado exitosamente el proceso Factoring SII (XML).</p>
            
            <p class="section-title">Información del proceso:</p>
            <p>· <span class="highlight">Fecha ejecución:</span> {fecha}</p>
            <p>· <span class="highlight">Hora término:</span> {hora}</p>
            
            <p class="section-title">Operación:</p>
            <p>· <span class="highlight">Sociedad:</span> {empresa}</p>
            <p>· <span class="highlight">Detalle:</span> {mensaje}</p>
            <p>· <span class="highlight">Archivo generado:</span> {nombre_archivo}</p>
            
            {captura_error}
            
            <div class="footer">
                <p>Este mensaje es exclusivo para personal autorizado de Aguas Nuevas.</p>
                <p><b>Asistente Virtual - Aguas Nuevas</b></p>
            </div>
        </div></body></html>
        """

        mail.HTMLBody = body

        # --- Adjuntar XML ---
        # ESTA ES LA PARTE IMPORTANTE: win32com hace el trabajo difícil por ti.
        if ruta_xml and os.path.exists(ruta_xml):
            mail.Attachments.Add(ruta_xml)
            print(f"   -> Archivo adjuntado: {nombre_archivo}")

        # --- Destinatarios ---
        mail.To = email
        # mail.CC = "jefe@aguasnuevas.cl" # Descomentar si necesitas copia

        # --- Envío ---
        mail.Send()
        print(f"📧 Correo enviado correctamente a {email}")

    except Exception as e:
        print(f"❌ Error al enviar correo Outlook: {e}")