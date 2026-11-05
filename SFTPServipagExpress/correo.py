import os
import win32com.client as win32
from datetime import datetime

def envio_correo_outlook(lista_ok, lista_fail, CARPETA_LOCAL):
    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    # Asignar destinatarios
    mail.To = 'karol.alvarado@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl;diego.morales@aguasnuevas.cl;'
    mail.CC = 'jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl;'
    #mail.To = 'jorge.flores@aguasnuevas.cl'

    # Asunto
    fecha = datetime.now().strftime("%Y-%m-%d")
    mail.Subject = f'Alerta SFTP Servipag Express- {fecha}'

    # Adjuntar archivos subidos exitosamente
    for archivo in lista_ok:
        ruta = os.path.join(CARPETA_LOCAL, archivo)
        try:
            if os.path.exists(ruta):
                mail.Attachments.Add(ruta)
            else:
                print(f"⚠️ No se encontró el archivo para adjuntar: {ruta}")
        except: pass
    # Cuerpo del correo en HTML
    filas_ok = "".join([f"<tr><td>{nombre}</td></tr>" for nombre in lista_ok]) or "<tr><td><i>Sin archivos</i></td></tr>"
    filas_fail = "".join([f"<tr><td>{nombre}</td></tr>" for nombre in lista_fail]) or "<tr><td><i>Sin errores</i></td></tr>"

    mail.HTMLBody = f"""
    <div style="font-family: Arial; font-size: 12px;">
        <p>Estimado usuario,</p>
        <p>Se ha ejecutado correctamente el bot Servipag Express SFTP. A continuación se detallan los archivos procesados:</p>

        <h4>✅ Archivos subidos correctamente:</h4>
        <table border="1" cellspacing="0" cellpadding="4">
            <thead><tr><th>Nombre del archivo</th></tr></thead>
            <tbody>
                {filas_ok}
            </tbody>
        </table>

        <h4>❌ Archivos con error:</h4>
        <table border="1" cellspacing="0" cellpadding="4">
            <thead><tr><th>Nombre del archivo</th></tr></thead>
            <tbody>
                {filas_fail}
            </tbody>
        </table>

        <p>Este es un correo automático, no responder.</p>
    </div>
    """

    # Enviar el correo
    mail.Send()
    print("📧 Correo enviado correctamente.")
