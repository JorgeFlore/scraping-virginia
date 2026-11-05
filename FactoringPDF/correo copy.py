import os
import win32com.client as win32
from dotenv import load_dotenv

load_dotenv()

DESTINATARIOS = os.getenv("DESTINATARIOS")
DESTINATARIOS_CC = os.getenv("DESTINATARIOS_CC")

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
    Envía correo con PDF o captura según corresponda.
    Se usa HTML para soportar acentos y caracteres especiales.
    Maneja múltiples destinatarios y CC desde variables de entorno.
    """
    try:
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)

        # --- Formato HTML ---
        mail.BodyFormat = 2  # 2 = olFormatHTML

        # --- Asunto ---
        mail.Subject = f"[{empresa}] Notificación de Proceso Factoring SII PDF"

        # --- Cuerpo ---
        if hay_cesiones:
            body = f"""
<html>
<body>
<p><b>Notificación de Proceso</b><br>
Se ha ejecutado el proceso Factoring SII (PDF).</p>

<p><b>Información del proceso:</b><br>
    · Fecha de ejecución: {fecha_ejecucion}<br>
    · Hora inicio/término: {hora_inicio} / {hora_fin}</p>

<p><b>Información de la operación:</b><br>
    · Rut empresa: {rut_dv}<br>
    · Sociedad: {empresa}<br>
    · Rango de fecha consulta: {fecha_desde} / {fecha_hasta}<br>
    · Nombre del archivo de cesiones: {os.path.basename(archivo_path)}</p>

<p>Este mensaje ha sido enviado con información exclusiva para personal autorizado de Aguas Nuevas.<br>
Asistente Virtual - Aguas Nuevas</p>
</body>
</html>
"""
        else:
            body = f"""
<html>
<body>
<p><b>Notificación de Proceso</b><br>
Se ha ejecutado el proceso Factoring SII (PDF).</p>

<p><b>Información del proceso:</b><br>
    · Fecha de ejecución: {fecha_ejecucion}<br>
    · Hora inicio/término: {hora_inicio} / {hora_fin}</p>

<p><b>Información de la operación:</b><br>
    · No existen registros de Cesiones para la Empresa {empresa}.</p>

<p>Este mensaje ha sido enviado con información exclusiva para personal autorizado de Aguas Nuevas.<br>
Asistente Virtual - Aguas Nuevas</p>
</body>
</html>
"""

        mail.HTMLBody = body

        # --- Adjuntar archivo ---
        if archivo_path and os.path.exists(archivo_path):
            mail.Attachments.Add(archivo_path)

        # --- Destinatarios ---
        if DESTINATARIOS:
            destinatarios_lista = [d.strip() for d in DESTINATARIOS.split(",") if d.strip()]
            mail.To = "; ".join(destinatarios_lista)

        if DESTINATARIOS_CC:
            cc_lista = [d.strip() for d in DESTINATARIOS_CC.split(",") if d.strip()]
            mail.CC = "; ".join(cc_lista)

        # --- Enviar ---
        mail.Send()
        print(f"📧 Correo enviado para {empresa}")

    except Exception as e:
        print(f"❌ Error al enviar correo para {empresa}: {e}")
