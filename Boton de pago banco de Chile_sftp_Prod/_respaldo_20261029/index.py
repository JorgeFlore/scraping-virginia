import os
import win32com.client as win32
from datetime import datetime, timedelta

ruta_archivos = r"C:\Rendicion\bchile"
ruta_banner = r"C:\Scraping\Boton de pago banco de Chile_sftp_Prod\BannerAguasNuevas.jpg" 


def envio_correo():

    # =========================================================
    # 1) Diccionario de empresas esperadas
    # =========================================================
    empresas_esperadas = {
        "ADA": "Aguas del Altiplano",
        "ARA": "Aguas Araucanía ",
        "AMA": "Aguas Magallanes",
        "ATA": "Nueva Atacama",
        "AXA": "Aguas Decima"
    }

    # =========================================================
    # 2) Fecha
    # =========================================================
    fecha_actual = datetime.now() + timedelta(days=-1)
    fecha_txt = fecha_actual.strftime("%Y-%m-%d")
    fecha_compacta = fecha_actual.strftime("%Y%m%d")

    # =========================================================
    # 3) Archivos
    # =========================================================
    contenido = os.listdir(ruta_archivos)
    lista_archivos = [
        f for f in contenido
        if os.path.isfile(os.path.join(ruta_archivos, f))
    ]

    # =========================================================
    # 4) Adjuntos que contengan "bchile"
    # =========================================================
    adjuntos = []
    for f in lista_archivos:
        if "bchile" in f.lower():
            adjuntos.append(os.path.join(ruta_archivos, f))

    # =========================================================
    # 5) Empresas cargadas detectadas por nombre archivo
    # =========================================================
    empresas_cargadas = {}

    for archivo in lista_archivos:
        nombre_upper = archivo.upper()
        for cod in empresas_esperadas.keys():
            if cod in nombre_upper:
                empresas_cargadas[cod] = archivo

    cargadas = sorted(list(empresas_cargadas.keys()))
    faltantes = sorted([c for c in empresas_esperadas.keys() if c not in empresas_cargadas])

    total = len(empresas_esperadas)
    cant_cargadas = len(cargadas)

    if cant_cargadas == total:
        resumen = f"✅ Se cargaron {cant_cargadas} de {total}. (Todo OK)"
        resumen_color = "#0b7a0b"
    else:
        resumen = f"⚠️ Se cargaron {cant_cargadas} de {total}. No Cargados: {', '.join(faltantes)}"
        resumen_color = "#b45f06"

    detalle_html = ""
    for cod in empresas_esperadas:
        if cod in empresas_cargadas:
            detalle_html += f"<li>✅ <b>{cod}</b> ({empresas_esperadas[cod]}) - {empresas_cargadas[cod]}</li>"
        else:
            detalle_html += f"<li>❌ <b>{cod}</b> ({empresas_esperadas[cod]}) - <span style='color:red'>NO RECIBIDO</span></li>"

    # =========================================================
    # 6) Crear correo Outlook
    # =========================================================
    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.cc = 'manuel.rodriguez@aguasnuevas.cl;fabian.cabrera@aguasnuevas.cl;jorge.flores@aguasnuevas.cl;eduardo.gajardo@aguasnuevas.cl;luis.gonzalez@aguasnuevas.cl;'
    mail.to = 'karol.alvarado@aguasnuevas.cl;griselda.aburto@aguasnuevas.cl;diego.morales@aguasnuevas.cl;'

    mail.Subject = f'[BOT] Alerta envío Archivo Botón de pago Banco de Chile (SFTP PRODUCCION) - {fecha_compacta}'

    # =========================================================
    # 7) Banner inline (CID)
    # =========================================================
    cid_banner = "banner_bchile_001"

    if os.path.exists(ruta_banner):
        attach_banner = mail.Attachments.Add(ruta_banner)

        # PR_PROPERTY_ACCESSOR
        # 0x3712001F = PR_ATTACH_CONTENT_ID
        attach_banner.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
            cid_banner
        )

        # 0x7FFE000B = PR_ATTACHMENT_HIDDEN (True)
        attach_banner.PropertyAccessor.SetProperty(
            "http://schemas.microsoft.com/mapi/proptag/0x7FFE000B",
            True
        )

    # =========================================================
    # 8) Adjuntar archivos del proceso
    # =========================================================
    for attachment in adjuntos:
        mail.Attachments.Add(attachment)

    # =========================================================
    # 9) Cuerpo HTML con banner
    # =========================================================
    mail.HTMLBody = f"""
    <div style="font-family:Arial;font-size:12px;">

        <div style="margin-bottom:12px;">
            <img src="cid:{cid_banner}" style="width:100%; max-width:850px; border-radius:10px;" alt="Banner Banco Chile" />
        </div>

        <h3 style="margin:0;">Notificación descarga Botón de Pago Banco de Chile</h3>
        <p style="margin-top:4px;color:#555;">SFTP Producción</p>

        <p>Estimado usuario,</p>

        <p>
            Se ha ejecutado correctamente el bot de descarga Botón de Pago Banco de Chile SFTP PRODUCCIÓN.
            Se adjuntan los archivos correspondientes.
        </p>

        <div style="padding:10px;border-radius:10px;background:#f8f9fa;border:1px solid #e0e0e0;">
            <span style="color:{resumen_color}; font-weight:bold; font-size:13px;">
                {resumen}
            </span>
        </div>

        <p style="margin-top:15px;"><b>Detalle por empresa:</b></p>
        <ul>
            {detalle_html}
        </ul>

        <hr>
        <p style="color:#666;">
            Fecha proceso: {fecha_txt}<br>
            Ruta: {ruta_archivos}<br>
            Adjuntos encontrados: {len(adjuntos)}
        </p>
    </div>
    """

    mail.Send()
