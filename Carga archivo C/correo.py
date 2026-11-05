import os
import win32com.client as win32
from datetime import datetime
import pandas as pd

CARPETA_BASE = r"C:\Virginia\P02 D2 - Carga de Archivo C"

def obtener_archivos_para_adjunto(carpeta):
    extensiones_validas = ('.xlsx', '.txt', '.log', '.dat')
    archivos = []
    for item in os.listdir(carpeta):
        ruta_completa = os.path.join(carpeta, item)
        if os.path.isfile(ruta_completa) and item.lower().endswith(extensiones_validas):
            archivos.append(item)
    return archivos


def envio_correo_outlook(empresa):
    carpeta_local = os.path.join(CARPETA_BASE, "Logs", empresa.upper())

    outlook = win32.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = 'diego.morales@aguasnuevas.cl;manuel.apeleo@aguasnuevas.cl'
    mail.CC = 'jorge.flores@aguasnuevas.cl;manuel.rodriguez@aguasnuevas.cl' 
    mail.Subject = f'Alerta Reporte Carga Archivo C {empresa} - {datetime.now().strftime("%Y-%m-%d")}'

    cuerpo_tablas_html = ""

    archivos_a_adjuntar = obtener_archivos_para_adjunto(carpeta_local)

    for archivo in archivos_a_adjuntar:
        ruta = os.path.join(carpeta_local, archivo)
        mail.Attachments.Add(ruta)

        # Solo para archivos Excel armamos la tabla en el cuerpo del correo
        if archivo.lower().endswith('.xlsx'):
            try:
                df = pd.read_excel(ruta)
                df = df.dropna(how='all')
                if "Errores" in df.columns:
                    df["Errores"] = pd.to_numeric(df["Errores"], errors="coerce").fillna(0)

                tabla_html = "<table border='1' cellspacing='0' cellpadding='4' style='font-family: Arial; font-size: 12px;'>"
                tabla_html += "<thead><tr>" + "".join(f"<th>{col}</th>" for col in df.columns) + "</tr></thead><tbody>"

                for _, row in df.iterrows():
                    estilo = "style='color: red; font-weight: bold;'" if "Errores" in df.columns and row["Errores"] > 0 else ""
                    tabla_html += "<tr>" + "".join(
                        f"<td {estilo if col == 'Errores' else ''}>{row[col]}</td>" for col in df.columns
                    ) + "</tr>"

                tabla_html += "</tbody></table>"

                cuerpo_tablas_html += f"""
                    <h4>📄 Contenido del archivo: <i>{archivo}</i></h4>
                    {tabla_html}
                    <br><hr><br>
                """
            except Exception as e:
                cuerpo_tablas_html += f"<p><strong>⚠️ Error al leer el archivo {archivo}:</strong> {e}</p><br>"

    mail.HTMLBody = f"""
    <div style="font-family: Arial; font-size: 12px;">
        <p>Estimado usuario,</p>
        <p>Se adjuntan los archivos generados automáticamente. A continuación se muestra el contenido de los archivos Excel:</p>

        {cuerpo_tablas_html}

        <p>Este es un correo automático, no responder.</p>
    </div>
    """

    mail.Send()
    print(f"📧 Correo enviado correctamente con {len(archivos_a_adjuntar)} archivos adjuntados.")
