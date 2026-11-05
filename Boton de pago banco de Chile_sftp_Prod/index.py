"""
Envío de correos por Outlook: resumen de la ejecución y alerta de error.
El estado de cada empresa se calcula con lo que REALMENTE se subió al SFTP.
"""
import html
import logging
import os
import re
from datetime import date

import config

log = logging.getLogger(__name__)

CID_BANNER = "banner_bchile_001"


# ---------------------------------------------------------------------------
# Detección de empresa por nombre de archivo
# ---------------------------------------------------------------------------
def empresa_de_archivo(nombre: str):
    """
    Devuelve el código de empresa contenido en el nombre del archivo.
    Primero busca el código como palabra separada (ej. bchile_ADA_20261028.txt) para
    evitar falsos positivos como "ATA" dentro de "DATA"; si no encuentra ninguno,
    usa la búsqueda por subcadena del proceso original.
    """
    upper = nombre.upper()
    for cod in config.EMPRESAS:
        if re.search(rf"(?<![A-Z]){cod}(?![A-Z])", upper):
            return cod
    for cod in config.EMPRESAS:
        if cod in upper:
            return cod
    return None


# ---------------------------------------------------------------------------
# Outlook
# ---------------------------------------------------------------------------
def _enviar(asunto: str, cuerpo_html: str, adjuntos: list = ()) -> None:
    import win32com.client as win32  # import local: permite probar el resto sin Outlook

    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)
    mail.To = ";".join(config.CORREO_PARA)
    mail.CC = ";".join(config.CORREO_CC)
    mail.Subject = asunto

    if os.path.exists(config.RUTA_BANNER):
        banner = mail.Attachments.Add(str(config.RUTA_BANNER))
        banner.PropertyAccessor.SetProperty(  # PR_ATTACH_CONTENT_ID
            "http://schemas.microsoft.com/mapi/proptag/0x3712001F", CID_BANNER)
        banner.PropertyAccessor.SetProperty(  # PR_ATTACHMENT_HIDDEN
            "http://schemas.microsoft.com/mapi/proptag/0x7FFE000B", True)

    for ruta in adjuntos:
        mail.Attachments.Add(str(ruta))

    mail.HTMLBody = cuerpo_html
    mail.Send()
    log.info("Correo enviado: %s", asunto)


def _plantilla(titulo: str, contenido: str, fecha_proceso: date) -> str:
    return f"""
    <div style="font-family:Arial;font-size:12px;">
        <div style="margin-bottom:12px;">
            <img src="cid:{CID_BANNER}" style="width:100%; max-width:850px; border-radius:10px;" alt="Banner Banco Chile" />
        </div>
        <h3 style="margin:0;">{titulo}</h3>
        <p style="margin-top:4px;color:#555;">SFTP Producción</p>
        <p>Estimado usuario,</p>
        {contenido}
        <hr>
        <p style="color:#666;">
            Fecha proceso: {fecha_proceso:%Y-%m-%d}<br>
            Ruta: {html.escape(str(config.DIR_ARCHIVOS))}<br>
            Servidor: {config.SFTP_HOST}{config.SFTP_DIR_REMOTO}
        </p>
    </div>
    """


def _caja(texto: str, color: str) -> str:
    return f"""
        <div style="padding:10px;border-radius:10px;background:#f8f9fa;border:1px solid #e0e0e0;">
            <span style="color:{color}; font-weight:bold; font-size:13px;">{texto}</span>
        </div>"""


def _avisos_html(avisos) -> str:
    if not avisos:
        return ""
    items = "".join(f"<li>{html.escape(a)}</li>" for a in avisos)
    return f"<p style='margin-top:15px;'><b>Avisos:</b></p><ul style='color:#b45f06;'>{items}</ul>"


