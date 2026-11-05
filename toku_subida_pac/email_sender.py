import os
import logging

import win32com.client as win32

from datetime import datetime

from config import (
    EMAIL_TO,
    EMAIL_CC,
    LOCAL_FOLDER
)


def send_report(lista_ok, lista_fail):

    try:

        outlook = win32.Dispatch(
            "Outlook.Application"
        )

        mail = outlook.CreateItem(0)

        mail.To = EMAIL_TO
        mail.CC = EMAIL_CC

        fecha = datetime.now().strftime(
            "%Y-%m-%d"
        )

        mail.Subject = (
            f"Alerta SFTP Toku - {fecha}"
        )

        # Adjuntar archivos cargados
        for archivo in lista_ok:

            ruta = os.path.join(
                LOCAL_FOLDER,
                archivo
            )

            try:

                if os.path.exists(ruta):
                    mail.Attachments.Add(ruta)

            except Exception as e:

                logging.warning(
                    f"No se pudo adjuntar {archivo}: {e}"
                )

        filas_ok = "".join(
            [
                f"""
                <tr>
                    <td>{archivo}</td>
                </tr>
                """
                for archivo in lista_ok
            ]
        )

        if not filas_ok:

            filas_ok = """
            <tr>
                <td>Sin archivos</td>
            </tr>
            """

        filas_fail = "".join(
            [
                f"""
                <tr>
                    <td>{archivo}</td>
                </tr>
                """
                for archivo in lista_fail
            ]
        )

        if not filas_fail:

            filas_fail = """
            <tr>
                <td>Sin errores</td>
            </tr>
            """

        mail.HTMLBody = f"""
        <html>
        <body>

        <p>Estimados,</p>

        <p>
        Se ha ejecutado correctamente el proceso
        de carga de archivos hacia el SFTP de Toku.
        </p>

        <h3>✅ Archivos subidos correctamente</h3>

        <table border="1" cellpadding="5" cellspacing="0">
            <tr bgcolor="#D9EAD3">
                <th>Archivo</th>
            </tr>

            {filas_ok}

        </table>

        <br>

        <h3>❌ Archivos con error</h3>

        <table border="1" cellpadding="5" cellspacing="0">
            <tr bgcolor="#F4CCCC">
                <th>Detalle</th>
            </tr>

            {filas_fail}

        </table>

        <br>

        <p>
        Este es un correo automático.
        Favor no responder.
        </p>

        </body>
        </html>
        """

        mail.Send()

        logging.info(
            "Correo enviado correctamente"
        )

    except Exception as e:

        logging.exception(
            f"Error enviando correo: {e}"
        )

        raise