# ---------------------------------------------------------------------------
# Correo de resumen
# ---------------------------------------------------------------------------
def envio_correo(resultados: list, fecha_proceso: date, avisos: list = ()) -> bool:
    """
    resultados: lista de sftp.Resultado. Devuelve True si todo quedó OK.
    """
    subidos = [r for r in resultados if r.ok]
    fallidos = [r for r in resultados if not r.ok]

    empresas_ok = {}
    for r in subidos:
        cod = empresa_de_archivo(r.nombre)
        if cod:
            empresas_ok.setdefault(cod, []).append(r.nombre)

    faltantes = [c for c in config.EMPRESAS if c not in empresas_ok]
    total = len(config.EMPRESAS)
    todo_ok = not faltantes and not fallidos

    if todo_ok:
        resumen = f"✅ Se cargaron al SFTP {len(empresas_ok)} de {total} empresas. (Todo OK)"
        color, estado = "#0b7a0b", ""
    else:
        partes = [f"⚠️ Se cargaron al SFTP {len(empresas_ok)} de {total} empresas."]
        if faltantes:
            partes.append(f"No cargadas: {', '.join(faltantes)}.")
        if fallidos:
            partes.append(f"{len(fallidos)} archivo(s) con error de envío.")
        resumen = " ".join(partes)
        color, estado = "#b45f06", " [INCOMPLETO]"

    detalle = ""
    for cod, nombre_emp in config.EMPRESAS.items():
        if cod in empresas_ok:
            archivos = ", ".join(html.escape(a) for a in empresas_ok[cod])
            detalle += f"<li>✅ <b>{cod}</b> ({nombre_emp}) - {archivos}</li>"
        else:
            detalle += f"<li>❌ <b>{cod}</b> ({nombre_emp}) - <span style='color:red'>NO CARGADO</span></li>"

    errores = ""
    if fallidos:
        items = "".join(
            f"<li><b>{html.escape(r.nombre)}</b>: {html.escape(r.detalle)}</li>" for r in fallidos)
        errores = (f"<p style='margin-top:15px;'><b>Archivos que NO se pudieron subir "
                   f"(se mantienen en la carpeta para el próximo intento):</b></p>"
                   f"<ul style='color:red;'>{items}</ul>")

    otros = [r.nombre for r in subidos if not empresa_de_archivo(r.nombre)]
    otros_html = ""
    if otros:
        otros_html = ("<p style='margin-top:15px;'><b>Otros archivos subidos:</b> "
                      + ", ".join(html.escape(o) for o in otros) + "</p>")

    intro = ("<p>Se ejecutó el bot de envío Botón de Pago Banco de Chile SFTP PRODUCCIÓN. "
             "Se adjuntan los archivos enviados.</p>") if resultados else (
             "<p>Se ejecutó el bot de envío Botón de Pago Banco de Chile SFTP PRODUCCIÓN, "
             "pero <b>no había archivos para enviar</b> en la carpeta de origen.</p>")

    contenido = (intro + _caja(resumen, color)
                 + "<p style='margin-top:15px;'><b>Detalle por empresa:</b></p><ul>" + detalle + "</ul>"
                 + errores + otros_html + _avisos_html(avisos)
                 + f"<p style='color:#666;'>Archivos enviados: {len(subidos)} · con error: {len(fallidos)}</p>")

    adjuntos = [r.ruta for r in subidos if config.FILTRO_ADJUNTOS in r.nombre.lower()]
    asunto = config.CORREO_ASUNTO.format(estado=estado, fecha=f"{fecha_proceso:%Y%m%d}")
    _enviar(asunto, _plantilla("Notificación envío Botón de Pago Banco de Chile", contenido, fecha_proceso), adjuntos)
    return todo_ok


# ---------------------------------------------------------------------------
# Correo de error
# ---------------------------------------------------------------------------
def envio_correo_error(mensaje: str, fecha_proceso: date, pendientes: list = (), avisos: list = ()) -> None:
    pend_html = ""
    if pendientes:
        items = "".join(f"<li>{html.escape(p)}</li>" for p in pendientes)
        pend_html = ("<p><b>Archivos pendientes (NO enviados, se mantienen en la carpeta):</b></p>"
                     f"<ul>{items}</ul>")

    contenido = ("<p>El bot de envío Botón de Pago Banco de Chile SFTP PRODUCCIÓN <b>falló</b>. "
                 "Los archivos no fueron enviados al banco.</p>"
                 + _caja(f"❌ ERROR: {html.escape(mensaje)}", "#c00000")
                 + pend_html + _avisos_html(avisos)
                 + "<p>Revise el log en la carpeta <i>logs</i> del bot.</p>")

    asunto = config.CORREO_ASUNTO.format(estado=" [ERROR]", fecha=f"{fecha_proceso:%Y%m%d}")
    _enviar(asunto, _plantilla("ERROR envío Botón de Pago Banco de Chile", contenido, fecha_proceso))
